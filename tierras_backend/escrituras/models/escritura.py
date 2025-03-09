from django.db import models


class Escritura(models.Model):
    numero_escritura = models.CharField(primary_key=True, max_length=255)
    proceso_escritura = models.ForeignKey('procesos.Proceso', models.DO_NOTHING, db_column='proceso_escritura', default=1)
    nombre_notaria = models.CharField(max_length=255, blank=True, null=True)
    fecha_otorgamiento = models.DateField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    municipio = models.CharField(max_length=255, blank=True, null=True)
    descripcion_movimiento = models.CharField(max_length=255, blank=True, null=True)
    direccion_predio = models.CharField(max_length=255, blank=True, null=True)
    direccion_smart_contract = models.CharField(max_length=255, blank=True, null=True)
    direccion_temporal_data = models.CharField(max_length=255, blank=True, null=True)
    cedula_catastral = models.CharField(max_length=255, blank=True, null=True) 

    class Meta:
        managed = True
        db_table = 'escritura'
