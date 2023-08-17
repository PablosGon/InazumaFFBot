import mysql.connector
import random

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

# GENERACION DE IMAGEN DE ALGUIEN

def createimage(player):

    cursor.execute("SELECT name FROM team WHERE idteam = " + str(player[4]))
    teamname = cursor.fetchone()[0]

    PROMPT = player[1] + ", " + player[2] + " de " + teamname + ", Inazuma Eleven, anime"

    print("Se va a generar una imagen que de " + PROMPT)

    seguir = False

    while(not seguir):
        action = input()
        seguir = True

    image = openai.Image.create(prompt=PROMPT, n=1, size="256x256")
    print("La imagen de " + player[1] + " es: " + image["data"][0]["url"])

cursor.execute("SELECT * FROM team")

resultados = cursor.fetchall()

team1 = resultados[0]
team2 = resultados[4]

def crearPartido(team1, team2):

    cursor.execute("UPDATE player SET titular = 0 WHERE teamid = " + str(team1[0]) + " OR teamid = " + str(team2[0]))
    cursor.execute("INSERT INTO inazumadb.match (idteam1, idteam2) VALUES ( " + str(team1[0]) + ", " + str(team2[0]) + ")")
    conexion.commit()
    cursor.execute("SELECT * FROM inazumadb.match WHERE idmatch = (SELECT MAX(idmatch) FROM inazumadb.match)")
    match = cursor.fetchone()
    print("¡Se van a enfrentar " + team1[1] + " contra " + team2[1] + "!")
    return match

def onceinicial(teamid):

    pTitular = 0.8

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid) + " AND position = 'portero'")
    resultados = cursor.fetchall()
    gkp = []
    for r in resultados:
        if r[4] == 1:
            gkp.append(pTitular)
        else: gkp.append(1 - pTitular)
    gk = random.sample(resultados, k=1)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid) + " AND position = 'defensa'")
    resultados = cursor.fetchall()
    df = random.sample(resultados, k=4)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid) + " AND position = 'centrocampista'")
    resultados = cursor.fetchall()
    md = random.sample(resultados, k=4)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid) + " AND position = 'delantero'")
    resultados = cursor.fetchall()
    dl = random.sample(resultados, k=2)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid))
    resultados = cursor.fetchall()
    banquillo = set(resultados) - set(gk) - set(md) - set(df) - set(dl)

    for p in list(set(resultados) - banquillo):
        cursor.execute("UPDATE player SET titular = 1 WHERE idplayer = " + str(p[0]))
    
    conexion.commit()

    return gk, df, md, dl, banquillo

match = crearPartido(team1, team2)
print(match)

# DECIDIMOS EL ONCE INICIAL DE TEAM1

gk1, df1, md1, dl1, b1 = onceinicial(team1[0])

print("¡El once inicial de " + team1[1] + " es el siguiente!\n")
print("PORTERO")
print(gk1[0][1] + "\n")
print("DEFENSAS")
for d in df1:
    print(d[1])
print("\nMEDIO CAMPO")
for m in md1:
    print(m[1])
print("\nDELANTEROS")
for d in dl1:
    print(d[1])
print("\nBANQUILLO")
for ba in b1:
    print(ba[1])

print("\n")

# DECIDIMOS EL ONCE INICIAL DE TEAM2

gk2, df2, md2, dl2, b2 = onceinicial(team2[0])

print("¡El once inicial de " + team2[1] + " es el siguiente!\n")
print("PORTERO")
print(gk2[0][1] + "\n")
print("DEFENSAS")
for d in df2:
    print(d[1])
print("\nMEDIO CAMPO")
for m in md2:
    print(m[1])
print("\nDELANTEROS")
for d in dl2:
    print(d[1])
print("\nBANQUILLO")
for ba in b2:
    print(ba[1])

# DECIDIMOS SAQUE

def saqueInicial(dl1, dl2, match):
    n = random.random()
    if n < 0.5:
        saqueid = dl1[0][0]
    else: saqueid = dl2[0][0]
    cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(saqueid) + " WHERE idmatch = " + str(match[0]))
    conexion.commit()

# COMIENZA EL PARTIDO

def comenzarPartido(match):
    cursor.execute("UPDATE inazumadb.match SET started = 1 WHERE idmatch = " + str(match[0]))
    conexion.commit()
    print("¡COMIENZA EL PARTIDO!\n")

saqueInicial(dl1, dl2, match)
comenzarPartido(match)

cursor.execute("SELECT * FROM inazumadb.match WHERE idmatch = (SELECT MAX(idmatch) FROM inazumadb.match)")
match = cursor.fetchone()


ended = False

players1 = [gk1, df1, md1, dl1]
players2 = [gk2, df2, md2, dl2]


def selectscorer(team):

    r = random.random()

    if r <= 0.6:
        scorer = random.choice(team[3])
    elif r <= 0.95:
        scorer = random.choice(team[2])
    elif r <= 0.99:
        scorer = random.choice(team[1])
    else: scorer = random.choice(team[0])

    return scorer

def passTo():
    
    print(match)

    cursor.execute("SELECT * FROM player WHERE idplayer = (SELECT idplayerwithball FROM inazumadb.match WHERE idmatch = (SELECT MAX(idmatch) FROM inazumadb.match))")
    player = cursor.fetchone()

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(player[4]) + " AND position = '" + player[2] + "' AND idplayer != " + str(player[0]) + "  AND titular = 1")

    receiver = random.choice(cursor.fetchall())

    cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(receiver[0]) + " WHERE idmatch = " + str(match[0]))
    conexion.commit()
    
    print("¡" + player[1] + " le pasa el balón a " + receiver[1] + "!")

def passForwardTo():

    print(match)

    cursor.execute("SELECT * FROM player WHERE idplayer = (SELECT idplayerwithball FROM inazumadb.match WHERE idmatch = (SELECT MAX(idmatch) FROM inazumadb.match))")
    player = cursor.fetchone()

    if player[2] == "portero":
        forward = "defensa"
    elif player[2] == "defensa":
        forward = "centrocampista"
    else: forward = "delantero"

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(player[4]) + " AND position = '" + forward + "' AND idplayer != " + str(player[0]))
    receiver = random.choice(cursor.fetchall())

    match[8] = receiver[0]
    cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(receiver[0]) + " WHERE idmatch = " + str(match[0]))
    cursor.commit()

def passBackwardsTo():

    print(match)

    cursor.execute("SELECT * FROM player WHERE idplayer = (SELECT idplayerwithball FROM inazumadb.match WHERE idmatch = (SELECT MAX(idmatch) FROM inazumadb.match))")
    player = cursor.fetchone()

    if player[2] == "centrocampista":
        forward = "defensa"
    elif player[2] == "delantero":
        forward = "centrocampista"
    else: forward = "portero"

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(player[4]) + " AND position = '" + forward + "' AND idplayer != " + str(player[0]))
    receiver = random.choice(cursor.fetchall())

    match[8] = receiver[0]
    cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(receiver[0]) + " WHERE idmatch = " + str(match[0]))
    cursor.commit()

def decide():
    r = random.random()
    if r < 1:
        passTo()
        formacion = formacion + 1
    elif r < 0.5:
        passForwardTo()
    else: print("Regate")

while(not ended):
    action = input()
    if action == "end":
        ended = True
    elif action == "pass":
        passTo()
    elif action == "next":
        decide()



def xd():
    action = input()

    if action == "end":
        ended = True
    elif action == "g1":
        scorer = selectscorer(players1)
        score1 = score1 + 1
        print("¡Gol de " + team1[1] + " por parte de " + scorer[1] + "!")
    elif action == "g2":
        scorer = selectscorer(players2)
        score2 = score2 + 1
        print("¡Gol de " + team2[1] + " por parte de " + scorer[1] + "!")
    elif action == "c1":
        playerin = random.choice(list(b1))
        position = playerin[2]
        playerout = ""
        if position == "dl":
            playerout = random.choice(dl1)
            dl1.remove(playerout)
            dl1.append(playerin)
        print("¡Cambio en " + team1[1] + "! ¡Entra " + playerin[1] + " sustituyendo a " + playerout[1] + "!")
    elif action == "i1":
        print("ID:")
        id = input()
        cursor.execute("SELECT * FROM player WHERE idplayer = " + id)
        player = cursor.fetchone()
        print(player)
        createimage(player)
