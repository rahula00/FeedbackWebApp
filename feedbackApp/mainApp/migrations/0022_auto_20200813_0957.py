# Generated by Django 3.0.7 on 2020-08-13 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0021_auto_20200812_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
