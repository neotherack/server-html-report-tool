from Server_Checker import Server_Checker

c = Server_Checker(config_file = "windows.conf")
c.check_servers()
print(c.get_html_report())