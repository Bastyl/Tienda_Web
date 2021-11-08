from app import app
from flask import render_template,redirect,url_for
from flask import request
from app.configuraciones import *
import datetime


import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()


@app.route('/')
@app.route('/index',methods=['POST','GET'])
def index():

	return render_template("index.html")

@app.route('/ver_cojines',methods=['POST','GET'])
def ver_cojines():

	sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela WHERE producto.tipo_producto ='%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id;"""%('cojin')
	cur.execute(sql)
	lista_cojines = cur.fetchall()

	print(lista_cojines)

	return render_template("ver_cojines.html",datos=lista_cojines)

@app.route('/ver_cojines/<id>',methods=['GET','POST'])
def cojin_especifico(id):
	sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela WHERE producto.id = '%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id;"""%(id)
	cur.execute(sql)
	cojin_especifico = cur.fetchall()
	print(cojin_especifico)
	return render_template("cojin_especifico.html",datos=cojin_especifico)

@app.route('/comprar/<id>',methods=['POST','GET'])
def comprar(id):

	cantidad = int(request.args.get('cantidad'))

	sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela WHERE producto.id = '%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id;"""%(id)
	cur.execute(sql)
	cojin_especifico = cur.fetchall()

	valor_unitario = cojin_especifico[0][5]

	if request.method == 'POST':
		nombre = request.form['nombre']
		apellido = request.form['apellido']
		rut2 = request.form['rut']
		mail = request.form['mail']
		telefono2 = request.form['telefono']
		ciudad = request.form['ciudad']
		comuna = request.form['comuna']
		direccion = request.form['direccion']

		#factura = request.form['adjunto'] FALTA AGREGAR FACTURA

		rut = int(rut2)
		telefono = int(telefono2)
		id_producto = int(id)
		c = datetime.datetime.now()
		fecha = c.strftime("%x")
		pendiente = "pendiente"
		pago = cantidad*valor_unitario

		sql = """INSERT INTO compras (nombre_comprador,apellido_comprador,rut,mail,telefono,ciudad,comuna,direccion,id_producto,cantidad, estado, fecha,pagado)
		VALUES ('%s','%s','%d','%s','%d','%s','%s','%s','%d','%d','%s','%s','%d');"""%(nombre,apellido,rut,mail,telefono,ciudad,comuna,direccion,id_producto, cantidad, pendiente,fecha,pago)
		cur.execute(sql)
		conn.commit()

		sql = """SELECT stock FROM producto WHERE producto.id = '%d';"""%(id_producto)
		cur.execute(sql)
		cantidad_actual = cur.fetchall()
		print(cantidad_actual[0][0])

		cantidad_nueva = cantidad_actual[0][0] - cantidad
		sql = """UPDATE producto SET stock = '%d' WHERE producto.id = '%d';"""%(cantidad_nueva,id_producto)
		cur.execute(sql)
		conn.commit()

		return render_template("compra_finalizada.html")


	return render_template("comprar.html",datos=cojin_especifico,cantidad=cantidad)


@app.route('/miscompras',methods=['POST','GET'])
def mis_compras():
	if request.args.get('rut') != None:
		rut = int(request.args.get('rut'))
		sql = """SELECT * FROM compras, producto, caracteristicas_cojin, relleno, tela WHERE
		compras.rut = '%d' AND compras.id_producto = producto.id AND producto.caracteristicas_id = caracteristicas_cojin.id 
		AND caracteristicas_cojin.id_tela = tela.id AND caracteristicas_cojin.id_relleno = relleno.id;"""%(rut)
		cur.execute(sql)
		compras = cur.fetchall()

		if len(compras)>0:
			print(compras)
			return render_template("mis_compras.html",compras=compras,valido=False)
		else:
			print("no hay compras")
			return render_template("mis_compras.html",compras=compras,valido=True)

	return render_template("mis_compras.html")

@app.route('/miscompras/rut=<rut>/<id>/<id_producto>',methods=['POST','GET'])
def mis_compras_factura(rut,id,id_producto):
	codigo_factura = id
	codigo_producto = id_producto
	print(codigo_producto)
	return render_template("mis_compras_factura.html",codigo=codigo_factura,codigo2=codigo_producto)

@app.route('/armatucojin',methods=['POST','GET'])
def armar_cojin():

	return render_template("armar_cojin.html")



# DESDE ACA VA LA RESTRICCION DEL LOGIN PARA VER LA VISTA:

@app.route('/administrar',methods=['POST','GET'])
def administrar():
	sql = """SELECT * FROM compras, producto WHERE compras.id_producto = producto.id ORDER BY compras.id desc;"""
	cur.execute(sql)
	datos = cur.fetchall()

	if request.method == 'POST':

		codigo = request.form['codigo_id']
		codigo = int(codigo)
		estado = request.form['estado']

		if request.form['boton'] == 'Finalizar' and estado == 'pendiente':
			sql = """UPDATE compras SET estado = '%s' WHERE compras.id = '%d';"""%('confirmado',codigo)
			cur.execute(sql)
			conn.commit()

		if request.form['boton'] == 'Cancelar' and estado == 'pendiente':
			print("cancelar")
			sql = """SELECT id_producto,cantidad FROM compras WHERE compras.id = '%d';"""%(codigo)
			cur.execute(sql)
			a = cur.fetchall()

			sql = """SELECT stock FROM producto WHERE producto.id = '%d';"""%(a[0][0])
			cur.execute(sql)
			stock = cur.fetchall()

			modificar = int(stock[0][0])+int(a[0][1])

			sql = """UPDATE producto SET stock = '%d' WHERE producto.id = '%d';"""%(modificar,a[0][0])
			cur.execute(sql)
			conn.commit()

			sql = """UPDATE compras SET estado = '%s' WHERE compras.id = '%d';"""%('cancelado',codigo)
			cur.execute(sql)
			conn.commit()

		if request.form['boton'] == 'Eliminar' and estado == 'pendiente':
			print("eliminar")
			sql = """SELECT id_producto,cantidad FROM compras WHERE compras.id = '%d';"""%(codigo)
			cur.execute(sql)
			a = cur.fetchall()

			sql = """SELECT stock FROM producto WHERE producto.id = '%d';"""%(a[0][0])
			cur.execute(sql)
			stock = cur.fetchall()

			modificar = int(stock[0][0])+int(a[0][1])

			sql = """UPDATE producto SET stock = '%d' WHERE producto.id = '%d';"""%(modificar,a[0][0])
			cur.execute(sql)
			conn.commit()

			sql = """DELETE FROM compras WHERE compras.id = '%d';"""%(codigo)
			cur.execute(sql)
			conn.commit()

		if request.form['boton'] == 'Eliminar' and estado == 'cancelado':
			sql = """DELETE FROM compras WHERE compras.id = '%d';"""%(codigo)
			cur.execute(sql)
			conn.commit()

		sql = """SELECT * FROM compras, producto WHERE compras.id_producto = producto.id ORDER BY compras.id desc;"""
		cur.execute(sql)
		datos = cur.fetchall()
		return render_template("administrar_web.html",datos=datos)
			

	return render_template("administrar_web.html",datos=datos)

@app.route('/administrar_cojines',methods=['POST','GET'])
def administrar_cojines():
	sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela WHERE producto.tipo_producto ='%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id ORDER BY producto.id;"""%('cojin')
	cur.execute(sql)
	productos = cur.fetchall()

	if request.method == 'POST':
		nombre = request.form['nombre']
		codigo_id = int(request.form['codigo_id'])
		stock = int(request.form['stock'])
		precio = int(request.form['precio'])
		
		if request.form['boton'] == 'Guardar':
  			sql = """UPDATE producto SET titulo = '%s',stock = '%d', precio_unitario = '%d' WHERE id = '%d';"""%(nombre,stock,precio,codigo_id)
  			cur.execute(sql)
  			conn.commit()
  			sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela WHERE producto.tipo_producto ='%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id ORDER BY producto.id;"""%('cojin')
  			cur.execute(sql)
  			productos = cur.fetchall()

  			return render_template("administrar_cojin.html",productos=productos,a=True,b=True)
		if request.form['boton'] == 'Eliminar':
			sql = """SELECT rut FROM compras WHERE compras.id_producto = '%s';"""%(codigo_id)
			cur.execute(sql)
			compras = cur.fetchall()

			if len(compras) > 0:
				return render_template("administrar_cojin.html",productos=productos,a=True,b=False)
			else:
				sql = """SELECT caracteristicas_id FROM producto WHERE producto.id = '%d';"""%(codigo_id)
				cur.execute(sql)
				caracteristicas_id = cur.fetchall()

				c = int(caracteristicas_id[0][0])

				sql = """DELETE FROM producto WHERE producto.id = '%d';"""%(codigo_id)
				cur.execute(sql)
				conn.commit()

				sql = """DELETE FROM caracteristicas_cojin WHERE caracteristicas_cojin.id = '%d';"""%(c)
				cur.execute(sql)
				conn.commit()

				sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela WHERE producto.tipo_producto ='%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id ORDER BY producto.id;"""%('cojin')
				cur.execute(sql)
				productos = cur.fetchall()

				return render_template("administrar_cojin.html",productos=productos,a=False,b=True)


	return render_template("administrar_cojin.html",productos=productos,a=False,b=False)

@app.route('/ingresar_cojin',methods=['POST','GET'])
def ingresar_cojin():
	if request.method == 'POST':
		nombre = request.form['nombre']
		stock = int(request.form['stock'])
		precio = int(request.form['precio'])
		tela = int(request.form['tela'])
		relleno = int(request.form['relleno'])
		altura = int(request.form['altura'])
		ancho = int(request.form['ancho'])


		sql = """INSERT INTO caracteristicas_cojin (id_relleno, altura, ancho, id_tela )
		VALUES ('%d','%d','%d','%d') RETURNING id"""%(relleno,altura,ancho,tela)
		cur.execute(sql)
		conn.commit()
		a = cur.fetchall()
		id_caracteristica = a[0][0]

		sql = """INSERT INTO producto (tipo_producto, titulo, caracteristicas_id, stock, precio_unitario)
		VALUES ('%s','%s','%d','%d','%d')"""%('cojin',nombre,id_caracteristica,stock,precio)
		cur.execute(sql)
		conn.commit()

	return render_template("administrar_crearcojin.html")

@app.route('/administrar/<id>/<id_producto>',methods=['POST','GET'])
def ver_facturayproducto(id,id_producto):
	codigo_factura = id
	codigo_producto = id_producto
	print(codigo_producto)
	return render_template("administrar_verfacturayproducto.html",codigo=codigo_factura,codigo2=codigo_producto)
