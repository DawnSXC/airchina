# Generated by Django 4.1 on 2023-05-11 18:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("airchina", "0006_flight_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookings",
            name="datetime",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 5, 12, 2, 37, 39, 837005)
            ),
        ),
    ]