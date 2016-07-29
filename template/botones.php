<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="300">
    <title>CF Twitter Harvester</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Le styles -->
    <script src="{{STATIC_URL}}js/jquery.js"></script>
    <link href="{{STATIC_URL}}css/bootstrap.css" rel="stylesheet" type="text/css">
    <link href="{{STATIC_URL}}css/bootstrap-switch.css" rel="stylesheet">
    <script src="{{STATIC_URL}}js/bootstrap-switch.js"></script>

    

  </head>

  <body> 
    <div class="container theme-showcase" role="main">
    <a href='/logout/'>logout</a>
<center><b><font size="16">CF Twitter Harvester</font></b></center>
      <!-- Main jumbotron for a primary marketing message or call to action -->

<script>
    $(document).ready(function() {
{% for cuenta in cuentas %}
    $("#switch-state{{forloop.counter}}").bootstrapSwitch('state',{% if cuenta.activo%}true{%else%}false{%endif%});
{% endfor %}
{% for hashtag in hashtags %}
    $("#switch-state{{forloop.counter|add:lencuentas}}").bootstrapSwitch('state',{% if hashtag.activo%}true{%else%}false{%endif%});
{% endfor %}
  });
</script>
<div class="container" style="padding:54px;">
    
    <div class="row">
  <div class="col-md-1"></div>
  <div class="col-md-1"></div>
  <div class="col-md-8">

      <div id="info_santiago" > 

  <table class="table table-bordered">
  <thead>
    <tr>
      <td colspan="6" style="text-align: -webkit-center;"><b>Twitter - Accounts</b></td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Account</td>
      <td>#</td>
      <td># per day</td>
      <td>Zip size [k]</td>
      <td>Creation date</td>
      <td>State</td>
    </tr>
{% for cuenta in cuentas %}
    <tr>
      <td>{{cuenta.nombre}}  [<a href='/media/cuentas/{{cuenta.nombre}}.txt.zip'>data</a>][<a href='/media/cuentas/{{cuenta.nombre}}.csv'>csv</a>] [<a href='/eliminar/C{{cuenta.id}}/'>delete account</a>]</td>
      <td>{{cuenta.cantidad}}</td>
      <td>{{cuenta.hoy}}</td>
      <td>{{cuenta.tam_zip}}   [<a href='/eliminar_archivo/?query=C{{cuenta.id}}'>delete file</a>]</td>
      <td>{{cuenta.creado}}</td>
{% if cuenta.activo %}
      <td>
            <p>
              <a href='/matarproceso/?pid={{cuenta.pid}}'><input id="switch-state{{forloop.counter}}" name="box{% if foorlop.counter != 1 %}{{forloop.counter}}{%endif%}" type="checkbox" checked></a>
            </p>
           
      </td>
{% else %}
      <td>
            <p>
              <a href='/iniciarstream/?account={{cuenta.nombre}}'><input id="switch-state{{forloop.counter}}" name="box{% if foorlop.counter != 1 %}{{forloop.counter}}{%endif%}" type="checkbox" checked></a>
            </p>

      </td>
{% endif %}
{% if not cuenta.incluye_pasados %}
  {% if cuenta.pasados_activo %}
      <td> Descargando tweets pasados </td>
  {% else %}
      <td> <a href='/pasados/C{{cuenta.id}}'>Descargar tweets actuales</a></td>
  {% endif %}
{% endif %}
</tr>
{% endfor %}
<tr>
<td colspan="6" style="text-align: -webkit-center;">

<form action="/agregarcuenta/" method="post"><label for="cuenta">Add acount: </label>
{% csrf_token %}
<input id="cuenta" type="text" name="cuenta" value="">
<input type="submit" value="OK">
</form>

</td>
</tr>


</tbody>
</table>

  <table class="table table-bordered">
  <thead>
    <tr>
      <td colspan="7" style="text-align: -webkit-center;"><b>Twitter - Hashtags & searchs</b></td>
    </tr>
  </thead>
</tbody>
    <tr>
      <td>Account</td>
      <td>#</td>
      <td># per day</td>
      <td>Zip size [k]</td>
      <td>Creation date</td>
      <td>Finish date</td>
      <td>State</td>
    </tr>

{% for hashtag in hashtags %}
    <tr>
      <td>{{hashtag.nombre}}  [<a href='/media/hashtag/{%if hashtag.hashtag%}HASHTAG{%endif%}{{hashtag.nombre}}.txt.zip'>data</a>][<a href='/media/hashtag/{%if hashtag.hashtag%}H{%else%}S{%endif%}{{hashtag.nombre}}.csv'>csv</a>] [<a href='/eliminar/H{{hashtag.id}}/'>delete search</a>]</td>
      <td>{{hashtag.cantidad}}</td>
      <td>{{hashtag.hoy}}</td>
      <td>{{hashtag.tam_zip}}   [<a href='/eliminar_archivo/?query=H{{hashtag.id}}'>delete file</a>]</td>
      <td>{{hashtag.creado}}</td>
      <td>{{hashtag.hasta}}</td>
{% if hashtag.activo %}
      <td>
            <p>
              <a href='/matarproceso/?pid={{hashtag.pid}}'><input id="switch-state{{forloop.counter|add:lencuentas}}" name="box{{forloop.counter|add:lencuentas}}" type="checkbox" checked></a>
            </p>

      </td>
{% else %}
      <td>
            <p>
              <a href='/iniciarhashtag/?account={{hashtag.id}}'><input id="switch-state{{forloop.counter|add:lencuentas}}" name="box{{forloop.counter|add:lencuentas}}" type="checkbox" checked></a>
            </p>

      </td>
{% endif %}
{% if not hashtag.incluye_pasados %}
  {% if hashtag.pasados_activo %}
      <td> Descargando tweets pasados </td>
  {% else %}
      <td> <a href='/pasados/H{{hashtag.id}}'>Descargar tweets actuales</a></td>
  {% endif %}
{% endif %}
</tr>
{% endfor %}




<tr>
<td colspan="7" style="text-align: -webkit-center;">

<form action="/agregarhashtag/" method="post"><label for="cuenta">Add Hashtag: </label>
{% csrf_token %}
<input id="cuenta" type="text" name="cuenta" value=""><br>
Activation days <input id="dias" type="test" name="dias" value=""><br>
<input id="hashtag" type="checkbox" name="hashtag" value="hashtag" checked="checked"> Include # <br>
<input type="submit" value="OK">
</form>


</td>
</tr>


  </tbody>
</table>

<table class="table table-bordered">
<thead>
<tr>
<td colspan="3" style="text-align: -webkit-center;">La información de Twitter se actualiza cada 10 minutos.<br>Activar y desactivar los botones puede causar problemas al intentar capturar los datos, favor de activar o desactivar solo cuando sea necesario.</td>
</tr>
</thead>
<tbody>
</tbody>
</table>


    </div>
</div>
  <div class="col-md-1"></div>
  <div class="col-md-1"></div>
</div>      

<center>
<table style="undefined;table-layout: fixed; width: 600px">
<colgroup>
<col style="width: 320px">
<col style="width: 320px">
</colgroup>
  <tr>
    <th><center>Información de Contacto</center></th>
    <th><center>Agradecimientos</center></th>
  </tr>
  <tr>
    <td><center>Stefan Steiniger<br>ssteiniger@uc.cl<br><br>Cristian Fuentes<br>fuentescri@gmail.com</center></td>
    <td><img src="http://www.cedeus.cl/wp-content/themes/cedeus/img/logo.png" border="2" width="100"></td>
  </tr>
</table>
</center>

    </div> <!-- /container -->
  </body>

  </html>

