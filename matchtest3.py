import mysql.connector
import random
import matchfunctions
import time
import tweepy
import bdactions3

with open("C:/Users/pablo/OneDrive/Proyectos Personales/InazumaBot/keys/twitterkeys.txt", 'r', encoding='utf-8') as f:
    lineas = f.readlines()

client = tweepy.Client(consumer_key=lineas[0].split()[0],
                    consumer_secret=lineas[1].split()[0],
                    access_token=lineas[2].split()[0],
                    access_token_secret=lineas[3].split()[0],
                    bearer_token=lineas[4].split()[0])
# Replace the text with whatever you want to Tweet about

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb",
    consume_results=True
)

cursor = conexion.cursor()

def print_jugadores(players):

    out = players[0][1]
    if len(players) > 2:
        for i in range(len(players) - 2):
            out = out + ", " + players[i+1][1]
    out = out + " y " + players[len(players)-1][1]

    return out

def media_list(players):

    medias = []
    for p in players:
        medias.append(p[7])
    
    return medias

def tweetOnceInicial(gk, df, md, dl, b, team):
    response = client.create_tweet(text="¡El once inicial de " + team[1] + " es el siguiente!")
    id1 = response.data["id"]

    response = client.create_tweet(text="¡En la delantera tenemos a " + print_jugadores(dl) + "!", in_reply_to_tweet_id=id1, media_ids=media_list(dl))
    id1 = response.data["id"]

    response = client.create_tweet(text="¡En el centro del campo tenemos a " + print_jugadores(md) + "!", in_reply_to_tweet_id=id1, media_ids=media_list(md))
    id1 = response.data["id"]

    response = client.create_tweet(text="¡En la defensa tenemos a " + print_jugadores(df) + "!", in_reply_to_tweet_id=id1, media_ids=media_list(df))
    id1 = response.data["id"]

    response = client.create_tweet(text="¡Y finalmente, en la portería, tenemos a " + gk[0][1] + "!", in_reply_to_tweet_id=id1, media_ids=[gk[0][7]])
    id1 = response.data["id"]

def simular_partido(idmatch, allow_draws, tweet):

    cursor.execute("SELECT * FROM inazumadb.match WHERE idmatch = " + str(idmatch))
    match = cursor.fetchone()

    idteam1 = match[1]
    idteam2 = match[2]

    if tweet:
        print("Subiendo imágenes...")
        bdactions3.upload_media_team(idteam1)
        bdactions3.upload_media_team(idteam2)


    cursor.execute("SELECT * FROM team WHERE idteam = " + str(idteam1) + " OR idteam = " + str(idteam2))

    resultados = cursor.fetchall()

    team1 = resultados[0]
    team2 = resultados[1]
    
    if tweet:
        response = client.create_tweet(text='¡Ha llegado el momento que todos estábamos esperando! ¡Se van a enfrentar el equipo ' + team1[1] + " y el equipo " + team2[1] + "! ¿Para quién será la victoria?")
        id = response.data["id"]
    else:
        print("¡Ha llegado el momento que todos estábamos esperando! ¡Se van a enfrentar el equipo " + team1[1] + " y el equipo " + team2[1] + "! ¿Para quién será la victoria?")

    # DECIDIMOS EL ONCE INICIAL

    gk1, df1, md1, dl1, b1 = matchfunctions.onceinicial(team1[0])
    gk2, df2, md2, dl2, b2 = matchfunctions.onceinicial(team2[0])

    if tweet: 
        tweetOnceInicial(gk1, df1, md1, dl1, b1, team1)
        tweetOnceInicial(gk2, df2, md2, dl2, b2, team2)
    else:
        matchfunctions.printOnceInicial(gk1, df1, md1, dl1, b1, team1)
        matchfunctions.printOnceInicial(gk2, df2, md2, dl2, b2, team2)


    # DECIDIMOS EL ONCE INICIAL DE TEAM2

    idsaque2 = matchfunctions.saqueInicial(dl1, dl2, match)
    matchfunctions.comenzarPartido(match)

    match = matchfunctions.refrescarPartido(match)

    lineaformacion = 0

    ended = False

    players1 = [gk1, df1, md1, dl1]
    players2 = [gk2, df2, md2, dl2]

    for i in range(45):
        lineaformacion = matchfunctions.decide(match, team1[0], team2[0], lineaformacion)
        time.sleep(0)
        match = matchfunctions.refrescarPartido(match)
        print("¡Balón para " + matchfunctions.possesionTeam(match)[1] + "! (" + str(lineaformacion) + ")")
        time.sleep(0)

    print("¡Termina la primera parte!\n" + team1[1] + " " + str(match[4]) + " - " + str(match[5]) + " " + team2[1] + "\n\n\n")
    cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(idsaque2) + " WHERE idmatch = " + str(match[0]))
    conexion.commit()
    lineaformacion = 0

    for i in range(45):
        lineaformacion = matchfunctions.decide(match, team1[0], team2[0], lineaformacion)
        time.sleep(0)
        match = matchfunctions.refrescarPartido(match)
        print("¡Balón para " + matchfunctions.possesionTeam(match)[1] + "! (" + str(lineaformacion) + ")")
        time.sleep(0)

    if match[4] == match[5] and not allow_draws:

        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(idsaque2) + " WHERE idmatch = " + str(match[0]))
        conexion.commit()
        lineaformacion = 0

        print("¡EMPATE! ¡VA A COMENZAR LA PRÓRROGA!\n" + team1[1] + " " + str(match[4]) + " - " + str(match[5]) + " " + team2[1] + "\n\n\n")

        for i in range(15):
            lineaformacion = matchfunctions.decide(match, team1[0], team2[0], lineaformacion)
            time.sleep(0)
            match = matchfunctions.refrescarPartido(match)
            print("¡Balón para " + matchfunctions.possesionTeam(match)[1] + "! (" + str(lineaformacion) + ")")
            time.sleep(0)

        print("¡Termina el primer tiempo!\n" + team1[1] + " " + str(match[4]) + " - " + str(match[5]) + " " + team2[1] + "\n\n\n")
        cursor.execute("UPDATE inazumadb.match SET idplayerwithball = " + str(idsaque2) + " WHERE idmatch = " + str(match[0]))
        conexion.commit()
        lineaformacion = 0

        for i in range(15):
            lineaformacion = matchfunctions.decide(match, team1[0], team2[0], lineaformacion)
            time.sleep(0)
            match = matchfunctions.refrescarPartido(match)
            print("¡Balón para " + matchfunctions.possesionTeam(match)[1] + "! (" + str(lineaformacion) + ")")
            time.sleep(0)

    if match[4] == match[5] and not allow_draws:
        simularPenaltis()


    print("¡FINAL DEL PARTIDO!\n" + team1[1] + " " + str(match[4]) + " - " + str(match[5]) + " " + team2[1])

    if match[4] > match[5]:
        winner = match[1]
    elif match[5] > match[4]:
        winner = match[2]

    if match[4] != match[5]:
        cursor.execute("UPDATE inazumadb.match SET winner = " + str(winner) + " WHERE idmatch = " + str(match[0]))
    conexion.commit()

def simularPenaltis(team1, team2):

    score1 = 0
    score2 = 0

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(team1[0]) + " order by position desc")
    players1 = cursor.fetchall()

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(team2[0]) + " order by position desc")
    players2 = cursor.fetchall()

    players = [players1, players2]

    r = random.random()
    if r > 0.5:
        turn = 0
    else:
        turn = 1

    for i in range(5):
        None


simular_partido(403, False, False)