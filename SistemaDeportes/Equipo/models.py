from django.db import models

# Create your models here.
class Equipo (models.Model):
    nombre = models.CharField(max_length=50)
    participantes = models.ManyToManyField("Persona.Jugador")
    disiplina = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre