# Generated by Django 4.2.6 on 2023-10-14 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[('1', 'Vendor'), ('2', 'Customer')], null=True),
        ),
    ]
