from django.db import models

class Notario(models.Model):
    notario_id = models.AutoField(primary_key=True)
    numero_licencia = models.CharField(max_length=255, blank=True, null=True)
    oficina_registro = models.CharField(max_length=255)
    notaria_asignada = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'notario'
