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
                        make_option('-H', action='store',
                            dest='hashtag',
                            default='',
                            help='Nombre del hashtag'),
                  )

    option_list = option_list  + (
                        make_option('-S', action='store',
                            dest='search',
                            default='',
                            help='Nombre de la busqueda'),
                  ) 

    def handle(self, *app_labels, **options):

        if options['hashtag']!='':
            nombre = options['hashtag']
            h = True
        elif options['search']!='':
            nombre = options['search']
            h = False
        else:
            return

        class listener(StreamListener):
            def on_data(self, data):
                try:
                    #Procesamiento de datos
                    tweet = json.loads(data)
                    client = MongoClient('localhost',27017)
                    db = client['twitter_db']
                    if h:
                        collection = db['H'+nombre]
                    else:
                        collection = db['S#'+nombre]
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

        if h:
            nombre = '#'+nombre

        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=[nombre])
