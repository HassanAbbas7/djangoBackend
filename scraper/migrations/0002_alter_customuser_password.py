# Generated by Django 4.1.7 on 2023-04-06 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scraper", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="password",
            field=models.CharField(max_length=200),
        ),
    ]
