from django.db import models

class Juez(models.Model):
    juez_id = models.AutoField(primary_key=True)
    tribunal = models.CharField(max_length=255, blank=True, null=True)
    nivel_jurisdiccional = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'juez'
