import psutil
import os
import datetime
import docker

class Server:
    hostname = None
    port = None
    friendly_name = None
    environment = None
    alarm = None
    memory = None
    swap = None
    analysis_date = None
    application_list = None
    filesystems = None
    files = None
    containers = None
    format = None

    def __init__(self, config):
        self.hostname = config["hostname"]
        self.port = config["port"]
        self.friendly_name = config["friendly_name"]
        self.environment = config["environment"]
        self.application_list = config["application_list"]
        self.memory = config["memory"]
        self.swap = config["swap"]
        self.filesystems = config["filesystems"]
        self.files = config["files"]
        self.containers = config["containers"]
        self.format = "%d/%m/%Y %H:%M:%S"

    def __str__(self):
        return f"{self.hostname, self.friendly_name, self.environment, self.application_list, self.memory, self.swap, self.filesystems, self.files, self.containers}"

    def to_json(self):
        return {"hostname": self.hostname, "friendly_name": self.friendly_name, 
                "environment": self.environment, "application_list": self.application_list,
                "memory": self.memory, "swap": self.swap, 
                "filesystems": self.filesystems, "files": self.files, "containers": self.containers}

    def check_server(self):
        self.alarm = False
        self.analysis_date = datetime.datetime.now().strftime(self.format)
        self.check_memory()
        self.check_swap()
        self.check_applications()
        self.check_filesystems()
        self.check_files()
        self.check_containers()

    def check_memory(self):
        try:
            self.memory["value"] = psutil.virtual_memory().percent
            self.memory["alarm"] = psutil.virtual_memory().percent > self.memory["limit"]
            self.alarm = self.alarm or self.memory["alarm"]
        except:
            self.memory["value"] = -1
            self.memory["alarm"] = True
            self.alarm = self.alarm or True

    def check_swap(self):
        try:
            self.swap["value"] = psutil.swap_memory().percent
            self.swap["alarm"] = psutil.swap_memory().percent > self.swap["limit"]
            self.alarm = self.alarm or self.swap["alarm"]
        except:
            self.memory["value"] = -1
            self.memory["alarm"] = True
            self.alarm = self.alarm or True

    def check_applications(self):
        for index, application in enumerate(self.application_list):
            try:
                self.application_list[index]["found"] = self.check_application(application["process_name"])
                self.alarm = self.alarm or self.application_list[index]["found"] == False
            except:
                self.application_list[index]["found"] = False
                self.alarm = self.alarm or True

    def check_filesystems(self):
        for index, filesystem in enumerate(self.filesystems):
            try:
                value = self.check_filesystem(filesystem["mount_location"])
                self.filesystems[index]["found"] = value
                self.filesystems[index]["alarm"] = value > self.filesystems[index]["limit"]
                self.alarm = self.alarm or self.filesystems[index]["alarm"]
            except:
                self.filesystems[index]["found"] = -1
                self.filesystems[index]["alarm"] = True
                self.alarm = self.alarm or True

    def check_files(self):
        for index, file in enumerate(self.files):
            try:
                value = self.check_file(file["location"])
                self.files[index]["found"] = value
                self.files[index]["alarm"] = value < 0 or value > self.files[index]["limit"]
                self.alarm = self.alarm or self.files[index]["alarm"]
            except: 
                self.files[index]["found"] = -1
                self.files[index]["alarm"] = True
                self.alarm = self.alarm or True

    def check_containers(self): 
        for index, container in enumerate(self.containers):
            try:
                value = self.check_container(container["name"])
                self.containers[index]["found"] = value
                self.alarm = self.alarm or self.containers[index]["found"] == False
            except:
                self.containers[index]["found"] = False
                self.alarm = self.alarm or True

    def check_application(self, processName):
        for proc in psutil.process_iter():
            try:
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False;

    def check_filesystem(self, path):
        return psutil.disk_usage(path=path).percent

    def check_file(self, path):
        try:
            return os.path.getsize(path)
        except FileNotFoundError:
            return -1
        except Exception as e:
            print(f"EXCEPTION: analyzing file {path}\n{e}")

    def check_container(self, container_name):
        """Verify the status of a container by it's name

        :param container_name: the name of the container
        :return: boolean or None
        """
        RUNNING = "running"
        # Connect to Docker using the default socket or the configuration
        # in your environment
        docker_client = docker.from_env()
        # Or give configuration
        # docker_socket = "unix://var/run/docker.sock"
        # docker_client = docker.DockerClient(docker_socket)

        try:
            container = docker_client.containers.get(container_name)
        except docker.errors.NotFound as exc:
            print(f"Check container name!\n{exc.explanation}")
        else:
            container_state = container.attrs["State"]
            return container_state["Status"] == RUNNING