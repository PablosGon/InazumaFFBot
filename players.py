import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb"
)

cursor = conexion.cursor()

cursor.execute("SELECT name FROM player WHERE teamid = 5")
resultados = cursor.fetchall()

for fila in resultados:
    print(fila)