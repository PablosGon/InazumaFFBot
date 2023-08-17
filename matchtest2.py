import mysql.connector
import random
import matchfunctions
import time

import openai

openai.api_key = "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"

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb",
    consume_results=True
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM team")

resultados = cursor.fetchall()

team1 = resultados[0]
team2 = resultados[13]

match = matchfunctions.crearPartido(team1, team2)
print(match)

# DECIDIMOS EL ONCE INICIAL DE TEAM1

gk1, df1, md1, dl1, b1 = matchfunctions.onceinicial(team1[0])
matchfunctions.printOnceInicial(gk1, df1, md1, dl1, b1, team1)

# DECIDIMOS EL ONCE INICIAL DE TEAM2

gk2, df2, md2, dl2, b2 = matchfunctions.onceinicial(team2[0])
matchfunctions.printOnceInicial(gk2, df2, md2, dl2, b2, team2)

matchfunctions.saqueInicial(dl1, dl2, match)
matchfunctions.comenzarPartido(match)

match = matchfunctions.refrescarPartido()

lineaformacion = 0

ended = False

players1 = [gk1, df1, md1, dl1]
players2 = [gk2, df2, md2, dl2]

while(not ended):
    action = input()
    if action == "end":
        ended = True
    elif action == "pass":
        matchfunctions.passTo(match)
    elif action == "next":
        lineaformacion = matchfunctions.decide(match, team1[0], team2[0], lineaformacion)
    elif action == "regate":
        lineaformacion = matchfunctions.regatear(match, team1[0], team2[0], lineaformacion)
    elif action == "avanza":
        lineaformacion = lineaformacion + 1
    elif action == "play":
        for i in range(45):
            lineaformacion = matchfunctions.decide(match, team1[0], team2[0], lineaformacion)
            time.sleep(0)
            match = matchfunctions.refrescarPartido()
            print("¡Balón para " + matchfunctions.possesionTeam(match)[1] + "! (" + str(lineaformacion) + ")")
            time.sleep(0)
        print("Termina la primera parte!\n" + team1[1] + " " + str(match[4]) + " - " + str(match[5]) + " " + team2[1])


    match = matchfunctions.refrescarPartido()

    print(matchfunctions.possesionTeam(match))

    print("¡Balón para " + matchfunctions.possesionTeam(match)[1] + "! (" + str(lineaformacion) + ")")