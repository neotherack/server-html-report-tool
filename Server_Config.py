import json

class Server_Config:

    config = None

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

    def get_config(self):
        return self.config