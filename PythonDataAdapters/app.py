"""
Stimulsoft.Reports.JS
Version: 2025.2.2
Build date: 2025.04.08
License: https://www.stimulsoft.com/en/licensing/reports
"""

from flask import Flask, render_template, request
from stimulsoft_data_adapters import StiBaseHandler

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/handler', methods = ['GET', 'POST'])
def handler():
    handler = StiBaseHandler()
    handler.processRequest(request)
    return handler.getFrameworkResponse()

if __name__ == "__main__":
    app.run(debug=True, port=8040)