# Generated by Django 5.1.2 on 2024-10-31 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0007_alter_stock_cantidad_masas'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stock',
            new_name='StockGeneral',
        ),
        migrations.RenameField(
            model_name='stockgeneral',
            old_name='cantidad_masas',
            new_name='cantidad',
        ),
    ]
