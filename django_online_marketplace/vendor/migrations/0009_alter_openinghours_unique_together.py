# Generated by Django 4.2.6 on 2023-11-13 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0008_alter_openinghours_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='openinghours',
            unique_together={('vendor', 'day', 'from_hour', 'to_hour')},
        ),
    ]