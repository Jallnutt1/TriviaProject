# Generated by Django 2.2 on 2021-06-30 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appTrivia', '0002_auto_20210629_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='player_2_score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
