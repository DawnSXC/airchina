# Generated by Django 4.1 on 2023-05-11 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airchina", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="aircraft", name="capability",),
        migrations.RemoveField(model_name="flight", name="capability",),
    ]
