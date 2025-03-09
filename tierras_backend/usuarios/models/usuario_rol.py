from django.db import models



class UsuarioRol(models.Model):
    usuario_rol_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, null=True)
    rol = models.ForeignKey('Rol', models.DO_NOTHING, default = 1)
    juez = models.ForeignKey('Juez', models.DO_NOTHING, blank=True, null=True)
    escribano = models.ForeignKey('Escribano', models.DO_NOTHING, blank=True, null=True)
    notario = models.ForeignKey('Notario', models.DO_NOTHING, blank=True, null=True)
    beneficiario = models.ForeignKey('Beneficiario', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'usuario_rol'
