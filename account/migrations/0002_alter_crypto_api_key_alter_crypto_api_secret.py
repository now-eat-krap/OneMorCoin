# Generated by Django 4.2.11 on 2024-05-11 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='api_key',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='crypto',
            name='api_secret',
            field=models.CharField(max_length=100),
        ),
    ]