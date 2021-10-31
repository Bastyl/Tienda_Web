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
		tono = request.args.get('tono')

		char0 = """SELECT delincuentes FROM delincuentes,caracteristicas WHERE estatura BETWEEN '%d' AND '%d' AND sexo = '%s' AND delincuentes.id = caracteristicas.usuario_id"""
		end = ";"

		#tatuajes:
		if tat1 == "cara":
			chartat1 = "AND tatuaje_cara = '1' "
		if tat2 == "torso":
			chartat2 = "AND tatuaje_torso = '1' "
		if tat3 == "brazos":
			chartat3 = "AND tatuaje_brazos = '1' "
		if tat4 == "piernas":
			chartat4 = "AND tatuaje_piernas = '1' "

		char0 = char0 + chartat1 + chartat2 + chartat3 + chartat4

		char1 = "tez_piel = '%s' AND"
		char2 = "nacionalidad = '%s' AND"
		char3 = "color_ojos = '%s' AND"
		char4 = "color_pelo = '%s' AND"
		char5 = "tono_voz = '%s' "

		if piel == "":
			char1 = "AND tez_piel != '%s' "
		if nacionalidad == "":
			char2 = "AND nacionalidad != '%s'"
		if ojos == "":
			char3 = "AND color_ojos != '%s'"
		if pelo == "":
			char4 = "AND color_pelo != '%s'"
		if tono == "":
			char5 = "AND tono_voz != '%s' "

		sql = char0+char1+char2+char3+char4+char5+end %(min,max,sexo,piel,nacionalidad,ojos,pelo,tono)
		cur.execute(sql)
		sospechosos1 = cur.fetchall()

		sql = char0+char1+char2+char3+char4+end %(min,max,sexo,piel,nacionalidad,ojos)
		cur.execute(sql)
		sospechosos2 = cur.fetchall()

		sql = char0+char1+char2+char3+end %(min,max,sexo,piel,nacionalidad,ojos,)
		cur.execute(sql)
		sospechosos3 = cur.fetchall()

		sql = char0+char1+char2+end %(min,max,sexo,piel,nacionalidad)
		cur.execute(sql)
		sospechosos4 = cur.fetchall()

		sql = char0+char1+end %(min,max,sexo,piel)
		cur.execute(sql)
		sospechosos5 = cur.fetchall()

		sql = char0+end %(min,max,sexo)
		cur.execute(sql)
		sospechosos6 = cur.fetchall()

		sospechosos = sospechosos1 + sospechosos2 + sospechosos3 + sospechosos4 + sospechosos5 + sospechosos6

		lista_final = []
		for i in sospechosos:
			if i not in lista_final:
				lista_final.append(i)

		return lista(lista_final)

	return render_template("buscar_delincuente.html")

###################################################################################################
