from flask import render_template,redirect,url_for
from flask import request
import datetime
from flask import Flask

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def index():
    sql = """SELECT * FROM tela;"""
    cur.execute(sql)
    a = cur.fetchall()

    return render_template("index.html",datos=a)
