from flask import render_template,redirect,url_for
from flask import request
import datetime
from flask import Flask

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",datos=conn)
