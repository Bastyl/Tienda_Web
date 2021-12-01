from flask import render_template,redirect,url_for
from flask import request, flash, Blueprint
import datetime
from flask import Flask
import psycopg2
import os
import base64

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import *
from flask_login import LoginManager,login_user,login_required, current_user, logout_user

app = Flask(__name__)

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()


@app.route('/')
@app.route('/index',methods=['POST','GET'])
def index():
	return render_template("index.html")


@app.route('/ver_cojines',methods=['POST','GET'])
def ver_cojines():

	sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela, imagen WHERE producto.tipo_producto ='%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id AND caracteristicas_cojin.id = imagen.id_tela;"""%('cojin')
	cur.execute(sql)
	lista_cojines = cur.fetchall()

	return render_template("ver_cojines.html",datos=lista_cojines)

@app.route('/ver_cojines/<id>',methods=['GET','POST'])
def cojin_especifico(id):
	sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela, imagen WHERE producto.id = '%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id AND caracteristicas_cojin.id = imagen.id_tela;"""%(id)
	cur.execute(sql)
	cojin_especifico = cur.fetchall()
	return render_template("cojin_especifico.html",datos=cojin_especifico)

@app.route('/comprar/<id>',methods=['POST','GET'])
def comprar(id):


	cantidad = int(request.args.get('cantidad'))

	sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela, imagen WHERE producto.id = '%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id AND caracteristicas_cojin.id = imagen.id_tela;"""%(id)
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

		pic = request.files['adjunto']
		filename = pic.mimetype
		image_string = base64.b64encode(pic.read())
		pic = image_string.decode()


		sql = """INSERT INTO compras (nombre_comprador,apellido_comprador,rut,mail,telefono,ciudad,comuna,direccion,id_producto,cantidad, estado, fecha,pagado)
		VALUES ('%s','%s','%d','%s','%d','%s','%s','%s','%d','%d','%s','%s','%d') RETURNING id"""%(nombre,apellido,rut,mail,telefono,ciudad,comuna,direccion,id_producto, cantidad, pendiente,fecha,pago)
		cur.execute(sql)
		conn.commit()
		a = cur.fetchall()
		id_caracteristica = a[0][0]

		sql = """INSERT INTO factura (id_compra,img,filename) VALUES ('%d','%s','%s')"""%(id_caracteristica,pic,filename)
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
		sql = """SELECT * FROM compras, producto, caracteristicas_cojin, relleno, tela, imagen, factura WHERE
		compras.rut = '%d' AND compras.id_producto = producto.id AND producto.caracteristicas_id = caracteristicas_cojin.id 
		AND caracteristicas_cojin.id_tela = tela.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id = imagen.id_tela AND compras.id = factura.id_compra;"""%(rut)
		cur.execute(sql)
		compras = cur.fetchall()

		sql = """SELECT * FROM pedidos_usuario, pedido_cojin, tela_armados, relleno, imagen WHERE
		pedidos_usuario.rut = '%d' AND pedidos_usuario.id_pedido_cojin = pedido_cojin.id AND pedido_cojin.id_relleno = relleno.id 
		AND pedido_cojin.id_tela_armados = tela_armados.id AND tela_armados.id = imagen.id_tela;"""%(rut)
		cur.execute(sql)
		pedidos = cur.fetchall()


		return render_template("mis_compras.html",compras=compras,pedidos=pedidos)

	return render_template("mis_compras.html")

@app.route('/miscompras/rut=<rut>/<id>/<id_producto>',methods=['POST','GET'])
def mis_compras_factura(rut,id,id_producto):
	codigo_factura = int(id)
	codigo_producto = id_producto
	
	sql = """SELECT * FROM factura WHERE factura.id_compra = '%d'"""%(codigo_factura)
	cur.execute(sql)
	factura = cur.fetchall()
	data = factura[0]

	print(data)

	return render_template("mis_compras_factura.html",codigo=codigo_factura,codigo2=codigo_producto,datos=data)

@app.route('/armatucojin',methods=['POST','GET'])
def armar_cojin():
	sql = """SELECT * FROM tela_armados, imagen WHERE tela_armados.id = imagen.id_tela;"""
	cur.execute(sql)
	telas = cur.fetchall()

	if request.method == 'POST':
		tela = request.form['tela']
		medida = request.form['medida']
		relleno = request.form['relleno']
		cantidad = request.form['cantidad']

		nombre = request.form['nombre']
		apellido = request.form['apellido']
		rut2 = request.form['rut']
		mail = request.form['mail']
		telefono2 = request.form['telefono']
		ciudad = request.form['ciudad']
		comuna = request.form['comuna']
		direccion = request.form['direccion']
		rut = int(rut2)
		telefono = int(telefono2)
		c = datetime.datetime.now()
		fecha = c.strftime("%x")
		pendiente = "pendiente"

		tela = int(tela)
		cantidad = int(cantidad)
		relleno = int(relleno)
		altura = 0
		ancho = 0
		if medida == "1":
			print("es treinta")
			altura = 30
			ancho = 30
		if medida == "2":
			print("es cincuenta")
			altura = 50
			ancho = 50
		if medida == "3":
			print("es sesenta")
			altura = 60
			ancho = 60

		print(medida)
		print(altura)
		print(ancho)

		sql = """INSERT INTO pedido_cojin (id_relleno,altura,ancho,id_tela_armados)
		VALUES ('%d','%d','%d','%d') RETURNING id;"""%(relleno,altura,ancho,tela)
		cur.execute(sql)
		conn.commit()
		a = cur.fetchall()
		id_pedido = a[0][0]

		sql = """INSERT INTO pedidos_usuario (nombre_comprador, apellido_comprador , rut ,
			mail , telefono , ciudad , comuna , direccion , id_pedido_cojin, cantidad, estado , fecha )
		VALUES ('%s','%s','%d','%s','%d','%s','%s','%s','%d','%d','%s','%s');"""%(nombre,apellido,rut,mail,telefono,ciudad,comuna,direccion,id_pedido,cantidad,pendiente,fecha)
		cur.execute(sql)
		conn.commit()

		return render_template("compra_finalizada.html")

	return render_template("armar_cojin.html",datos=telas)



# DESDE ACA VA LA RESTRICCION DEL LOGIN PARA VER LA VISTA:

@app.route('/administrar',methods=['POST','GET'])
def administrar():
	sql = """SELECT * FROM compras, producto WHERE compras.id_producto = producto.id ORDER BY compras.id desc;"""
	cur.execute(sql)
	datos = cur.fetchall()

	sql = """SELECT * FROM pedidos_usuario, pedido_cojin, tela_armados, relleno WHERE pedidos_usuario.id_pedido_cojin = pedido_cojin.id AND pedido_cojin.id_relleno = relleno.id 
	AND pedido_cojin.id_tela_armados = tela_armados.id;"""
	cur.execute(sql)
	pedidos = cur.fetchall()

	if request.method == 'POST':

		codigo = request.form['codigo_id']
		codigo = int(codigo)
		estado = request.form['estado']
		tipo = request.form['tipo']

		if tipo == 'Cojin Armado':
			if request.form['boton'] == 'Finalizar':
				sql = """UPDATE pedidos_usuario SET estado = '%s' WHERE pedidos_usuario.id = '%d';"""%('confirmado',codigo)
				cur.execute(sql)
				conn.commit()
			if request.form['boton'] == 'Cancelar':
				sql = """UPDATE pedidos_usuario SET estado = '%s' WHERE pedidos_usuario.id = '%d';"""%('cancelado',codigo)
				cur.execute(sql)
				conn.commit()
			if request.form['boton'] == 'Eliminar':
				sql = """DELETE FROM pedidos_usuario WHERE pedidos_usuario.id = '%d' RETURNING id_pedido_cojin;"""%(codigo)
				cur.execute(sql)
				conn.commit()
				a = cur.fetchall()
				id_pedido = a[0][0]

				sql = """DELETE FROM pedido_cojin WHERE pedido_cojin.id = '%d';"""%(id_pedido)
				cur.execute(sql)
				conn.commit()

			sql = """SELECT * FROM compras, producto WHERE compras.id_producto = producto.id ORDER BY compras.id desc;"""
			cur.execute(sql)
			datos = cur.fetchall()

			sql = """SELECT * FROM pedidos_usuario, pedido_cojin, tela_armados, relleno WHERE pedidos_usuario.id_pedido_cojin = pedido_cojin.id AND pedido_cojin.id_relleno = relleno.id 
			AND pedido_cojin.id_tela_armados = tela_armados.id;"""
			cur.execute(sql)
			pedidos = cur.fetchall()

			return render_template("administrar_web.html",datos=datos,pedidos=pedidos)
				

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

			sql = """DELETE FROM factura WHERE factura.id_compra = '%d';"""%(codigo)
			cur.execute(sql)
			conn.commit()

		if request.form['boton'] == 'Eliminar' and estado == 'cancelado':
			sql = """DELETE FROM compras WHERE compras.id = '%d';"""%(codigo)
			cur.execute(sql)
			conn.commit()

			sql = """DELETE FROM factura WHERE factura.id_compra = '%d';"""%(codigo)
			cur.execute(sql)
			conn.commit()

		sql = """SELECT * FROM compras, producto WHERE compras.id_producto = producto.id ORDER BY compras.id desc;"""
		cur.execute(sql)
		datos = cur.fetchall()

		sql = """SELECT * FROM pedidos_usuario, pedido_cojin, tela_armados, relleno WHERE pedidos_usuario.id_pedido_cojin = pedido_cojin.id AND pedido_cojin.id_relleno = relleno.id 
		AND pedido_cojin.id_tela_armados = tela_armados.id;"""
		cur.execute(sql)
		pedidos = cur.fetchall()

		return render_template("administrar_web.html",datos=datos,pedidos=pedidos)
			

	return render_template("administrar_web.html",datos=datos,pedidos=pedidos)

@app.route('/administrar/<id>/<id_producto>',methods=['POST','GET'])
def administrar_factura(id,id_producto):
	codigo_factura = int(id)
	codigo_producto = int(id_producto)
	
	sql = """SELECT * FROM factura WHERE factura.id_compra = '%d'"""%(codigo_factura)
	cur.execute(sql)
	factura = cur.fetchall()
	data1 = factura[0]

	sql = """SELECT * FROM imagen WHERE imagen.id_tela = '%d'"""%(codigo_producto)
	cur.execute(sql)
	factura = cur.fetchall()
	data2 = factura[0]

	return render_template("administrar_factura.html",datos1=data1,datos2=data2)

@app.route('/administrar_cojines',methods=['POST','GET'])
def administrar_cojines():
	sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela,imagen WHERE producto.tipo_producto ='%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id AND caracteristicas_cojin.id = imagen.id_tela ORDER BY producto.id;"""%('cojin')
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

  			sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela,imagen WHERE producto.tipo_producto ='%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id AND caracteristicas_cojin.id = imagen.id_tela ORDER BY producto.id;"""%('cojin')
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

				sql = """DELETE FROM imagen WHERE imagen.id_tela = '%d';"""%(c)
				cur.execute(sql)
				conn.commit()

				sql = """SELECT * FROM producto, caracteristicas_cojin, relleno, tela,imagen WHERE producto.tipo_producto ='%s' AND producto.caracteristicas_id = caracteristicas_cojin.id AND caracteristicas_cojin.id_relleno = relleno.id AND caracteristicas_cojin.id_tela = tela.id AND caracteristicas_cojin.id = imagen.id_tela ORDER BY producto.id;"""%('cojin')
				cur.execute(sql)
				productos = cur.fetchall()

				return render_template("administrar_cojin.html",productos=productos,a=False,b=True)


	return render_template("administrar_cojin.html",productos=productos,a=False,b=False)

@app.route('/administrar_telas',methods=['POST','GET'])
def administrar_telas():

	sql = """SELECT * FROM tela_armados, imagen WHERE tela_armados.id = imagen.id_tela;"""
	cur.execute(sql)
	telas = cur.fetchall()

	if request.method == 'POST':
		nombre = request.form['nombre']
		codigo_id = int(request.form['codigo_id'])
		estado = request.form['estado']
		precio = int(request.form['precio'])

		if request.form['boton'] == 'Guardar':
			sql = """UPDATE tela_armados SET nombre = '%s',precio_metrocuadrado = '%d', estado = '%s' WHERE id = '%d';"""%(nombre,precio,estado,codigo_id)
			cur.execute(sql)
			conn.commit()
			sql = """SELECT * FROM tela_armados, imagen WHERE tela_armados.id = imagen.id_tela;"""
			cur.execute(sql)
			telas = cur.fetchall()
			return render_template("administrar_telas.html",telas=telas,a=True,b=True)
		if request.form['boton'] == 'Eliminar':
			sql = """SELECT * FROM pedido_cojin WHERE pedido_cojin.id_tela_armados = '%s';"""%(codigo_id)
			cur.execute(sql)
			pedidos = cur.fetchall()

			if len(pedidos) > 0:
				return render_template("administrar_telas.html",telas=telas,a=True,b=False)
			else:
				sql = """DELETE FROM tela_armados WHERE tela_armados.id = '%d';"""%(codigo_id)
				cur.execute(sql)
				conn.commit()

				sql = """DELETE FROM imagen WHERE imagen.id_tela = '%d';"""%(codigo_id)
				cur.execute(sql)
				conn.commit()

				sql = """SELECT * FROM tela_armados, imagen WHERE tela_armados.id = imagen.id_tela;"""
				cur.execute(sql)
				telas = cur.fetchall()

				return render_template("administrar_telas.html",telas=telas,a=False,b=True)



	return render_template("administrar_telas.html",telas=telas,a=False,b=False)


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

		pic = request.files['adjunto']
		filename = pic.mimetype
		image_string = base64.b64encode(pic.read())
		pic = image_string.decode()


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

		sql = """INSERT INTO imagen (id_tela,img,filename) VALUES ('%d','%s','%s')"""%(id_caracteristica,pic,filename)
		cur.execute(sql)
		conn.commit()

	return render_template("administrar_crearcojin.html")

@app.route('/ingresar_tela',methods=['POST','GET'])
def ingresar_tela():
	if request.method == 'POST':
		nombre = request.form['nombre']
		precio = int(request.form['precio'])
		estado = "disponible"

		pic = request.files['adjunto']
		filename = pic.mimetype
		image_string = base64.b64encode(pic.read())

		pic = image_string.decode()

		sql = """INSERT INTO tela_armados (nombre,precio_metrocuadrado,estado) VALUES ('%s', '%d','%s') RETURNING id"""%(nombre,precio,estado)
		cur.execute(sql)
		conn.commit()
		a = cur.fetchall()
		id_caracteristica = a[0][0]

		sql = """INSERT INTO imagen (id_tela,img,filename) VALUES ('%d','%s','%s')"""%(id_caracteristica,pic,filename)
		cur.execute(sql)
		conn.commit()

	return render_template("administrar_creartela.html")

