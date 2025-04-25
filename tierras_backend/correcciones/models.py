from django.db import models

# Create your models here.
class Correcion(models.Model):
    id_correcion = models.AutoField(primary_key=True)
    id_notificacion = models.ForeignKey('notificaciones.Notificacion', models.DO_NOTHING, null=True)
    line_number = models.IntegerField()
    start_position = models.IntegerField()
    end_position = models.IntegerField()
    is_resolved = models.BooleanField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        managed = True
        db_table= 'correccion'

    def __str__(self):
        return f'Corrección {self.id_correcion}'
