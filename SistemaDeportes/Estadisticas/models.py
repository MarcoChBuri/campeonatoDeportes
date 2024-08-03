from django.db import models

class EstadisticasJugador(models.Model):
    jugador = models.ForeignKey("Persona.Jugador", on_delete=models.CASCADE)
    goles = models.IntegerField()
    tarjetasAmarillas = models.IntegerField()
    tarjetasRojas = models.IntegerField()

    def __str__(self):
        return f"Estadísticas de {self.jugador.nombre}"

