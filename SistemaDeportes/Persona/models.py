from django.db import models

# Clase abstracta con los campos comunes
class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.IntegerField()
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre

class Jugador(Persona):
    numero = models.IntegerField()
    posicion = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"

class Albitro(Persona):
    tipo = models.CharField(max_length=50)

    def sancionar(self, jugador, motivo):
        # Aquí puedes definir la lógica de sanción
        sancion = f"El árbitro {self.nombre} ha sancionado al jugador {jugador.nombre} por: {motivo}"
        return sancion

    def __str__(self):
        return f"Árbitro {self.nombre}"
