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
                server = Server(config = server_config)
                server_report = Server_Report(server)
                server_report.check_server()
                self.servers.append(server)
                self.reports.append(server_report.get_html_report())
        else:
            raise ValueError("EXCEPTION: faulty config")

    def get_html_report(self):
        report = """<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Server analytics by Microfocus Professional Services</title>
	</head>
	<body style="background-color:grey">
		<table align="center" border="0" cellpadding="0" cellspacing="0"
			   bgcolor="white" style="border:2px solid #0079EF">
			<tbody>
				<tr>
					<td align="center">
						<table align="center" border="0" cellpadding="0"
							   cellspacing="0" class="col-550" width="550">
							<tbody>
								<tr>
									<td align="center" style="background-color:#0079EF;height: 50px;">
										<p style="color:white;font-weight:bold;">
											Server analytics by Microfocus Professional Services
										</p>
									</td>
								</tr>
							</tbody>
						</table>
					</td>
				</tr>
				<tr style="display: column">
					<td style="height: 150px;
							   padding: 2px;
							   border: none; 
							   border-bottom: 1px solid #0079EF;
							   background-color: white;">"""

        for server_report in self.reports:
            report += server_report

        report +=    """				</tr>
				</tr>
				<tr style="border: none; 
				background-color: #0079EF; 
				height: 40px; 
				color:white; 
				padding-bottom: 20px; 
				text-align: center;">
					  
					<td height="40px" align="center">
						<p style="color:white; 
						line-height: 1.5em;">
						Microfocus Professional Services Iberia
						</p>
					</td>
				</tr>
				<tr>
					<td style="font-family:'Open Sans', Arial, sans-serif;
							   font-size:11px; line-height:18px; 
							   color:#999999;" 
						valign="top"
						align="center">
					</td>
				</tr>
				<tr>
				  <td class="em_hide"
				  style="line-height:1px;
						 min-width:700px;
						 background-color: #0079EF;">
					  <img alt="" 
					  src="images/spacer.gif" 
					  style="max-height:1px; 
					  min-height:1px; 
					  display:block; 
					  width:700px; 
					  min-width:700px;" 
					  width="700"
					  border="0" 
					  height="1">
					  </td>
				</tr>
			</tbody>
		</table>
	</body>
</html>"""
        return report