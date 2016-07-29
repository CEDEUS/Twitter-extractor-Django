from pymongo import MongoClient
import json

def crear_CSV(cuenta='cristian_f_g',tipo='C'):

  #Coneccion con la base de datos
  client = MongoClient('localhost', 27017)
  db = client['twitter_db']
  collection = db[cuenta]

  if tipo=='C':
    ruta = 'media/cuentas/'
  else:
    ruta = 'media/hashtag/'

  #Abrir archivo CSV
  archivo = open(ruta+cuenta.replace('#','')+'.csv',"w")
  archivo.write("text;id;created_at;user_screen_name;Y;X;Polygon\n")

  #Lectura de tweets y construccion de archivo CSV
  tweets_iterator = collection.find()
  for tweet in tweets_iterator:
    text = tweet.get('text','').replace(';',',')+';'
    text = text +str(tweet.get('id',''))+';'
    text = text+str(tweet.get('created_at',''))+';'
    text = text+tweet.get('user',{'screen_name':''})['screen_name']+';'
    #Busqueda de coordenadas para posicionamiento geografico
    if tweet.get('place',None) != None:
      aux = []
      polygon = 'POLYGON(('
      for coord in tweet['place']['bounding_box']['coordinates'][0]:
          for m in coord:
              aux.append(m)
              polygon = polygon + str(m) + ' '
          polygon = polygon.strip(' ')+','
      polygon = polygon.strip(',')+'))'
      aux = list(set(aux))
      aux.sort(reverse=True) #Solo para paises cercanos a Chile
      aux = [(aux[0]+aux[1])/2,(aux[2]+aux[3])/2] #Coordenadas X e Y
      text = text + str(aux[0]) + ';' + str(aux[1])+';' +polygon+'\n'
    else:
      text = text + ';;\n'
    archivo.write(text.encode('utf-8'))
  archivo.close()
  print "Data compilada en csv para " + cuenta
