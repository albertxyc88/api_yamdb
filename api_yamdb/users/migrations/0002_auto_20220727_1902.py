# Generated by Django 2.2.16 on 2022-07-27 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('USER', 'USER'), ('MODERATOR', 'MODERATOR'), ('ADMIN', 'ADMIN')], default='USER', max_length=20),
        ),
    ]
