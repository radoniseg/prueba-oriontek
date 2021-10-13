import sqlite3

#CONEXION A LA BASE DE DATOS
def conexion_db():
	conn = sqlite3.connect("oriontek.db")
	cursor = conn.cursor()

#CREACION DE TABLAS CLIENTES
	try:
		cursor.execute('''
			CREATE TABLE clientes(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			nombre VARCHAR(75) UNIQUE NOT NULL
			)
			''')
	except sqlite3.OperationalError:
		print("tabla existe!")
	else:
		print("tabla Creada!")

#CREACION DE TABLAS DIRECCION
	try:	
		cursor.execute('''
			CREATE TABLE direccion(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			calle VARCHAR(50) NOT NULL,
			numero INTEGER,
			sector VARCHAR (50) NOT NULL, 
			provincia VARCHAR (50) NOT NULL,
			id_cliente INTEGER NOT NULL,
			FOREIGN KEY (id_cliente) REFERENCES clientes(id)
			)
			''')
	except sqlite3.OperationalError:
		print("tabla existe!")
	else:
		print("tabla Creada!") 

#FUNCION PARA CAPTURAR LOS CLIENTES
def clientes():

	cliente = input("Nombre del cliente: ")

	conn = sqlite3.connect("oriontek.db")
	cursor = conn.cursor()

	try:
		cursor.execute("INSERT INTO clientes VALUES(NULL, '{}')".format(cliente))
	except sqlite3.IntegrityError:
		print("Cliente '{}' ya existe!".format(cliente))
	else:
		print("cliente '{}' Creado!".format(cliente))
		
	conn.commit()
	conn.close()

#FUNCION PARA CAPTURAR LAS DIRECCIONES
def direcciones():

	conn = sqlite3.connect("oriontek.db")
	cursor = conn.cursor()

	cliente = cursor.execute("SELECT * FROM clientes").fetchall()
	print("Seleccione el cliente:")
	for c in cliente:
		print("[{}] {}".format(c[0], c[1]))

	clientes_s = int(input("Opcion="))

	calle = input("Calle: ")

	numero = int(input("numero:"))
	sector = input("Sector: ")
	provincia = input("provincia: ")

	try:
		cursor.execute("INSERT INTO direccion VALUES(NULL, '{}','{}','{}','{}','{}')".format(calle,numero,sector,provincia,clientes_s))
	except sqlite3.IntegrityError:
		print("Direccion '{}' ya existe!".format(calle))
	else:
		print("Direccion '{}' Creado!".format(calle))
		
	conn.commit()
	conn.close()
 
#CONSULTAS
def consulta():

	conn = sqlite3.connect("oriontek.db")
	cursor = conn.cursor()

	consulta_c = input("""CONSULTAR CLIENTE \n
	ID: """)
	cliente = cursor.execute("SELECT * FROM clientes WHERE id={}".format(consulta_c)).fetchone()
	consulta_id= cliente
	print("Direcciones de '{}'".format(consulta_id))

	consulta_d  = cursor.execute("SELECT * FROM direccion WHERE id_cliente={}".format(consulta_id[0])).fetchall()
	for c in consulta_d:
		print("{}".format(c))

	conn.close()


conexion_db()

#MENU PARA DIRECCIONES
def menu_d():

	while True:
		print("""
			AGREGAR DIRECCION

			OPCIONES
			[1]Agragar direccion
			[2]Consultar direciones
			[3]salir
			""")

		opcion = input("opcion>")

		if opcion == "1":
			direcciones()

		elif opcion == "2":
			consulta()

		elif opcion == "3":
			break
		else:
			print("Opcion incorecta")

#MENU PARA CLIENTES
def menu_c():

	while True:
		print("""
			REGISTRO DE CLIENTES

			OPCIONES
			[1]registrar clientes
			[2]consultar clientes
			[3]salir
			""")

		opcion = input("opcion>")

		if opcion == "1":
			clientes()
			
		elif opcion == "2":
			menu_d()

		elif opcion == "3":
			break
		else:
			print("Opcion incorecta")

menu_c()
