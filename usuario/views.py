from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User

def login_user(request):
  if request.user.is_authenticated():
    return redirect('/')

  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      login(request,user)
      return redirect('/')
  return render_to_response('login.php',context_instance=RequestContext(request))

def logout_user(request):
  logout(request)
  return redirect('/')
