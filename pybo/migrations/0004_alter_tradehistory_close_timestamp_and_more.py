# Generated by Django 4.2.11 on 2024-05-13 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0003_alter_tradehistory_close_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradehistory',
            name='close_timestamp',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='tradehistory',
            name='open_timestamp',
            field=models.PositiveBigIntegerField(),
        ),
    ]
