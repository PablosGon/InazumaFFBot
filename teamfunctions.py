import mysql.connector
import time
import matchfunctions

import tweepy

with open("C:/Users/pablo/OneDrive/Proyectos Personales/InazumaBot/keys/twitterkeys.txt", 'r', encoding='utf-8') as f:
    lineas = f.readlines()

client = tweepy.Client(consumer_key=lineas[0].split()[0],
                    consumer_secret=lineas[1].split()[0],
                    access_token=lineas[2].split()[0],
                    access_token_secret=lineas[3].split()[0],
                    bearer_token=lineas[4].split()[0])

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb",
    consume_results=True
)

cursor = conexion.cursor()

def present_team(idteam):

    cursor.execute("SELECT name FROM team WHERE idteam = " + str(idteam))
    teamname = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(idteam) + " ORDER BY position")
    players = cursor.fetchall()

    response = client.create_tweet(text="¡Va a presentarse el equipo " + teamname + "!")
    id_reply = response.data["id"]

    for p in players:

        supertecnicas = "Sus supertécnicas son las siguientes:\n"

        if p[2] == 1:
            position = "portero"
            supertecnicas = supertecnicas + "- " + matchfunctions.getSupertecnica(p, 1) + " (Parada)\n"
        elif p[2] == 2:
            position = "defensa"
            supertecnicas = supertecnicas + "- " + matchfunctions.getSupertecnica(p, 2) + " (Bloqueo)\n"
            supertecnicas = supertecnicas + "- " + matchfunctions.getSupertecnica(p, 3) + " (Regate)\n"
        elif p[2] == 3:
            position = "centrocampista"
            supertecnicas = supertecnicas + "- " + matchfunctions.getSupertecnica(p, 2) + " (Bloqueo)\n"
            supertecnicas = supertecnicas + "- " + matchfunctions.getSupertecnica(p, 3) + " (Regate)\n"
            supertecnicas = supertecnicas + "- " + matchfunctions.getSupertecnica(p, 4) + " (Tiro)\n"
        elif p[2] == 4:
            position = "delantero"
            supertecnicas = supertecnicas + "- " + matchfunctions.getSupertecnica(p, 3) + " (Regate)\n"
            supertecnicas = supertecnicas + "- " + matchfunctions.getSupertecnica(p, 4) + " (Tiro)\n"


        if p[6] == 1:
            afinidad = "aire"
        elif p[6] == 2:
            afinidad = "bosque"
        elif p[6] == 3:
            afinidad = "fuego"
        elif p[6] == 4:
            afinidad = "montaña"

        response = client.create_tweet(text="¡" + p[1] + ", " + position + " de " + afinidad + "!\n\n" + supertecnicas, media_ids=[p[7]], in_reply_to_tweet_id=id_reply)
        id_reply = response.data["id"]

present_team(5)
