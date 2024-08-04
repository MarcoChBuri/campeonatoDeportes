from django.db import models

class EstadisticasJugador(models.Model):
    jugador = models.ForeignKey("Persona.Jugador", on_delete=models.CASCADE)
    goles = models.IntegerField()
    tarjetasAmarillas = models.IntegerField()
    tarjetasRojas = models.IntegerField()

    def __str__(self):
        return f"Estadísticas de {self.jugador.nombre}"

class EstadisticasEquipo(models.Model):
    equipo = models.ForeignKey("Equipo.Equipo", on_delete=models.CASCADE)
    partidosJugados = models.IntegerField()
    partidosGanados = models.IntegerField()
    partidosEmpatados = models.IntegerField()
    partidosPerdidos = models.IntegerField()
    golesFavor = models.IntegerField()
    golesContra = models.IntegerField()

    def __str__(self):
        return f"Estadísticas de {self.equipo.nombre}"
