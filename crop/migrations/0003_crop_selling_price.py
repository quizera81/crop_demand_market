# Generated by Django 4.0.6 on 2022-08-15 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crop', '0002_crop_production_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='selling_price',
            field=models.FloatField(default=0),
        ),
    ]