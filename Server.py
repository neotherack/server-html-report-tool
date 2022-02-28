import psutil
import os

class Server:
    hostname = None
    friendly_name = None
    environment = None

    application_list = None
    memory = None
    swap = None
    filesystems = None
    files = None

    def __init__(self, config):
        self.hostname = config["hostname"]
        self.friendly_name = config["friendly_name"]
        self.environment = config["environment"]

        self.application_list = config["application_list"]
        self.memory = config["memory_alert"]
        self.swap = config["swap_alert"]
        self.filesystems = config["filesystems"]
        self.files = config["files"]

    def __str__(self):
        return f"{self.hostname, self.friendly_name, self.environment, self.application_list, self.memory, self.swap, self.filesystems, self.files}"

    def check_memory(self):
        self.memory["status"]["value"] = psutil.virtual_memory().percent
        self.memory["status"]["alarm"] = psutil.virtual_memory().percent > self.memory["config"]

    def check_swap(self):
        self.swap["status"]["value"] = psutil.swap_memory().percent
        self.swap["status"]["alarm"] = psutil.swap_memory().percent > self.swap["config"]

    def check_applications(self):
        for application in self.application_list["config"]:
            self.application_list[application["friendly_name"]]["status"] = self.check_application(application["process_name"])

    def check_filesystems(self):
        for filesystem in self.filesystems["config"]:
            self.filesystems[filesystem["mount_location"]]["status"] = self.check_filesystem(filesystem["mount_location"])

    def check_files(self):
        for file in self.files["config"]:
            self.files[file["location"]]["status"] = self.check_file(file["location"])

    def check_application(self, processName):
        for proc in psutil.process_iter():
            try:
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False;

    def check_filesystem(self, path):
        return psutil.disk_usage(path=path)

    def check_file(self, path):
        return os.path.getsize(path)