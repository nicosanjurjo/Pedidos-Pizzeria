# Generated by Django 5.0.7 on 2024-07-30 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zonas', '0004_rename_costoenvio_zona_costo'),
    ]

    operations = [
        migrations.AddField(
            model_name='zona',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]
