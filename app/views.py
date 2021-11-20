from app import app
from flask import render_template,redirect,url_for
from flask import request
from app.configuraciones import *
import datetime


import psycopg2


@app.route('/')
@app.route('/index',methods=['POST','GET'])
def index():

	return render_template("index.html")
