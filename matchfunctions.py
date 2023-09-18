import mysql.connector
import random
import time
import openai

t = 0

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

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid) + " AND position = 1")
    resultados = cursor.fetchall()
    gkp = []
    for r in resultados:
        if r[4] == 1:
            gkp.append(pTitular)
        else: gkp.append(1 - pTitular)
    gk = random.sample(resultados, k=1)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid) + " AND position = 2")
    resultados = cursor.fetchall()
    df = random.sample(resultados, k=4)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid) + " AND position = 3")
    resultados = cursor.fetchall()
    md = random.sample(resultados, k=4)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid) + " AND position = 4")
    resultados = cursor.fetchall()
    dl = random.sample(resultados, k=2)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(teamid))
    resultados = cursor.fetchall()
    banquillo = set(resultados) - set(gk) - set(md) - set(df) - set(dl)

    for p in list(set(resultados) - banquillo):
        cursor.execute("UPDATE player SET titular = 1 WHERE idplayer = " + str(p[0]))
    
    conexion.commit()

    return gk, df, md, dl, banquillo

def printOnceInicial(gk, df, md, dl, b, team):
    print("¡El once inicial de " + team[1] + " es el siguiente!\n")
    print("PORTERO")
    print(gk[0][1] + "\n")
    print("DEFENSAS")
    for d in df:
        print(d[1])
    print("\nMEDIO CAMPO")
    for m in md:
        print(m[1])
    print("\nDELANTEROS")
    for d in dl:
        print(d[1])
    print("\nBANQUILLO")
    for ba in b:
        print(ba[1])

    print("\n")
# DECIDIMOS SAQUE

def saqueInicial(dl1, dl2, match):
    n = random.random()
    if n < 0.5:
        saqueid = dl1[0][0]
        saqueid2 = dl2[0][0]
    else:
        saqueid = dl2[0][0]
        saqueid2 = dl1[0][0]
    cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(saqueid) + " WHERE idmatch = " + str(match[0]))
    conexion.commit()

    return saqueid2

# COMIENZA EL PARTIDO

def comenzarPartido(match):
    cursor.execute("UPDATE inazumadb.match SET started = 1 WHERE idmatch = " + str(match[0]))
    conexion.commit()
    print("¡COMIENZA EL PARTIDO!\n")

def refrescarPartido(match):
    cursor.execute("SELECT * FROM inazumadb.match WHERE idmatch = " + str(match[0]))
    match = cursor.fetchone()
    return match

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

def possesionTeam(match):
    
    cursor.execute("SELECT * FROM team WHERE idteam = (SELECT teamid FROM player WHERE idplayer = " + str(match[8]) + ")")
    return cursor.fetchone()

def advOf(player, match):

    if player[4] == match[1]:
        return match[2]
    elif player[4] == match[2]: 
        return match[1]
    else: 
        print("ERROR: No se pudo encontrar el equipo adversario de " + player[1])
        return -1

def passTo(player, match, lf):

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(player[4]) + " AND position = " + str(player[2]) + " AND idplayer != " + str(player[0]) + "  AND titular = 1")

    receiver = random.choice(cursor.fetchall())

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(advOf(player, match)) + " AND position = " + str(player[2] - lf) + " AND titular = 1")
    advs = cursor.fetchall()

    exito = True

    if len(advs) != 0:
        adv = random.choice(advs)
        r = random.random()
        if r < 0.2:
            exito = False

    if exito:
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(receiver[0]) + " WHERE idmatch = " + str(match[0]))
        print("¡" + getNPT(player) + ", le pasa el balón a " + getNPT(receiver) + "!")
    else:
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(adv[0]) + " WHERE idmatch = " + str(match[0]))
        print("¡" + getNPT(adv) + ", corta el pase de " + getNPT(player) + "!")


    if lf < 4:
        linea = lf + 1
    else: linea = 4

    conexion.commit()
    
    return linea

def passForwardTo(player, match, lf):

    forward = player[2] + 1

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(player[4]) + " AND position = " + str(forward) + " AND idplayer != " + str(player[0]) + " AND titular = 1")
    receiver = random.choice(cursor.fetchall())

    advpos = 9 - lf - player[2]

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(advOf(player, match)) + " AND position = " + str(advpos) + " AND titular = 1")
    advs = cursor.fetchall()

    exito = True

    if len(advs) != 0:
        adv = random.choice(advs)
        r = random.random()
        if r < 0.2:
            exito = False

    if exito:
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(receiver[0]) + " WHERE idmatch = " + str(match[0]))
        print("¡" + getNPT(player) + ", le pasa el balón a " + getNPT(receiver) + "!")
    else:
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(adv[0]) + " WHERE idmatch = " + str(match[0]))
        print("¡" + getNPT(adv) + ", corta el pase adelante de " + getNPT(player) + "!")

    cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(receiver[0]) + " WHERE idmatch = " + str(match[0]))
    conexion.commit()


def passBackwardsTo(player, match, lf):

    forward = player[2] - 1

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(player[4]) + " AND position = " + str(forward) + " AND idplayer != " + str(player[0]) + " AND titular = 1")
    receiver = random.choice(cursor.fetchall())

    advpos = 7 - lf - player[2]

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(advOf(player, match)) + " AND position = " + str(advpos) + " AND titular = 1")
    advs = cursor.fetchall()

    exito = True

    if len(advs) != 0:
        adv = random.choice(advs)
        r = random.random()
        if r < 0.2:
            exito = False

    if exito:
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(receiver[0]) + " WHERE idmatch = " + str(match[0]))
        print("¡" + getNPT(player) + ", da un pase atrás a " + getNPT(receiver) + "!")
    else:
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(adv[0]) + " WHERE idmatch = " + str(match[0]))
        print("¡" + getNPT(adv) + ", corta el pase atrás de " + getNPT(player) + "!")

    cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(receiver[0]) + " WHERE idmatch = " + str(match[0]))
    conexion.commit()

def regatear(player, match, idt1, idt2, lf):
    
    if player[4] == idt1:
        idt = idt2
    else: idt = idt1

    advpos = 8 - lf - player[2]

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(idt) + " AND position = " + str(advpos) + " AND titular = 1")
    advs = cursor.fetchall()
    adv = random.choice(advs)

    probmatrix = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0.6, 0.5, 0.4],
                 [0, 0.8, 0.5, 0.4, 0],
                 [0.5, 0.4, 0.3, 0, 0]]
    
    pe = probmatrix[player[2]][lf]

    r = random.random()
    if r < pe:
        exito = True
    else: exito = False

    if getSupertecnica(player, 3) != None: 
        print("¡" + getNPT(player) + ", va a intentar regatear a " + adv[1] + " con " + getSupertecnica(player, 3) + "!")
        time.sleep(t)
    if getSupertecnica(adv, 2) != None: 
        print("¡" + getNPT(adv) + ", intenta pararlo con " + getSupertecnica(adv, 2) + "!")
        time.sleep(t)

    if exito:
        print("¡" + getNPT(player) + ", regatea a " + adv[1] + " con éxito! (" + str(pe) + ")")
    else:
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(adv[0]) + " WHERE idmatch = " + str(match[0]))
        print("¡" + getNPT(adv) + ", le roba el balón a " + player[1] + "!")

    if lf < 4:
        linea = lf + 1
    else: linea = lf
    
    return linea

def tiro(player, match, idt1, idt2, lf):
    print("¡" + getNPT(player) + ", va a tirar a puerta!")
    time.sleep(t)
    print("¡" + player[1] + " ha usado " + getSupertecnica(player, 4) + "!")
    time.sleep(t)

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(advOf(player, match)) + " AND position = 1 AND titular = 1")
    gk = cursor.fetchone()

    print("¡" + getNPT(gk) + " intenta detenerlo con " + getSupertecnica(gk, 1) + "!")
    time.sleep(t)

    r = random.random()
    if r <= (0.15*lf):
        print("¡GOOOL!")
        if player[4] == idt1:
            cursor.execute("SELECT score1 FROM inazumadb.match WHERE idmatch = " + str(match[0]))
            score1 = cursor.fetchone()[0] + 1
            cursor.execute("UPDATE inazumadb.match SET score1 = " + str(score1) + " WHERE idmatch = " + str(match[0]))
        else: 
            cursor.execute("SELECT score2 FROM inazumadb.match WHERE idmatch = " + str(match[0]))
            score2 = cursor.fetchone()[0] + 1
            cursor.execute("UPDATE inazumadb.match SET score2 = " + str(score2) + " WHERE idmatch = " + str(match[0]))
        linea = 0
        cursor.execute("SELECT * FROM player WHERE teamid = " + str(advOf(player, match)) + " AND position = 4 AND titular = 1")
        saque = random.choice(cursor.fetchall())
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(saque[0]) + " WHERE idmatch = " + str(match[0]))

    else:
        print("¡" + gk[1] + " lo ha detenido!")
        linea = 2
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(gk[0]) + " WHERE idmatch = " + str(match[0]))
    
    conexion.commit()

    return linea

def getSupertecnica(player, type):

    cursor.execute("SELECT supertecnica.name FROM playertecnica inner join supertecnica on playertecnica.idsupertecnica = supertecnica.idsupertecnica where playertecnica.idplayer = " +  str(player[0]) + " and supertecnica.tipo = " + str(type))
    result = cursor.fetchall()

    if len(result) == 0:
        return None
    else: return result[0][0]

def getNPT(player):

    if player[2] == 1:
        pos = "portero"
    elif player[2] == 2:
        pos = "defensa"
    elif player[2] == 3:
        pos = "centrocampista"
    else: pos = "delantero"

    cursor.execute("SELECT name FROM team WHERE idteam = " + str(player[4]))
    teamname = cursor.fetchone()[0]

    return player[1] + ", " + pos + " de " + teamname



def decide(match, idt1, idt2, lf):

    cursor.execute("SELECT * FROM player WHERE idplayer = (SELECT idplayerwithball FROM inazumadb.match WHERE idmatch = " + str(match[0]) + ")")
    player = cursor.fetchone()

    shootmatrix = [[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0.1, 0.2, 0.4],
                   [0, 0.1, 0.4, 1, 1]]
    driblematrix = [[0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0.4, 0.25, 0.1],
                    [0, 0.3, 0.4, 0.3, 0],
                    [0.3, 0.3, 0.25, 0, 0]]
    passmatrix = [[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0.7, 0.5, 0.3, 0.25, 0.2],
                  [0.5, 0.3, 0.2, 0.2, 0, 0],
                  [0.3, 0.3, 0.25, 0, 0]]
    backpassmatrix = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0.3, 0.2, 0.1, 0, 0],
                      [0.4, 0.3, 0.1, 0, 0]]
    passforwardmatrix = [[0, 0, 0, 0, 0],
                         [1, 1, 1, 1, 1],
                         [0.3, 0.5, 0.3, 0.5, 0.7],
                         [0.2, 0.2, 0.2, 0.3, 0.6],
                         [0, 0, 0, 0, 0]]

    decmatrix = [shootmatrix, driblematrix, passmatrix, backpassmatrix, passforwardmatrix]

    for i in [2, 3, 4]:
        for j in range(5):
            if shootmatrix[i][j] + driblematrix[i][j] + passmatrix[i][j] + backpassmatrix[i][j] + passforwardmatrix[i][j] != 1:
                print("AVISO: error en las coordenadas (" + str(i) + ", " + str(j) + ")")

    linea = lf

    r = random.random()
    if r < shootmatrix[player[2]][lf]:
        linea = tiro(player, match, idt1, idt2, lf)
    elif r < shootmatrix[player[2]][lf] + driblematrix[player[2]][lf]:
        linea = regatear(player, match, idt1, idt2, lf)
    elif r < shootmatrix[player[2]][lf] + driblematrix[player[2]][lf] + passmatrix[player[2]][lf]:
        linea = passTo(player, match, lf)
    elif r < shootmatrix[player[2]][lf] + driblematrix[player[2]][lf] + passmatrix[player[2]][lf] + backpassmatrix[player[2]][lf]:
        passBackwardsTo(player, match, lf)
    else: passForwardTo(player, match, lf)



    return linea
