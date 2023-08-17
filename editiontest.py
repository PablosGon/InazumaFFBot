import mysql.connector
from faker import Faker
import random
import openai

openai.api_key = "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"

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb"
)

cursor = conexion.cursor()

# GENERACION DE IMAGEN DE ALGUIEN

def createimage(player):

    cursor.execute("SELECT name FROM team WHERE idteam = " + player[4])
    teamname = cursor.fetchone()

    PROMPT = player[1] + ", " + player[2] + " de " + teamname + ", Inazuma Eleven, anime"

    image = openai.Image.create(prompt="PROMPT", n=1, size="256x256")

# CREACIÓN DE TODOS LOS EQUIPOS

def crearequipos():

    cursor.execute("DELETE FROM player")
    conexion.commit()

    cursor.execute("SELECT * FROM team")
    teams = cursor.fetchall()

    for t in teams:
        
        fake = Faker()
        cursor.execute("INSERT INTO player (name, position, gen, teamid) VALUES ('" + fake.name() + "', 'portero', 20," + str(t[0]) + ")")

        for i in range(4):
            fake = Faker()
            cursor.execute("INSERT INTO player (name, position, gen, teamid) VALUES ('" + fake.name() + "', 'defensa', 20," + str(t[0]) + ")")
            
        for i in range(4):
            fake = Faker()
            cursor.execute("INSERT INTO player (name, position, gen, teamid) VALUES ('" + fake.name() + "', 'centrocampista', 20," + str(t[0]) + ")")

        for i in range(2):
            fake = Faker()
            cursor.execute("INSERT INTO player (name, position, gen, teamid) VALUES ('" + fake.name() + "', 'delantero', 20," + str(t[0]) + ")")

        for i in range(5):
            fake = Faker()
            pos = random.choice(['portero', 'defensa', 'centrocampista', 'delantero'])
            cursor.execute("INSERT INTO player (name, position, gen, teamid) VALUES ('" + fake.name() + "', '" + pos + "', 20," + str(t[0]) + ")")


        print("El equipo " + t[1] + " ha sido creado correctamente")
        conexion.commit()

# SIMULACIÓN DE SIGUIENTE TEMPORADA

def nextgen():

    # AÑO SIGUIENTE

    cursor.execute("SELECT year FROM clock")
    year = cursor.fetchone()[0] + 1
    cursor.execute("UPDATE clock SET year = " + str(year))
    conexion.commit()

    print("NUEVA EDICIÓN " + str(year))

    cursor.execute("SELECT * FROM player WHERE gen = " + str(year - 3))
    resultados = cursor.fetchall()

    for p in resultados:

        position = p[2]
        teamid = p[4]

        fake = Faker()

        cursor.execute("UPDATE player SET teamid = NULL WHERE idplayer = " + str(p[0]))

        # COMPROBAMOS SI HAY JUGADORES QUE VAYAN A ENTRAR

        cursor.execute("SELECT * FROM futureplayer WHERE year = " + str(year) + " AND idteam = + " + str(teamid))
        pending = cursor.fetchall()

        if len(pending) == 0:
            cursor.execute("INSERT INTO player (name, position, gen, teamid) VALUES ('" + fake.name() + "', '" + position + "', " + str(year) + ", " + str(teamid) + ")")
        else:
            cursor.execute("UPDATE player SET teamid = " + str(teamid) + " WHERE idplayer = " + str(pending[0][0]))
        conexion.commit()

        print(p[1] + " se ha graduado y " + fake.name() + " entra al club")

end = False

while(not end):
    action = input()
    if action == "end":
        end = True
    elif action == "next": nextgen()
    elif action == "create": crearequipos()

