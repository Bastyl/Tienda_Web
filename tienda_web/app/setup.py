from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()

#ESTADO COMPRAS:
#1 CONFIRMADA
#2 PENDIENTE
#3 CANCELADA

#TIPO PRODUCTO EN PRODUCTO:
#1 cojin
#2 cubrecama
#3 mantel
sql ="""
        DROP TABLE caracteristicas_cojin;
        DROP TABLE relleno;
        DROP TABLE tela;
        DROP TABLE producto;
        DROP TABLE compras;
        DROP TABLE tela_armados;
        DROP TABLE pedidos_usuario;
        DROP TABLE pedido_cojin;
"""

cur.execute(sql)

sql ="""
CREATE TABLE caracteristicas_cojin( id serial PRIMARY KEY, id_relleno integer, altura integer, ancho integer, id_tela integer);
CREATE TABLE relleno (id serial PRIMARY KEY, tipo_relleno varchar);
CREATE TABLE tela (id serial PRIMARY KEY, tipo_tela varchar);
CREATE TABLE producto (id serial PRIMARY KEY, tipo_producto varchar, titulo varchar, caracteristicas_id integer, stock integer, precio_unitario integer);
CREATE TABLE compras (id serial PRIMARY KEY, nombre_comprador varchar, apellido_comprador varchar, rut integer,
	mail varchar, telefono integer, ciudad varchar, comuna varchar, direccion varchar, id_producto integer,cantidad integer, estado varchar, fecha varchar, pagado integer);


CREATE TABLE tela_armados (id serial PRIMARY KEY, nombre varchar, precio_metrocuadrado integer,estado varchar);

CREATE TABLE pedidos_usuario (id serial PRIMARY KEY, nombre_comprador varchar, apellido_comprador varchar, rut integer,
	mail varchar, telefono integer, ciudad varchar, comuna varchar, direccion varchar, id_pedido_cojin integer,cantidad integer, estado varchar, fecha varchar);

CREATE TABLE pedido_cojin (id serial PRIMARY KEY, id_relleno integer, altura integer, ancho integer, id_tela_armados integer);

"""

cur.execute(sql)
conn.commit()
cur.close()
conn.close()
