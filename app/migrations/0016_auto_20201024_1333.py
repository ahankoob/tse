# Generated by Django 3.1.1 on 2020-10-24 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20201024_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbols_info',
            name='baseVol',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=8),
        ),
    ]