from flask import Flask

from Server_Report import Server_Report
from Server_Config import Server_Config

cnf = Server_Config('windows.conf')
rpt = Server_Report(cnf.get_config())
app = Flask(__name__)

@app.route('/')
def server_report():
    print(f"Checking server...")
    rpt.server.check_server()
    print(f"Building report...")
    return rpt.get_html_report()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=rpt.server.port)