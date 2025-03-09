from django.db import models

# Create your models here.
class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    id_escritura = models.ForeignKey('escrituras.Escritura', models.DO_NOTHING, null = True)
    user_sender = models.CharField(max_length= 255, blank=True, null=True)
    user_receiver = models.CharField(max_length= 255, blank=True, null=True)
    
    
    class Meta:
        managed = True
        db_table = 'notificacion'
