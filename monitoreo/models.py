from django.db import models

class Cuenta(models.Model):
  nombre = models.CharField(max_length=100)
  pid = models.IntegerField(null=True,blank=True)
  activo = models.BooleanField(default=False)
  cantidad = models.PositiveIntegerField(default=0)
  hoy = models.PositiveIntegerField(default=0)
  tam_zip = models.FloatField(default=0)
  creado = models.DateField(auto_now_add=True)
  incluye_pasados = models.BooleanField(default=False)
  pasados_activo = models.BooleanField(default=False)
  def __unicode__(self):
    return self.nombre

class Hashtag(models.Model):
  nombre = models.CharField(max_length=100)
  pid = models.IntegerField(null=True,blank=True)
  activo = models.BooleanField(default=False)
  hashtag = models.BooleanField(default=True)
  cantidad = models.PositiveIntegerField(default=0)
  hoy = models.PositiveIntegerField(default=0)
  tam_zip = models.FloatField(default=0)
  creado = models.DateField(auto_now_add=True)
  hasta = models.DateField(null=True,blank=True)
  incluye_pasados = models.BooleanField(default=False)
  pasados_activo = models.BooleanField(default=False)
  def __unicode__(self):
    return self.nombre
