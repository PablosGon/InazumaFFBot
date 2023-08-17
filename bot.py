import tweepy

consumer_key = "gj2fvOMqXZCNvVaYKngkD5xcN"
consumer_secret = "kvefLxYNNpmCODEoYqPvlD6dIKLhJI7m7r02kMAcS3Jjm2dRBP"
access_token = "1692114192034119680-dTHxdfdwcFZHpa9D3Ozfd4S3XkPKHJ"
access_token_secret = "jZUck9uFCrWxxRFro04ecKyYhT6tWseskve7BvSmZVtek"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

user = api.verify_credentials()

print("Conexión exitosa. Bienvenido,", user.name)

api.update_status("Se vienen cositas")