from Server import Server

class Server_Report:

    server:Server = None

    def __init__(self, server:Server):
        self.server = server

    def check_server(self):
        self.server.check_memory()
        self.server.check_swap()
        self.server.check_applications()
        self.server.check_filesystems()
        self.server.check_files()

    def get_html_report(self):
        return "<html></html>"