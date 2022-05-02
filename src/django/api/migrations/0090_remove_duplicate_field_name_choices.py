# Generated by Django 2.2.24 on 2022-05-05 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0089_reprocess_parent_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendedfield',
            name='field_name',
            field=models.CharField(choices=[('name', 'name'), ('address', 'address'), ('number_of_workers', 'number_of_workers'), ('native_language_name', 'native_language_name'), ('facility_type', 'facility_type'), ('processing_type', 'processing_type'), ('product_type', 'product_type'), ('parent_company', 'parent_company')], help_text='The name of the field, chosen from a strict list.', max_length=200),
        ),
        migrations.AlterField(
            model_name='historicalextendedfield',
            name='field_name',
            field=models.CharField(choices=[('name', 'name'), ('address', 'address'), ('number_of_workers', 'number_of_workers'), ('native_language_name', 'native_language_name'), ('facility_type', 'facility_type'), ('processing_type', 'processing_type'), ('product_type', 'product_type'), ('parent_company', 'parent_company')], help_text='The name of the field, chosen from a strict list.', max_length=200),
        ),
    ]
