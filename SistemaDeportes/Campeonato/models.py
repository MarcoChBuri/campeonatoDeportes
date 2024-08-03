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

    def save(self, *args, **kwargs):
        self.calculate_result()
        super().save(*args, **kwargs)
        self.update_tabla_posiciones()

    def calcularResultado(self):
        if self.golesLocal > self.golesVisitante:
            self.resultado = Resultado.GANADO
        elif self.golesLocal < self.golesVisitante:
            self.resultado = Resultado.PERDIDO
        else:
            self.resultado = Resultado.EMPATADO

    def actualizar(self):
        equipos = [self.equipoLocal, self.equipoVisitante]
        puntos = {self.equipoLocal: 0, self.equipoVisitante: 0}

        if self.resultado == Resultado.GANADO:
            puntos[self.equipoLocal] = 3
        elif self.resultado == Resultado.PERDIDO:
            puntos[self.equipoVisitante] = 3
        elif self.resultado == Resultado.EMPATADO:
            puntos[self.equipoLocal] = 1
            puntos[self.equipoVisitante] = 1

        for equipo in equipos:
            tabla_posicion, created = TablaPosiciones.objects.get_or_create(campeonato=self.campeonato, equipo=equipo)
            tabla_posicion.puntos += puntos[equipo]
            tabla_posicion.save()

    def __str__(self):
        if self.golesLocal > self.golesVisitante:
            return f"{self.equipoLocal.nombre} ganó contra {self.equipoVisitante.nombre}"
        elif self.golesLocal < self.golesVisitante:
            return f"{self.equipoVisitante.nombre} ganó contra {self.equipoLocal.nombre}"
        else:
            return f"Empate entre {self.equipoLocal.nombre} y {self.equipoVisitante.nombre}"

class TablaPosiciones(models.Model):
    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)
    equipo = models.ForeignKey("Equipo.Equipo", on_delete=models.CASCADE)
    puntos = models.IntegerField(default=0)

    class Meta:
        unique_together = ('campeonato', 'equipo')

    def __str__(self):
        return f"{self.equipo.nombre} - {self.puntos} puntos en {self.campeonato.nombre}"
