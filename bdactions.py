import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb",
    consume_results=True
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM player")
resultados = cursor.fetchall()

for p in resultados:
    
    if p[2] == 0: id = 1
    elif p[2] == 1: id = 2
    elif p[2] == 2: id = 3
    elif p[2] == 3: id = 4

    cursor.execute("UPDATE player SET position = '" + str(id) + "' WHERE idplayer = " + str(p[0]))

sure = False
print("Estás seguro?")
while(not sure):
    if input() == "Sí": sure = True

conexion.commit()