from Server import Server
from Server_Report import Server_Report
import json

class Server_Checker:

    config = None
    servers = []
    reports = []

    def __init__(self, config_file):
        try:
            f = open(config_file,"r")
            cnf = f.read()
            self.config = json.loads("".join(cnf))
        except FileNotFoundError:
            print(f"Config {config_file} not found")
        except json.decoder.JSONDecodeError:
            print(f"Cannot parse as JSON {cnf}")
        except Exception as e:
            print(f"EXCEPTION: {e}")

    def check_servers(self):
        if self.config:
            for server_config in self.config:
                s = Server_Report(Server(config = server_config))
                s.check_server()
                self.servers.append(s)
                self.reports.append(s.get_html_report())
        else:
            raise ValueError("EXCEPTION: faulty config")
