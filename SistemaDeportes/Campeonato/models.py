from django.db import models
from django.core.exceptions import ValidationError

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

class Resultado(models.TextChoices):
    GANADO = 'G', 'Ganado'
    EMPATADO = 'E', 'Empatado'
    PERDIDO = 'P', 'Perdido'

class Encuentro(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    fecha = models.DateField()
    equipoLocal = models.ForeignKey("Equipo.Equipo", on_delete=models.CASCADE, related_name="equipo_local")
    equipoVisitante = models.ForeignKey("Equipo.Equipo", on_delete=models.CASCADE, related_name="equipo_visitante")
    golesLocal = models.IntegerField()
    golesVisitante = models.IntegerField()
    arbitro = models.ForeignKey("Persona.Albitro", on_delete=models.CASCADE)
    resultado = models.CharField(
        max_length=1,
        choices=Resultado.choices,
        default=Resultado.EMPATADO
    )

    def clean(self):
        if self.golesLocal < 0:
            raise ValidationError("El número de goles del equipo local no puede ser negativo")
        if self.golesVisitante < 0:
            raise ValidationError("El número de goles del equipo visitante no puede ser negativo")

    def __str__(self):
        if self.golesLocal > self.golesVisitante:
            return f"{self.equipoLocal.nombre} ganó contra {self.equipoVisitante.nombre}"
        elif self.golesLocal < self.golesVisitante:
            return f"{self.equipoVisitante.nombre} ganó contra {self.equipoLocal.nombre}"
        else:
            return f"Empate entre {self.equipoLocal.nombre} y {self.equipoVisitante.nombre}"
