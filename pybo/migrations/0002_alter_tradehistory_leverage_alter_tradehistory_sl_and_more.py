# Generated by Django 4.2.11 on 2024-05-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradehistory',
            name='leverage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tradehistory',
            name='sl',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tradehistory',
            name='tp',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
