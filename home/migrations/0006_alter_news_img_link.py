# Generated by Django 4.2.13 on 2024-06-26 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_link_news_news_link_news_img_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='img_link',
            field=models.CharField(max_length=100),
        ),
    ]