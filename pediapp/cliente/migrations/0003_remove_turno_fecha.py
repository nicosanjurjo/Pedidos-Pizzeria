# Generated by Django 5.0.7 on 2024-07-22 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_turno_alter_pedido_horario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='turno',
            name='fecha',
        ),
    ]
