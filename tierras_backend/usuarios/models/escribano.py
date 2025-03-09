from django.db import models

class Escribano(models.Model):
    escribano_id = models.AutoField(primary_key=True)
    tribunal = models.CharField(max_length=255, blank=True, null=True)
    numero_registro = models.CharField(max_length=255, blank=True, null=True)
    notaria_asignada = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'escribano'
