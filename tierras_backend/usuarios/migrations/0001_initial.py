# Generated by Django 5.1.5 on 2025-02-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Escribano',
            fields=[
                ('escribano_id', models.AutoField(primary_key=True, serialize=False)),
                ('tribunal', models.CharField(blank=True, max_length=255, null=True)),
                ('numero_registro', models.CharField(blank=True, max_length=255, null=True)),
                ('notaria_asignada', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'escribano',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Juez',
            fields=[
                ('juez_id', models.AutoField(primary_key=True, serialize=False)),
                ('tribunal', models.CharField(blank=True, max_length=255, null=True)),
                ('nivel_jurisdiccional', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'juez',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Notario',
            fields=[
                ('notario_id', models.AutoField(primary_key=True, serialize=False)),
                ('numero_licencia', models.CharField(blank=True, max_length=255, null=True)),
                ('oficina_registro', models.CharField(max_length=255)),
                ('notaria_asignada', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'notario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('rol_id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'rol',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('cedula', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('hash_password', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('primer_apellido', models.CharField(blank=True, max_length=255, null=True)),
                ('segundo_apellido', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_expedicion_cedula', models.DateField(blank=True, null=True)),
                ('numero_telefono', models.CharField(blank=True, max_length=255, null=True)),
                ('correo_electronico', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'usuario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsuarioRol',
            fields=[
                ('usuario_rol_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'usuario_rol',
                'managed': False,
            },
        ),
    ]
