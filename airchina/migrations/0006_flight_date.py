# Generated by Django 4.1 on 2023-05-11 17:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airchina", "0005_remove_flight_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="flight",
            name="date",
            field=models.DateTimeField(default=datetime.date(2023, 5, 12)),
        ),
    ]
