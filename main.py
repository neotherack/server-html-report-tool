from flask import Flask

from Server_Report import Server_Report
from Server_Config import Server_Config
from Mailer import Mailer

cnf = Server_Config('properties.conf')
rpt = Server_Report(cnf.get_config())
app = Flask(__name__)

@app.route('/')
def server_report():
    print(f"Checking server...")
    rpt.server.check_server()
    print(f"Building report...")
    return rpt.get_html_report()

def monitoring():
    print(f"Checking server...")
    rpt.server.check_server()
    print(f"Building report...")
    email_body = rpt.get_html_report()

    #print(email_body)

    if rpt.server.alarm:
      print(f"Alarm on {rpt.server.hostname}!")

      m = Mailer(rpt.server.mail_host, rpt.server.mail_port)
      m.build_message( rpt.server.mail_from, rpt.server.mail_to, \
        f"Server alarm detected {rpt.server.friendly_name} - {rpt.server.environment}", email_body)
      m.send()

    else:
      print(f"Everything is fine")

if __name__ == '__main__':
    app.run(host=rpt.server.hostname, port=rpt.server.port)