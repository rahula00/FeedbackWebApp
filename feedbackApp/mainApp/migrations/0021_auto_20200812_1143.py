# Generated by Django 3.0.7 on 2020-08-12 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0020_auto_20200812_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='feedback',
            field=models.CharField(max_length=500),
        ),
    ]
