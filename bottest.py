import tweepy

with open("C:/Users/pablo/OneDrive/Proyectos Personales/InazumaBot/keys/twitterkeys.txt", 'r', encoding='utf-8') as f:
    lineas = f.readlines()

client = tweepy.Client(consumer_key=lineas[0].split()[0],
                    consumer_secret=lineas[1].split()[0],
                    access_token=lineas[2].split()[0],
                    access_token_secret=lineas[3].split()[0],
                    bearer_token=lineas[4].split()[0])
# Replace the text with whatever you want to Tweet about
response = client.create_tweet(text='Se vienen cositas 5')

id = response.data["id"]

response = client.create_tweet(text="Se vienen cositas 6", in_reply_to_tweet_id=id)