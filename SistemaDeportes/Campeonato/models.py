from django.db import models
from django.core.exceptions import ValidationError

# Enumeración para los tipos de campeonatos
class TipoCampeonato(models.TextChoices):
    LIGA = 'LI', 'Liga'
    COPA = 'CO', 'Copa'
    AMISTOSO = 'AM', 'Amistoso'
    INTERNACIONAL = 'IN', 'Internacional'
    MUERTE_SUBITA = 'MS', 'Muerte Súbita'

class Campeonato(models.Model):
    nombre = models.CharField(max_length=50)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    numeroEquipos = models.IntegerField()
    numeroJugadores = models.IntegerField()
    numeroArbitros = models.IntegerField()
    tipo = models.CharField(
        max_length=2,
        choices=TipoCampeonato.choices,
        default=TipoCampeonato.LIGA
    )

    def clean(self):
        if self.numeroEquipos < 2:
            raise ValidationError("El número de equipos debe ser mayor o igual a 2")
        if self.numeroJugadores < 0:
            raise ValidationError("El número de jugadores no puede ser negativo")
        if self.numeroArbitros < 0:
            raise ValidationError("El número de árbitros no puede ser negativo")

    def __str__(self):
        return self.nombre
