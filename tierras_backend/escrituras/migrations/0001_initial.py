# Generated by Django 5.1.5 on 2025-02-03 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Escritura',
            fields=[
                ('numero_escritura', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('nombre_notaria', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_otorgamiento', models.DateField(blank=True, null=True)),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('municipio', models.CharField(blank=True, max_length=255, null=True)),
                ('descripcion_movimiento', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_predio', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion_smart_contract', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'escritura',
                'managed': False,
            },
        ),
    ]
