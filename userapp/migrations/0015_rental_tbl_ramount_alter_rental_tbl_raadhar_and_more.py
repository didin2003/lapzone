# Generated by Django 4.2 on 2025-02-28 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0014_alter_rental_tbl_raadhar_alter_rental_tbl_rmobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='rental_tbl',
            name='ramount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rental_tbl',
            name='raadhar',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='rental_tbl',
            name='rmobile',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='rental_tbl',
            name='rmonths',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='rental_tbl',
            name='rname',
            field=models.CharField(default='Unknown', max_length=50),
        ),
    ]
