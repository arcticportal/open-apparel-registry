# Generated by Django 2.2.24 on 2022-06-21 16:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0092_add_sector_to_facility_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityclaim',
            name='sector',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, help_text='The sector(s) for goods made at the facility', null=True, size=None),
        ),
        migrations.AddField(
            model_name='historicalfacilityclaim',
            name='sector',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, help_text='The sector(s) for goods made at the facility', null=True, size=None),
        ),
    ]
