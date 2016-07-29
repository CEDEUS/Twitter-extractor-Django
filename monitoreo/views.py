import psutil
import os
import subprocess
from django.shortcuts import render_to_response, redirect, HttpResponse, get_object_or_404
from django.template.context import RequestContext
from models import Cuenta, Hashtag
import shlex
from django.contrib.auth.decorators import login_required
from shutil import make_archive
from wsgiref.util import FileWrapper
from datetime import timedelta

@login_required(login_url='/login/')
def data(request):
    cuentas = Cuenta.objects.all()
    for cuenta in cuentas:
      cuenta.activo = False
      cuenta.save()
    hashtags = Hashtag.objects.all()
    for hashtag in hashtags:
      hashtag.activo = False
      hashtag.save()

    for proc in psutil.process_iter():
      try:
        pinfo = proc.as_dict(attrs=['pid','name'])
      except psutil.NoSuchProcess:
        pass
      else:
        if pinfo['name'] == 'python':
          process = psutil.Process(int(pinfo['pid']))
          if 'streamaccount' in process.cmdline():
            cuenta = Cuenta.objects.get(nombre=process.cmdline()[-1])
            cuenta.pid = int(process.pid)
            cuenta.activo = True
            cuenta.save()
          elif 'streamhashtag' in process.cmdline():
            if '-H' in process.cmdline():
              n = True
            elif '-S' in process.cmdline():
              n = False
            hashtag = Hashtag.objects.get(nombre=process.cmdline()[-1],hashtag=n)
            hashtag.pid = int(process.pid)
            hashtag.activo = True
            hashtag.save()
          elif 'passaccount' in process.cmdline():
            cuenta = Cuenta.objects.get(nombre=process.cmdline()[-1])
            cuenta.pasados_activo = True
            cuenta.save()
          elif 'passhashtag' in process.cmdline():
            if '-H' in process.cmdline:
              n = True
            else:
              n = False
            hashtag = Hashtag.objects.get(nombre=process.cmdline()[-1],hashtag=n)
            hashtag.pasados_activo = True
            hashtag.save()
          else:
            for cuenta in Cuenta.objects.all():
                if cuenta.pasados_activo:
                    cuenta.incluye_pasados = True
                    cuenta.save()

    cuentas = Cuenta.objects.all()
    hashtags = Hashtag.objects.all()

    return render_to_response('botones.php',{'hashtags':hashtags,'cuentas':cuentas,'lencuentas':len(cuentas)},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def pasados(request,query=""):
  if query=="":
    pass
  elif query[0]=="C":
    cuenta = Cuenta.objects.get(id=query[1:])
    subprocess.Popen(shlex.split("python manage.py passaccount -c "+cuenta.nombre))
  elif query[0]=="H":
    hashtag = Hashtag.objects.get(id=query[1:])
    if hashtag.hashtag:
      nombre = '-H '+hashtag.nombre
    else:
      nombre = '-S '+hashtag.nombre
    subprocess.Popen(shlex.split("python manage.py passhashtag "+nombre))
  return redirect('/')

@login_required(login_url='/login/')
def iniciar_streamer_twitter(request):
  if request.method == 'GET':
    account  = request.GET['account']

    # Verificar si el proceso ya esta corriendo
    for proc in psutil.process_iter():
      try:
        pinfo = proc.as_dict(attrs=['pid','name'])
      except psutil.NoSuchProcess:
        pass
      else:
        if pinfo['name'] == 'python':
          process = psutil.Process(int(pinfo['pid']))
          if 'streamaccount' in process.cmdline() and process.cmdline()[-1] == account:
            return redirect('/')

    subprocess.Popen(shlex.split('python manage.py streamaccount -c ' + account))
    return redirect('/')
  else:
    return redirect('/')

@login_required(login_url='/login/')
def iniciar_streamer_hashtag(request):
  if request.method == 'GET':
    acc  = request.GET['account']
    account = get_object_or_404(Hashtag,id=acc)

    if account.hashtag:
      subprocess.Popen(shlex.split('python manage.py streamhashtag -H ' + account.nombre))
    else:
      subprocess.Popen(shlex.split('python manage.py streamhashtag -S ' + account.nombre))
  return redirect('/')


@login_required(login_url='/login/')
def agregar_cuenta(request):
  if request.method == 'POST':
    a = Cuenta(nombre=request.POST['cuenta'])
    a.save()
  return redirect('/')

@login_required(login_url='/login/')
def agregar_hashtag(request):
  if request.method == 'POST':
    if request.POST.get('hashtag',False):
      h = True
    else:
      h = False
    if request.POST.get('dias',False):
      try:
        dias = int(request.POST.get('dias'))
      except:
        dias = 7
    else:
      return redirect('/')
    a = Hashtag(nombre=request.POST['cuenta'], hashtag = h)
    a.save()
    a.hasta = a.creado + timedelta(days=dias)
    a.save()
  return redirect('/')


@login_required(login_url='/login/')
def matarproceso(request):
  if request.method == 'GET':
    pid = request.GET['pid']
    os.system('kill ' + pid)
    return redirect('/')
  else:
    return redirect('/')

@login_required(login_url='/login/')
def eliminar(request,query=""):
  if query[0] == 'C':
    cuenta = Cuenta.objects.get(id=query[1:])
    if cuenta.activo:
      os.system('kill '+str(cuenta.pid))
    os.system('rm -rf media/cuentas/'+cuenta.nombre+'.txt')
    os.system('rm -rf media/cuentas/'+cuenta.nombre+'.txt.zip')
    cuenta.delete()
  elif query[0] == 'H':
    cuenta = Hashtag.objects.get(id=query[1:])
    if cuenta.activo:
      os.system('kill '+str(cuenta.pid))
    if cuenta.hashtag:
      os.system('rm -rf media/hashtag/HASHTAG'+cuenta.nombre+'.txt')
      os.system('rm -rf media/hashtag/HASHTAG'+cuenta.nombre+'.txt.zip')
    else:
      os.system('rm -rf media/hashtag/'+cuenta.nombre+'.txt')
      os.system('rm -rf media/hashtag/'+cuenta.nombre+'.txt.zip')
    cuenta.delete()
  return redirect('/')

@login_required(login_url='/login/')
def eliminar_archivo(request):
  if request.method == 'GET':
    query = request.GET['query']
    if query[0] == 'C':
      cuenta = Cuenta.objects.get(id=query[1:])
      if cuenta.activo:
        os.system('kill '+str(cuenta.pid))
      os.system('rm -rf media/cuentas/'+cuenta.nombre+'.txt')
      os.system('rm -rf media/cuentas/'+cuenta.nombre+'.txt.zip')
      os.system('touch media/cuentas/'+cuenta.nombre+'.txt')
      os.system('touch media/cuentas/'+cuenta.nombre+'.txt.zip')
      cuenta.cantidad=0
      cuenta.hoy=0
      cuenta.tam_zip=0
      cuenta.save()
    elif query[0] == 'H':
      cuenta = Hashtag.objects.get(id=query[1:])
      if cuenta.activo:
        os.system('kill '+str(cuenta.pid))
      if cuenta.hashtag:
        os.system('rm -rf media/hashtag/HASHTAG'+cuenta.nombre+'.txt')
        os.system('rm -rf media/hashtag/HASHTAG'+cuenta.nombre+'.txt.zip')
        os.system('touch media/hashtag/HASHTAG'+cuenta.nombre+'.txt')
      else:
        os.system('rm -rf media/hashtag/'+cuenta.nombre+'.txt')
        os.system('rm -rf media/hashtag/'+cuenta.nombre+'.txt.zip')
        os.system('touch media/hashtag/'+cuenta.nombre+'.txt')
      os.system('python manage.py cron')
      cuenta.cantidad=0
      cuenta.hoy=0
      cuenta.tam_zip=0
      cuenta.save()
  return redirect('/')
