from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from monitoreo.models import Cuenta
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
from pymongo import MongoClient
import time

class Command(BaseCommand):
 
    help = "Streamer de cuenta"
 
    option_list = BaseCommand.option_list  + (
                        make_option('-c', action='store',
                            dest='nombre',
                            default='',
                            help='Nombre de la cuenta'),
                  )

    def handle(self, *app_labels, **options):
        nombre = options['nombre']
        class listener(StreamListener):
            def on_data(self, data):
                try:
                    #Procesamiento de datos
                    tweet = json.loads(data)
                    client = MongoClient('localhost',27017)
                    db = client['twitter_db']
                    collection = db[nombre]
                    collection.insert(tweet)
                    print tweet['text']
                except:
                    pass
                finally:

                    return True

            def on_error(self, status):
                print status
                print "Alcanzado limite de solicitudes, descanzando 5 minutos para " + nombre
                time.sleep(5*60)

        print "CONECTANDO A LA API DE TWITTER..."
        consumer_key = 'IxT5vwTXwond0kbahQMKaU46g'
        consumer_secret = 'QpYbm5ZCc6jqFQxoUUElTCuSVjmLQ69cyNsgWzDu688TaehcVi'
        access_token = '75291095-yDtR9RqcZdOJHy2zV6iVf8WgKkwpQTn62oB6ulONt'
        access_secret = '24H7aZbjk7saf8V7mOhkBiQe4jgdF1KI2AzxmK72zzrzU'

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        api = tweepy.API(auth)

        print "RECOLECTANDO Y GUARDANDO TWEETS EN LA BASE DE DATOS "

        tweets = api.user_timeline(screen_name=nombre,page=1,per_page=2)
        cuentaid = str(tweets[0].user.id)

        twitterStream = Stream(auth, listener())
        twitterStream.filter(follow=[cuentaid])
