import mysql.connector
import random

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb",
    consume_results=True
)

cursor = conexion.cursor()

def eliminar_lineas_duplicadas(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    lineas_unicas = list(set(lineas))
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.writelines(lineas_unicas)

def insertar(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    for l in lineas:
        linea = l.strip()
        print(linea)
        if len(linea) > 2:
            cursor.execute("INSERT INTO supertecnica (name) VALUES ('" + linea + "')")
    
    conexion.commit()

def asignar_supertectnicas():

    cursor.execute("SELECT * FROM player WHERE teamid != 1 AND teamid != 14")
    players = cursor.fetchall()

    cursor.execute("SELECT * FROM supertecnica WHERE tipo = 1")
    ptecnicas = cursor.fetchall()

    cursor.execute("SELECT * FROM supertecnica WHERE tipo = 2")
    btecnicas = cursor.fetchall()

    cursor.execute("SELECT * FROM supertecnica WHERE tipo = 3")
    rtecnicas = cursor.fetchall()

    cursor.execute("SELECT * FROM supertecnica WHERE tipo = 4")
    ttecnicas = cursor.fetchall()

    for p in players:
        
        tecnicas = []

        if p[2] == 1:
            tecnicas.append(random.choice(ptecnicas))
        elif p[2] == 2:
            tecnicas.append(random.choice(btecnicas))
            tecnicas.append(random.choice(rtecnicas))
        elif p[2] == 3:
            tecnicas.append(random.choice(btecnicas))
            tecnicas.append(random.choice(rtecnicas))
            tecnicas.append(random.choice(ttecnicas))
        elif p[2] == 4:
            tecnicas.append(random.choice(rtecnicas))
            tecnicas.append(random.choice(ttecnicas))

        for t in tecnicas:
            cursor.execute("INSERT INTO playertecnica (idplayer, idsupertecnica) VALUES (" + str(p[0]) + ", " + str(t[0]) + ")")
        
    conexion.commit()
