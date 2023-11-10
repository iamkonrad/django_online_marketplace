# Generated by Django 4.2.6 on 2023-11-10 19:31

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_alter_vendor_vendor_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='address',
            field=models.CharField(default=123, max_length=300),
        ),
        migrations.AddField(
            model_name='vendor',
            name='city',
            field=models.CharField(default=124, max_length=200),
        ),
        migrations.AddField(
            model_name='vendor',
            name='country',
            field=django_countries.fields.CountryField(default=123, max_length=2),
        ),
        migrations.AddField(
            model_name='vendor',
            name='province',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
