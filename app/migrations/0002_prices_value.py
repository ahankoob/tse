# Generated by Django 3.1.1 on 2020-09-30 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prices',
            name='value',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=15),
        ),
    ]
