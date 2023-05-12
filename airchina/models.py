from django.db import models
from datetime import datetime
from django.urls import reverse


class Airports(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    time_zone = models.CharField(max_length=20)


class Aircraft(models.Model):
    type = models.CharField(max_length=20)
    tail_number = models.CharField(max_length=20)
    capability = models.IntegerField(default=100)
    seats = models.IntegerField(default=100)



class Flight(models.Model):
    flight_num = models.CharField(max_length=100)
    aircraft = models.ForeignKey(to=Aircraft, on_delete=models.CASCADE, default='')
    departure_time = models.DateTimeField(default=datetime.now)
    date = models.DateTimeField(default=datetime(2023, 5, 12, 00, 00, 00, 00).date())
    arrival_time = models.DateTimeField(default=datetime.now)
    # duration = models.TimeField()
    departure_airport = models.ForeignKey(to=Airports, related_name='departing_flights', on_delete=models.CASCADE,
                                          default='')
    arrival_airport = models.ForeignKey(to=Airports, related_name='arriving_flights', on_delete=models.CASCADE,
                                        default='')
    price = models.IntegerField() #economy_class_price class A
    price_business= models.IntegerField() #business_class_price
    price_first = models.IntegerField()#first_class_price class C
    # airline_company = models.CharField(max_length=255)
    #capability = models.IntegerField(default=100)
    airline_company_name = models.CharField(max_length=100,default='airchina')


class Passengers(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    nationality = models.CharField(max_length=20)
    passport_num = models.CharField(max_length=20)



class Bookings(models.Model):
    booking_num = models.CharField(max_length=20)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, default='')
    num_ticket = models.IntegerField()
    price = models.IntegerField()
    status = models.CharField(max_length=20)
    datetime = models.DateTimeField(default=datetime.now())


class PassengersBookings(models.Model):
    passengers = models.ForeignKey('Passengers', on_delete=models.CASCADE, default='')
    booking = models.ForeignKey('Bookings', on_delete=models.CASCADE, default='')


class PaymentProvider(models.Model):
    name = models.CharField(max_length=50)
    web_address = models.CharField(max_length=100)
    airline_login_name = models.CharField(max_length=100)
    airline_login_password = models.CharField(max_length=100)


class Invoices(models.Model):
    invoice_num = models.CharField(max_length=20)
    booking = models.ForeignKey(to=Bookings,on_delete=models.CASCADE)
    payment_provider_id = models.ForeignKey(to=PaymentProvider, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    date_time = models.DateTimeField()
    stamp = models.CharField(max_length=20)
