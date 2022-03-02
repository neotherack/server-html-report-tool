import psutil
import os
import datetime

class Server:
    hostname = None
    friendly_name = None
    environment = None
    memory = None
    swap = None
    analysis_date = None
    application_list = None
    filesystems = None
    files = None

    def __init__(self, config):
        self.hostname = config["hostname"]
        self.friendly_name = config["friendly_name"]
        self.environment = config["environment"]
        self.analysis_date = datetime.datetime.now()
        self.application_list = config["application_list"]
        self.memory = config["memory"]
        self.swap = config["swap"]
        self.filesystems = config["filesystems"]
        self.files = config["files"]

    def __str__(self):
        return f"{self.hostname, self.friendly_name, self.environment, self.application_list, self.memory, self.swap, self.filesystems, self.files}"

    def to_json(self):
        return {"hostname": self.hostname, "friendly_name": self.friendly_name, 
                "environment": self.environment, "application_list": self.application_list,
                "memory": self.memory, "swap": self.swap, 
                "filesystems": self.filesystems, "files": self.files}

    def check_memory(self):
        self.memory["value"] = psutil.virtual_memory().percent
        self.memory["alarm"] = psutil.virtual_memory().percent > self.memory["limit"]

    def check_swap(self):
        self.swap["value"] = psutil.swap_memory().percent
        self.swap["alarm"] = psutil.swap_memory().percent > self.swap["limit"]

    def check_applications(self):
        for index, application in enumerate(self.application_list):
            self.application_list[index]["found"] = self.check_application(application["process_name"])

    def check_filesystems(self):
        for index, filesystem in enumerate(self.filesystems):
            value = self.check_filesystem(filesystem["mount_location"])
            self.filesystems[index]["found"] = value
            self.filesystems[index]["alarm"] = value > self.filesystems[index]["limit"]

    def check_files(self):
        for index, file in enumerate(self.files):
            value = self.check_file(file["location"])
            self.files[index]["found"] = value
            self.files[index]["alarm"] = value < 0 or value > self.files[index]["limit"]

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
        except Exception:
            print(f"EXCEPTION: analyzing file {path}\n{e}")