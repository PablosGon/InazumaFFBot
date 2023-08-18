import mysql.connector
import random
import matchfunctions
import time
import tweepy

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

def simular_partido(idteam1, idteam2):

    cursor.execute("SELECT * FROM team WHERE idteam = " + str(idteam1) + " OR idteam = " + str(idteam2))

    resultados = cursor.fetchall()

    team1 = resultados[0]
    team2 = resultados[1]

    match = matchfunctions.crearPartido(team1, team2)
    response = client.create_tweet(text='¡Ha llegado el momento que todos estábamos esperando! ¡Se van a enfrentar el equipo ' + team1[1] + " y el equipo " + team2[1] + "! ¿Para quién será la victoria?")
    id = response.data["id"]

    # DECIDIMOS EL ONCE INICIAL DE TEAM1

    gk1, df1, md1, dl1, b1 = matchfunctions.onceinicial(team1[0])
    response = client.create_tweet("¡El once inicial de " + team1[1] + " es el siguiente!")
    id1 = response.data["id"]

    response = client.create_tweet("¡En la delantera tenemos a " + print_jugadores(dl1) + "!", in_reply_to_tweet_id=id1, media_ids=media_list(dl1))
    id1 = response.data["id"]

    response = client.create_tweet("¡En el centro del campo tenemos a " + print_jugadores(md1) + "!", in_reply_to_tweet_id=id1, media_ids=media_list(md1))
    id1 = response.data["id"]

    response = client.create_tweet("¡En la defensa tenemos a " + print_jugadores(df1) + "!", in_reply_to_tweet_id=id1, media_ids=media_list(df1))
    id1 = response.data["id"]

    response = client.create_tweet("¡Y finalmente, en la portería, tenemos a " + gk1[0][1] + "!", in_reply_to_tweet_id=id1, media_ids=[gk1[0][7]])
    id1 = response.data["id"]

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