from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))
cur = conn.cursor()
#*********************************************************************************************************
#RELLENOS
sql = """
insert into relleno (tipo_relleno) values
  ('espuma')
returning id;
"""
cur.execute(sql)

sql = """
insert into relleno (tipo_relleno) values
  ('pluma')
returning id;
"""
cur.execute(sql)
#*********************************************************************************************************
#TELAS
sql = """
insert into tela (tipo_tela) values
  ('algodon')
returning id;
"""
cur.execute(sql)

sql = """
insert into tela (tipo_tela) values
  ('lana')
returning id;
"""
cur.execute(sql)

sql = """
insert into tela (tipo_tela) values
  ('seda')
returning id;
"""
cur.execute(sql)

sql = """
insert into tela (tipo_tela) values
  ('poliester')
returning id;
"""
cur.execute(sql)

sql = """
insert into tela (tipo_tela) values
  ('viscosa')
returning id;
"""
cur.execute(sql)
#*********************************************************************************************************
#COJIN 1:

sql = """
insert into caracteristicas_cojin (id_relleno, altura, ancho, id_tela ) values
  ('1','30','30','3')
returning id;
"""
cur.execute(sql)

sql = """
insert into cojines (titulo, caracteristicas_cojin_id, stock, precio_unitario ) values
  ('Cojin de felpa','1','5','5000')
returning id;
"""
cur.execute(sql)

#*********************************************************************************************************
#COJIN 2:

sql = """
insert into caracteristicas_cojin (id_relleno, altura, ancho, id_tela ) values
  ('2','50','50','2')
returning id;
"""
cur.execute(sql)

sql = """
insert into cojines (titulo, caracteristicas_cojin_id, stock, precio_unitario ) values
  ('Cojin Retro','2','3','6500')
returning id;
"""
cur.execute(sql)


conn.commit()
cur.close()
conn.close()
