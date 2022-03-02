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

    def humanbytes(self, B):
        """Return the given bytes as a human friendly KB, MB, GB, or TB string."""
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2) # 1,048,576
        GB = float(KB ** 3) # 1,073,741,824
        TB = float(KB ** 4) # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B / KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B / MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B / GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B / TB)

    def get_html_report(self):
        report  = f"""<div class="pure-g">
                        <div class="pure-u-1-3"><p></p></div>
                        <div class="pure-u-1-3"><p></p></div>
                        <div class="pure-u-1-3"><p></p></div>
                    </div>
                    <div class="pure-g">
                        <div class="pure-u-1-3"><p>Date: {self.server.analysis_date}</p></div>
                        <div class="pure-u-1-3"><p>RAM: {self.server.memory}</p></div>
                        <div class="pure-u-1-3"><p>SWAP: {self.server.swap}</p></div>
                    </div>"""

        report = f"""<table align="center" border="1px solid #0079EF" cellpadding="0"
							   cellspacing="0" class="col-550" width="550">
							<tbody>
								<tr>
									<td align="center" style="background-color: white;height: 50px;color:#0079EF;">
										<p>
											<span style="font-weight:bold;">{self.server.friendly_name} &nbsp; [{self.server.environment}]</span><br/>
											Hostname: &nbsp; {self.server.hostname} <br/>
											Report date:  &nbsp; {self.server.analysis_date}
										</p>
									</td>
								</tr>
								<tr>
									<td align="center" style="background-color: white;height: 50px;color:black;">
										<h3>System performance</h3>
										<table style="width:100%">
											<tr>
												<td align="left"><label>RAM usage</td>
												<td><span style="font-weight:bold;color:{"red" if self.server.memory["alarm"] else "green"}">{self.server.memory["value"]}%</span></label></td>
												<td align="center"><progress value="{self.server.memory["value"]}" max="100" style="width:300px;height:40px"></progress></td>
											</tr>
											<tr>
												<td align="left"><label >SWAP usage</td>
												<td><span style="font-weight:bold;color:{"red" if self.server.swap["alarm"] else "green"}">{self.server.swap["value"]}%</span></label></td>
												<td align="center"><progress value="{self.server.swap["value"]}" max="100" style="width:300px;height:40px"></progress></td>
											</tr>
										</table>
										
										<h3>Application check</h3>
										<table style="width:75%">"""

        for app in self.server.application_list:
            report += f"""											<tr>
												<td align="left">{app["friendly_name"]}</td>
												<td><span style="font-weight:bold;color:{"green" if app["found"] else "red"}">{"Present" if app["found"] else "Not present"}</span></td>
											</tr>"""

        report += f"""										</table>
										
										<h3>Filesystem status</h3>
										<table style="width:100%">"""
		
        for fs in self.server.filesystems:
            report += f"""									<tr>
												<td align="left"><label>{fs["mount_location"]}</td>
												<td><span style="font-weight:bold;color:{"red" if fs["alarm"] else "green"}">{fs["found"]}</span></label></td>
												<td align="center"><progress value="{fs["found"]}" max="100" style="width:300px;height:40px"></progress></td>
											</tr>"""

        report += f"""								</table>
										
										<h3>File size check</h3>
										<table style="width:75%">"""

        for file in self.server.files:
            report += f"""									<tr>
												<td align="left">{file["location"]}</td>
												<td><span style="font-weight:bold;color:>{"green" if file["found"]>0 else "red"}">{self.humanbytes(file["found"]) if file["found"]>0 else "Not Found"}</span></td>
												<td><span style="font-weight:bold;color:{"red" if file["alarm"] else "green"}">{"KO" if file["alarm"] else "OK"}</span></td>
											</tr>"""

        report +="""								</table>
									</td>
								</tr>
							</tbody>
						</table>"""

        return report