from django.db import models

class Beneficiario(models.Model):
    beneficiario_id = models.AutoField(primary_key=True)
    municipio_actual = models.CharField(max_length=255, blank=True, null=True)
    departamento_actual = models.CharField(max_length=255, blank=True, null=True)
    grupo_poblacional = models.CharField(max_length=255, blank=True, null=True)
    situacion_despojo = models.CharField(max_length=255, blank=True, null=True)
    documentos_soporte = models.TextField(blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'beneficiario'  # Aquí defines el nombre de la tabla en la base de datos
        managed = True  # Esto indica que Django gestionará la tabla y sus migraciones
