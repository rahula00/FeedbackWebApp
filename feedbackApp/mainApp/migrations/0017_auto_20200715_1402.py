# Generated by Django 3.0.7 on 2020-07-15 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0016_feedback_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='salesforceOp',
            field=models.CharField(blank=True, default='N/A', max_length=100, null=True),
        ),
    ]
