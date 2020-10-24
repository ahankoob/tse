# Generated by Django 3.1.1 on 2020-10-24 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20201024_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbols_info',
            name='MaxWeek',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='MaxYear',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='MinWeek',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='MinYear',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='baseVol',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='eps',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='group_pe',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='maxValidPrice',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='minValidPrice',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='monthlyAvgVol',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='pe',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='symbols_info',
            name='sahamCount',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=20),
        ),
    ]
