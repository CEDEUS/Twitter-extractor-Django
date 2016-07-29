from pymongo import MongoClient
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from monitoreo.models import Cuenta
import os
import datetime
import tweepy
from tweepy import OAuthHandler
import psycopg2 as lite
import sys
import time
import json
# Class MUST be named 'Command'
class Command(BaseCommand):
 
    # Displayed from 'manage.py help mycommand'
    help = "Rescate de tweets pasados de cuenta"
 
    # make_option requires options in optparse format
    option_list = BaseCommand.option_list  + (
                        make_option('-c', action='store',
                            dest='nombre',
                            default='',
                            help='Nombre de la cuenta'),
                  )

    def handle(self, *app_labels, **options):
        """
        app_labels - app labels (eg. myapp in "manage.py reset myapp")
        options - configurable command line options
        """

        nombre=options['nombre']

        print "CONECTANDO A LA API DE TWITTER..."

        consumer_key = 'IxT5vwTXwond0kbahQMKaU46g'
        consumer_secret = 'QpYbm5ZCc6jqFQxoUUElTCuSVjmLQ69cyNsgWzDu688TaehcVi'
        access_token = '75291095-yDtR9RqcZdOJHy2zV6iVf8WgKkwpQTn62oB6ulONt'
        access_secret = '24H7aZbjk7saf8V7mOhkBiQe4jgdF1KI2AzxmK72zzrzU'

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        api = tweepy.API(auth)

        print "RECOLECTANDO Y GUARDANDO TWEETS EN LA BASE DE DATOS "

        client = MongoClient('localhost',27017)
        db = client['twitter_db']
        collection = db[nombre]

        boolean = True
        pag = 1
        count = 1
        while boolean:
            try:
                tweets = api.user_timeline(screen_name=nombre,page=pag,per_page=40)

                if len(tweets)==0:
                    boolean = False

                for tweet in tweets:
                    collection.insert(tweet._json)
                    count = count + 1
                print "Tweets guardados: " + str(count)
                pag = pag + 1
            except tweepy.TweepError:
                print "Limite alcanzado, descanzando 15 minutos"
                time.sleep(60*15)
                continue
            except Exception as e:
                print e
                print type(e)

