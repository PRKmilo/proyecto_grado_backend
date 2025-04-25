from django.db import models



class Proceso(models.Model):
    proceso_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('usuarios.Usuario', models.DO_NOTHING, blank=True, null=True)
    seriado_proceso = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_actualizacion = models.DateField(blank=True, null=True)
    limite_tiempo = models.IntegerField(blank=True, null=True)
    fecha_limite = models.DateField(blank=True, null=True)

    def __str__(self):
         return f"Proceso {self.proceso_id} - {self.seriado_proceso or 'Sin código'}"


    class Meta:
        managed = True
        db_table = 'proceso'
