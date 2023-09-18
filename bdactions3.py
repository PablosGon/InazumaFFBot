import mysql.connector
import tweepy

with open("C:/Users/pablo/OneDrive/Proyectos Personales/InazumaBot/keys/twitterkeys.txt", 'r', encoding='utf-8') as f:
    lineas = f.readlines()

consumer_key=lineas[0].split()[0]
consumer_secret=lineas[1].split()[0]
access_token=lineas[2].split()[0]
access_token_secret=lineas[3].split()[0]
bearer_token=lineas[4].split()[0]

client = tweepy.Client(consumer_key,
                    consumer_secret,
                    access_token,
                    access_token_secret,
                    bearer_token)

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)


conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL0104",
    database="inazumadb",
    consume_results=True
)

cursor = conexion.cursor()

def upload_media_team(idteam):

    cursor.execute("SELECT * FROM player WHERE teamid = " + str(idteam))
    players = cursor.fetchall()

    for p in players:
        media = api.media_upload("C:/Users/pablo/Pictures/InazumaBot/" + str(idteam) + "/" + str(p[0]) + ".jpg")
        print(media.media_id)

        cursor.execute("UPDATE player SET idmedia = " + str(media.media_id) + " WHERE idplayer = " + str(p[0]))
    conexion.commit()