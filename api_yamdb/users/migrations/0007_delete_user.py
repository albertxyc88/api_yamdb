# Generated by Django 2.2.16 on 2022-08-01 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_confirmation_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]