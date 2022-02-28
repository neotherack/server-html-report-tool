from Server_Checker import Server_Checker

c = Server_Checker(config_file = "windows.conf")
c.check_servers()

for server,report in zip(c.servers,c.reports):
    print(server)
    print(report)