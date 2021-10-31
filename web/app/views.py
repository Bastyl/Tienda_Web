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


@app.route('/estadisticas',methods=['POST','GET'])
def estadisticas():

	sql = """SELECT COUNT(sector),sector FROM historial GROUP BY sector ORDER BY COUNT(sector) DESC;"""
	cur.execute(sql)
	comunas_mas_asaltadas = cur.fetchall()
	


	sql = """SELECT COUNT(usuario_id),usuario_id FROM historial GROUP BY usuario_id ORDER BY COUNT(usuario_id) DESC;"""
	cur.execute(sql)
	top_delincuentes = cur.fetchall()

	lista_de_delincuentes = []

	for i in top_delincuentes:
		sql = """SELECT delincuentes FROM delincuentes WHERE id = '%d' ;"""%(i[1])
		cur.execute(sql)
		lista_de_delincuentes.append(cur.fetchall())

	lista_top = []
	for i in range(0,len(lista_de_delincuentes)):
		lista_top.append(lista_de_delincuentes[i][0][0].split(','))
		lista_top[i][5] = lista_top[i][5].split(')')
		lista_top[i][0] = lista_top[i][0].split('(')
		lista_top[i][0][0] = top_delincuentes[i][0]

	return render_template("estadisticas.html",datos=lista_top,numero=top_delincuentes,comunas=comunas_mas_asaltadas)

@app.route('/ingresar',methods=['POST','GET'])
def ingresar_delincuente():

	if request.method == 'POST':

		#datos
		nombre = request.form['nombre']
		apellido_paterno = request.form['apellido_paterno']
		apellido_materno = request.form['apellido_materno']
		rut = request.form['rut']
		edad = request.form['edad']
		estatura = request.form['estatura']

		rut = int(rut)
		edad = int(edad)
		estatura = int(estatura)

		#caracteristicas
		sexo = request.form['sexo']

		tat1 = request.form['tat1']
		tat2 = request.form['tat2']
		tat3 = request.form['tat3']
		tat4 = request.form['tat4']

		tat1 = int(tat1)
		tat2 = int(tat2)
		tat3 = int(tat3)
		tat4 = int(tat4)

		piel = request.form['piel']
		nacionalidad = request.form['nacionalidad']
		ojos = request.form['ojos']
		pelo = request.form['pelo']
		contextura = request.form['contextura']
		tono = request.form['tono']

		#historial

		sector = request.form['sector']
		relato = request.form['historia']
		fecha = request.form['fecha']
		hora = request.form['hora']

		if relato != "":

			sql = """INSERT INTO delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad)
			VALUES ('%d','%s','%s','%s','%d');"""%(rut,nombre,apellido_paterno,apellido_materno,edad)
			cur.execute(sql)
			conn.commit()

			sql = """SELECT delincuentes.id FROM delincuentes WHERE delincuentes.rut = '%d';"""%(rut)
			cur.execute(sql)
			id = cur.fetchall()

			id_real = int(id[0][0])
			

			sql = """INSERT INTO caracteristicas (usuario_id,sexo,estatura,contextura_fisica,tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas)
			VALUES ('%d','%s','%d','%s','%s','%s','%s','%s','%s','%d','%d','%d','%d');"""%(id_real,sexo,estatura,contextura,piel,nacionalidad,tono,pelo,ojos,tat1,tat2,tat3,tat4)
			cur.execute(sql)
			conn.commit()


			sql = """INSERT INTO historial (usuario_id,sector,relato,fecha,hora) values ('%d','%s','%s','%s','%s');"""%(id_real,sector,relato,fecha,hora)
			cur.execute(sql)
			conn.commit()

			return render_template("index.html")
		else:
			return redirect(url_for('index'))


	return render_template("ingresar.html")


@app.route('/buscar',methods=['GET','POST'])
def buscar_delincuente():
	if request.method == 'GET' and request.args.get('min') != None and request.args.get('max') != None:

		sexo = request.args.get('sexo')
		min = request.args.get('min')
		max = request.args.get('max')
		tat1 = request.args.get('tat1')
		tat2 = request.args.get('tat2')
		tat3 = request.args.get('tat3')
		tat4 = request.args.get('tat4')

		piel = request.args.get('piel')
		nacionalidad = request.args.get('nacionalidad')
		ojos = request.args.get('ojos')
		pelo = request.args.get('pelo')
		contextura = request.args.get('contextura')
		tono = request.args.get('tono')

		char0 = """SELECT delincuentes FROM delincuentes,caracteristicas WHERE estatura BETWEEN '{0}' AND '{1}' AND sexo = '{2}' AND delincuentes.id = caracteristicas.usuario_id """
		endd = " ;"""


		chartat1 = ""
		chartat2 = ""
		chartat3 = ""
		chartat4 = ""

		if tat1 == "cara":
			chartat1 = " AND tatuaje_cara = '1' "
		if tat2 == "torso":
			chartat2 = " AND tatuaje_torso = '1' "
		if tat3 == "brazos":
			chartat3 = " AND tatuaje_brazos = '1' "
		if tat4 == "piernas":
			chartat4 = " AND tatuaje_piernas = '1' "

		char0 = char0 + chartat1 + chartat2 + chartat3 + chartat4


		char1 = " AND tez_piel = '{3}' "
		char2 = " AND nacionalidad = '{4}' "
		char3 = " AND color_ojos = '{5}' "
		char4 = " AND color_pelo = '{6}' "
		char5 = " AND contextura_fisica = '{7}' "
		char6 = " AND tono_voz = '{8}' "

		if piel == "":
			char1 = " AND tez_piel != '{3}' "
		if nacionalidad == "":
			char2 = " AND nacionalidad != '{4}' "
		if ojos == "":
			char3 = " AND color_ojos != '{5}' "
		if pelo == "":
			char4 = " AND color_pelo != '{6}' "
		if contextura == "":
			char5 = " AND contextura_fisica != '{7}' "
		if tono == "":
			char6 = " AND tono_voz != '{8}' "


		s1 = char0 + char1 + char2 + char3 + char4 + char5 + char6
		sql = s1 .format(min,max,sexo,piel,nacionalidad,ojos,pelo,contextura,tono)
		cur.execute(sql)
		s1 = cur.fetchall()

		s2 = char0 + char1 + char2 + char3 + char4 + char5
		sql = s2 .format(min,max,sexo,piel,nacionalidad,ojos,pelo,contextura)
		cur.execute(sql)
		s2 = cur.fetchall()

		s3 = char0 + char1 + char2 + char3 + char4
		sql = s3 .format(min,max,sexo,piel,nacionalidad,ojos,pelo)
		cur.execute(sql)
		s3 = cur.fetchall()

		s4 = char0 + char1 + char2 + char3
		sql = s4 .format(min,max,sexo,piel,nacionalidad,ojos)
		cur.execute(sql)
		s4 = cur.fetchall()

		s5 = char0 + char1 + char2
		sql = s5 .format(min,max,sexo,piel,nacionalidad)
		cur.execute(sql)
		s5 = cur.fetchall()

		s6 = char0 + char1
		sql = s6 .format(min,max,sexo,piel)
		cur.execute(sql)
		s6 = cur.fetchall()

		#s7 = char0
		#sql = s7 .format(min,max,sexo)
		#cur.execute(sql)
		#s7 = cur.fetchall


		sospechosos = s1+s2+s3+s4+s6+s6

		mi_lista = []
		for i in sospechosos:
			if i not in mi_lista:
				mi_lista.append(i)

		lista_final = []
		for i in mi_lista:
			lista_final.append(i[0].split(','))

		for i in range(0,len(lista_final)):
			lista_final[i][0] = lista_final[i][0].split('(')
			lista_final[i][5] = lista_final[i][5].split(')')

		
		return lista(lista_final)

	return render_template("buscar_delincuente.html")


def lista(sospechosos):
	return render_template("lista.html",sospechosos=sospechosos)

@app.route('/delincuente/<id>',methods=['GET','POST'])
def delincuente(id):
	sql = """SELECT delincuentes FROM delincuentes,historial WHERE delincuentes.id = historial.usuario_id AND delincuentes.id = '%s';"""%(id)
	cur.execute(sql)
	delincuente = cur.fetchall()

	sql = """SELECT historial FROM delincuentes,historial WHERE delincuentes.id = historial.usuario_id AND delincuentes.id = '%s';"""%(id)
	cur.execute(sql)
	historial = cur.fetchall()

	delincuente1 = delincuente[0][0].split(',')
	delincuente1[0] = delincuente1[0].split('(')
	delincuente1[5] = delincuente1[5].split(')')

	historial1 = []
	for i in range(0,len(historial)):
		historial1.append(historial[i][0].split(','))
		historial1[i][5] = historial1[i][5].split(')')
		historial1[i][0] = historial1[i][0].split('(')

	if request.method == 'POST':

		val = request.form['method_']
		if val == "ELIMINAR":
			sql = """DELETE FROM delincuentes WHERE delincuentes.id = '%s';"""%(id)
			cur.execute(sql)
			cur.close

			sql = """DELETE FROM caracteristicas WHERE caracteristicas.usuario_id = '%s';"""%(id)
			cur.execute(sql)
			cur.close

			sql = """DELETE FROM historial WHERE historial.usuario_id = '%s';"""%(id)
			cur.execute(sql)
			cur.close

			return redirect(url_for('index'))

		id_real = int(id)

		val2 = request.form['method_2']
		if val2 != "NO_ELIMINAR":
			sql = """DELETE FROM historial WHERE historial.id = '%s';"""%(val2)
			cur.execute(sql)
			cur.close
			#return redirect(url_for('index'))

		relato = request.form['historia']

		if relato != '':
			sector = request.form['sector']
			fecha = request.form['fecha']
			hora = request.form['hora']
			sql = """INSERT INTO historial (usuario_id,sector,relato,fecha,hora) values ('%d','%s','%s','%s','%s');"""%(id_real,sector,relato,fecha,hora)
			cur.execute(sql)
			conn.commit()

		sql = """SELECT delincuentes FROM delincuentes,historial WHERE delincuentes.id = historial.usuario_id AND delincuentes.id = '%s';"""%(id_real)
		cur.execute(sql)
		delincuente = cur.fetchall()

		sql = """SELECT historial FROM delincuentes,historial WHERE delincuentes.id = historial.usuario_id AND delincuentes.id = '%s';"""%(id_real)
		cur.execute(sql)
		historial = cur.fetchall()

		delincuente1 = delincuente[0][0].split(',')
		delincuente1[0] = delincuente1[0].split('(')
		delincuente1[5] = delincuente1[5].split(')')

		historial1 = []
		for i in range(0,len(historial)):
			historial1.append(historial[i][0].split(','))
			historial1[i][5] = historial1[i][5].split(')')
			historial1[i][0] = historial1[i][0].split('(')
		
		return render_template("delincuente.html",delincuente=delincuente1,historial=historial1)

	#if method DELETE?????	

	return render_template("delincuente.html",delincuente=delincuente1,historial=historial1)
