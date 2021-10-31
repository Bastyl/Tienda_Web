from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()

sql ="""DROP TABLE DELINCUENTES;
        DROP TABLE CARACTERISTICAS;
        DROP TABLE HISTORIAL;
"""

cur.execute(sql)

sql ="""
CREATE TABLE delincuentes (id serial PRIMARY KEY, rut integer, nombre varchar, apellido_paterno varchar, apellido_materno varchar, edad integer);
CREATE TABLE caracteristicas (id serial PRIMARY KEY, usuario_id integer, sexo varchar, estatura integer, contextura_fisica varchar,tez_piel varchar, nacionalidad varchar, tono_voz varchar,color_pelo varchar,color_ojos varchar,tatuaje_cara bit,tatuaje_torso bit,tatuaje_brazos bit,tatuaje_piernas bit);
CREATE TABLE historial(id serial PRIMARY KEY, usuario_id integer, sector varchar, relato text, fecha date, hora time);
"""



cur.execute(sql)
conn.commit()
cur.close()
conn.close()
