# Generated by Django 2.2 on 2021-06-27 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoginReg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]