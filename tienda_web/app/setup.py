from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()

sql ="""
        DROP TABLE cojines;
        DROP TABLE caracteristicas_cojin;
        DROP TABLE relleno;
        DROP TABLE tela;
"""

cur.execute(sql)

sql ="""
CREATE TABLE cojines (id serial PRIMARY KEY, titulo varchar, caracteristicas_cojin_id integer, stock integer, precio_unitario integer);
CREATE TABLE caracteristicas_cojin( id serial PRIMARY KEY, id_relleno integer, altura integer, ancho integer, id_tela integer);
CREATE TABLE relleno (id serial PRIMARY KEY, tipo_relleno varchar);
CREATE TABLE tela (id serial PRIMARY KEY, tipo_tela varchar);
"""

cur.execute(sql)
conn.commit()
cur.close()
conn.close()
