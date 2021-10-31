from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()

#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('190323323','alexis','sanchez','sanchez','29')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('1','masculino','169','atletica','bronceada','chilena','grave','negro','negros','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('1','La reina','asalto a mano armada','2018-02-02','00:00:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('1813291329','gazzy','garcia','garcia','17')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('2','masculino','171','ancha','clara','extranjera','medio','tinturado','negros','1','1','1','1')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('2','Conchali ','asalto a mano armada con pistola','2018-02-02','00:00:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('2013231319','lionel','messi','cuccittini','31')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('3','masculino','170','atletica','clara','extranjera','medio','castaño','negros','0','0','1','1')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('3','El bosque','Me asaltó cuando fuí a un negocio a comprar','2018-03-02','23:01:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('291300913','cristiano','ronaldo','ronaldo','33')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('4','masculino','185','atletica','bronceada','extranjera','grave','negro','negros','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('4','Cerrillos ','Portonazo en lo prado en la tarde','2018-04-22','18:00:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('12312313','peter','dinklage','dinklage','49')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('5','masculino','141','ancha','clara','extranjera','grave','castaño','verdes','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('5','La florida','Lanza en sector de la florida, calle santa ines','2018-02-19','12:50:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************

#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('1200032130','arturo','vidal','pardo','31')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('6','masculino','180','atletica','bronceada','chilena','aguda','negro','negros','0','1','1','1')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('6','La florida','Robo una bicicleta en sector sur de la florida','2018-07-14','23:50:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('11323130','nicole','evangeline','lilly','38')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('7','femenino','168','delgada','clara','extranjera','aguda','castaño','verdes','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('7','La florida','me asalto con un cuchillo un viernes en la florida','2018-04-24','19:50:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('1132323545','natalie','portman','portman','37')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('8','femenino','160','delgada','clara','extranjera','aguda','castaño','negros','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('8','El bosque','me intento asaltar pero me resisti peligrosa','2017-04-24','13:50:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('0011101013','krysten','alyce','ritter','36')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('9','femenino','175','delgada','palida','extranjera','aguda','negro','negros','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('9','Macul ','La vi robando en el metro cerca de metro macul','2016-02-21','15:50:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('10101010','kaya','rose','humphrey','26')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('10','femenino','168','delgada','clara','extranjera','aguda','castaño','azules','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('10','Macul ','La vi en el metro macul junto con otra persona robando','2014-01-11','18:40:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('9999990','abbey','lee','kershaw','31')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('11','femenino','181','delgada','palida','extranjera','aguda','rubio','azules','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('11','Lo prado','Se junta en las afueras de Lo prado a asaltar a la gente','2013-11-11','14:43:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************
#*********************************************************************************************************
sql = """
insert into delincuentes (rut,nombre,apellido_paterno,apellido_materno,edad) values
 ('888120390','sarah','mcdaniel','mcdaniel','23')
returning id;
"""
cur.execute(sql)

sql = """
insert into CARACTERISTICAS (usuario_id,sexo,estatura,contextura_fisica,
           tez_piel,nacionalidad,tono_voz,color_pelo,color_ojos,tatuaje_cara,tatuaje_torso,tatuaje_brazos,tatuaje_piernas) values
           ('12','femenino','178','delgada','clara','extranjera','aguda','castaño','azules','0','0','0','0')
returning id;
"""

cur.execute(sql)

sql = """
insert into HISTORIAL (usuario_id, sector, relato, fecha, hora) values
 ('12','Lo prado','Me abrio la mochila en la micro en la comuna de lo prado','2017-10-11','19:50:00')
 returning id;
 """
cur.execute(sql)
#*********************************************************************************************************


















conn.commit()
cur.close()
conn.close()
