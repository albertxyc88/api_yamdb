# Generated by Django 2.2.16 on 2022-08-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20220801_1835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Биография'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=55, unique=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('USER', 'USER'), ('MODERATOR', 'MODERATOR'), ('ADMIN', 'ADMIN')], default='USER', max_length=20, verbose_name='Роль'),
        ),
    ]
