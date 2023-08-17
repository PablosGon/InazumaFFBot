import tweepy

with open("C:/Users/pablo/OneDrive/Proyectos Personales/InazumaBot/keys/twitterkeys.txt", 'r', encoding='utf-8') as f:
    lineas = f.readlines()



consumer_key = lineas[0].split()[0]
consumer_secret = lineas[1].split()[0]
access_token = lineas[2].split()[0]
access_token_secret = lineas[3].split()[0]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.verify_credentials()

print("Conexión exitosa. Bienvenido,", user.name)