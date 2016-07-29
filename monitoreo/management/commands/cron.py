from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from monitoreo.models import Hashtag, Cuenta
from monitoreo.utils import crear_CSV
import os
import datetime
from pymongo import MongoClient
import json

class Command(BaseCommand):
 
    help = "Corre el script actualizador detweets por dia"
 
    def handle(self, *app_labels, **options):
        ahora = datetime.datetime.now()

        client = MongoClient('localhost',27017)
        db = client['twitter_db']

        cuentas = Cuenta.objects.all()
        for cuenta in cuentas:
            archivo = open('media/cuentas/'+cuenta.nombre+'.txt','w')
            collection = db[cuenta.nombre]
            tweets = collection.find()
            cuenta.cantidad = 0
            cuenta.hoy = 0
            for tweet in tweets:
                cuenta.cantidad = cuenta.cantidad + 1
                archivo.write(str(tweet)+'\n')
                try:
                    if divmod((ahora - datetime.datetime.fromtimestamp(int(tweet['timestamp_ms'])/1000.0)).total_seconds(),60)[0]<=1440.0:
                        cuenta.hoy = cuenta.hoy + 1
                except:
                    pass
            archivo.close()
            os.system('zip media/cuentas/'+cuenta.nombre+'.txt.zip media/cuentas/'+cuenta.nombre+'.txt')
            try:
                cuenta.tam_zip = os.path.getsize("media/cuentas/"+cuenta.nombre+'.txt.zip')/1000.0
            except:
                pass
            crear_CSV(cuenta.nombre)
            cuenta.save()

        hashtags = Hashtag.objects.all()
        for hashtag in hashtags:
            if hashtag.activo and hashtag.hasta < datetime.datetime.today().date():
                os.system('kill '+str(hashtag.pid))

            if hashtag.hashtag:
                collection = db['H#'+hashtag.nombre]
                archivo = open('media/hashtag/HASHTAG'+hashtag.nombre+'.txt','w')
            else:
                collection = db['S#'+hashtag.nombre]
                archivo = open('media/hashtag/'+hashtag.nombre+'.txt','w')
            tweets = collection.find()

            hashtag.cantidad = 0
            hashtag.hoy = 0
            for tweet in tweets:
                hashtag.cantidad = hashtag.cantidad + 1
                archivo.write(str(tweet)+'\n')
                try:
                    if divmod((ahora - datetime.datetime.fromtimestamp(int(tweet['timestamp_ms'])/1000.0)).total_seconds(),60)[0]<=1440.0:
                        hashtag.hoy = hashtag.hoy + 1
                except:
                    pass
            archivo.close()

            if hashtag.hashtag:
                os.system('zip media/hashtag/HASHTAG'+hashtag.nombre+'.txt.zip media/hashtag/HASHTAG'+hashtag.nombre+'.txt')
                crear_CSV('H#'+hashtag.nombre,'H')
                try:
                    hashtag.tam_zip = os.path.getsize("media/hashtag/HASHTAG"+hashtag.nombre+".txt.zip")/1000.0
                except:
                    print "Error al intentar sacar tamanio de archivo de "+hashtag.nombre
            else:
                os.system('zip media/hashtag/'+hashtag.nombre+'.txt.zip media/hashtag/'+hashtag.nombre+'.txt')
                crear_CSV('S#'+hashtag.nombre,'S')
                try:
                    hashtag.tam_zip = os.path.getsize("media/hashtag/"+hashtag.nombre+".txt.zip")/1000.0
                except:
                    print "Error al intentar sacar tamanio de archivo de "+hashtag.nombre
            hashtag.save()
