from app import app
from flask import render_template,redirect,url_for
from flask import request
from app.configuraciones import *


import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()


@app.route('/')
@app.route('/index',methods=['POST','GET'])
def index():

	return render_template("index.html")

@app.route('/ver_cojines',methods=['POST','GET'])
def ver_cojines():

	sql = """SELECT * FROM cojines, caracteristicas_cojin, relleno, tela WHERE cojines.caracteristicas_cojin_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id;"""
	cur.execute(sql)
	lista_cojines = cur.fetchall()
	print(lista_cojines)

	return render_template("ver_cojines.html",datos=lista_cojines)

@app.route('/ver_cojines/<id>',methods=['GET','POST'])
def cojin_especifico(id):
	sql = """SELECT * FROM cojines, caracteristicas_cojin, relleno, tela WHERE cojines.id = '%s' AND cojines.caracteristicas_cojin_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id;"""%(id)
	cur.execute(sql)
	cojin_especifico = cur.fetchall()
	print(cojin_especifico)	
	return render_template("cojin_especifico.html",datos=cojin_especifico)