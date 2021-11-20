from flask import render_template,redirect,url_for
from flask import request
import datetime
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
