# Generated by Django 2.2.24 on 2022-02-16 15:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0082_extend_facility_claim_facility_type_field_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilityindex',
            name='facility_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(help_text='ExtendedField for facility type.', max_length=200), default=list, size=None),
        ),
        migrations.AddField(
            model_name='facilityindex',
            name='native_language_name',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(help_text='ExtendedField for native language name.', max_length=2000), default=list, size=None),
        ),
        migrations.AddField(
            model_name='facilityindex',
            name='number_of_workers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(help_text='ExtendedField for number of workers.', max_length=200), default=list, size=None),
        ),
        migrations.AddField(
            model_name='facilityindex',
            name='parent_company_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(help_text='ExtendedField for parent_company_id.'), default=list, size=None),
        ),
        migrations.AddField(
            model_name='facilityindex',
            name='parent_company_name',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(help_text='ExtendedField for parent company.', max_length=200), default=list, size=None),
        ),
        migrations.AddField(
            model_name='facilityindex',
            name='processing_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(help_text='ExtendedField for processing type.', max_length=200), default=list, size=None),
        ),
        migrations.AddField(
            model_name='facilityindex',
            name='product_type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(help_text='ExtendedField for product type.', max_length=200), default=list, size=None),
        ),
    ]