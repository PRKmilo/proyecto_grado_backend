from django.db import models


class  RolesVerificadores(models.Model):
    id_registro_validadores = models.AutoField(primary_key=True)
    id_escritura = models.ForeignKey('Escritura', models.DO_NOTHING, null =True)
    id_escribano = models.CharField(max_length=255, blank=True, null=True)
    id_juez1 = models.CharField(max_length=255, blank=True, null=True)
    id_notario = models.CharField(max_length=255, blank=True, null=True)
    id_juez2 = models.CharField(max_length=255, blank=True, null=True) 
    
    class Meta:
        managed = True
        db_table = 'roles_verificadores'
