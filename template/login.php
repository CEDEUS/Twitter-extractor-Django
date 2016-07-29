<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Le styles -->
    <link href="{{STATIC_URL}}css/bootstrap.css" rel="stylesheet" type="text/css">
 

    <script src="{{STATIC_URL}}js/jquery.js"></script>

  </head>

  <body> 
         
            
<div class="container" style="padding:54px;">
    
    <div class="row">
  <div class="col-md-2"></div>
  <div class="col-md-2"></div>
  <div class="col-md-4">

    
    <form action="/login/" method="post">
      <form class="form-signin">
{% csrf_token %}
        <h2 class="form-signin-heading">Inicie sesi&oacute;n</h2>
        <label for="inputName" class="sr-only">Usuario</label>
        <input type="text" name="username" id="inputName" class="form-control" placeholder="Nombre de usuario" required="" autofocus="">
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" name="password" id="inputPassword" class="form-control" placeholder="Contrase&nacute;a" required="">
        <div class="checkbox">
          <label>
            <input type="checkbox" value="remember-me"> Recordarme
          </label>
        </div>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Entrar</button>
      </form>
    </form>
    
      

    </div>
</div>
  <div class="col-md-2"></div>
  <div class="col-md-2"></div>
</div>      

      

    </div> <!-- /container -->
  </body>

  </html>

