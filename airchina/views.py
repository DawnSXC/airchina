import requests
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .models import *

import datetime

@csrf_exempt
def find_flight(request):
    if request.method == 'GET':
        # requestParam = json.loads(request.body)
        flag = request.GET.get("arrival_airport") and request.GET.get("departure_airport") \
               and request.GET.get("date")
        if flag:
            arrivalAirportName = request.GET.get("arrival_airport")
            departureAirportName = request.GET.get("departure_airport")
            date = request.GET.get("date")  # 2023/05/11
            # reformat:2023-05-11
            #date_reformat = date.replace("/", "-")
            datelist= date.split("/")
            date_start= datetime.date(int(datelist[0]), int(datelist[1]), int(datelist[2]))
            date_end = datetime.date(int(datelist[0]), int(datelist[1]), int(datelist[2])+1)
            print(date_start)
            print(date_end)
            #print(date_reformat)
            arrivalAirport = Airports.objects.get(name=arrivalAirportName)
            departureAirport = Airports.objects.get(name=departureAirportName)

            flights = Flight.objects.filter(
                arrival_airport=arrivalAirport.id,
                departure_airport=departureAirport.id,
                departure_time__range=[date_start,date_end]
            )
            results = []

            for flight in flights:
                if flight.aircraft.seats > 0:
                    #print(str(flight.departure_time.year)+"-"+str(flight.departure_time.month)+"-"+str(flight.departure_time.day))
                    result = {
                        'company_name': flight.airline_company_name,
                        'flight_num': flight.flight_num,
                        'arrival_airport': flight.arrival_airport.name,
                        'departure_airport': flight.departure_airport.name,
                        'departure_datetime': flight.departure_time,
                        'arrival_datetime': flight.arrival_time,
                        'price': str(flight.price) + "/" + str(flight.price_business) + "/" + str(flight.price_first),
                        'remaining_seats': flight.aircraft.seats,
                        'capability':flight.aircraft.capability
                    }
                results.append(result)
            if results:
                return JsonResponse(results, safe=False)
            else:
                return JsonResponse({'message': 'No flights found.'}, status=200, content_type='text/plain')
        else:
            return JsonResponse({"message": "Missing Flights' Information."}, status=200)
    else:
        return JsonResponse({'message': 'Request Error.'}, status=500, content_type='text/plain')


@require_GET
def payment_methods(request):
    if request.method == 'GET':
        payment_providers = PaymentProvider.objects.all()
        results = []
        for payment_provider in payment_providers:
            provider = {
                'payment_provider_name': payment_provider.name,
                'payment_provider_id': payment_provider.id
            }
            results.append(provider)
        if results:
            return JsonResponse(results, safe=False)
        else:
            return JsonResponse({'message': 'No provider found.'}, status=200, content_type='text/plain')
    else:
        return JsonResponse({'message': 'Request Error.'}, status=500, content_type='text/plain')


@require_POST
@csrf_exempt
def bookflight(request):
    if request.method == "POST":
        requestParam = json.loads(request.body)
        flag = requestParam.get("flight_num") and requestParam.get("passenger") and requestParam.get(
            "seats_num") and requestParam.get("seats_class")
        if flag:
            flight_num = requestParam["flight_num"]
            passenger = requestParam["passenger"]
            seats_num = int(requestParam["seats_num"])
            seats_class = requestParam["seats_class"]

            flight = Flight.objects.get(flight_num=flight_num)
            if seats_num > flight.aircraft.seats:
                return JsonResponse({"message": "Not enough seats left."}, status=500, content_type='text/plain')
            if seats_num != len(passenger):
                return JsonResponse({"message": "Missing passengers' information."}, status=500, content_type='text/plain')
            flight.aircraft.seats = flight.aircraft.seats - seats_num
            flight.save()
            if seats_class == 'Economy':
                price = flight.price * seats_num
            if seats_class == 'Business':
                price = flight.price_business * seats_num
            if seats_class == 'First':
                price = flight.price_first * seats_num
            booking_num = flight.airline_company_name+"-"+str(uuid.uuid1())[0:5]
            add_booking = Bookings(booking_num=booking_num, flight=flight, num_ticket=seats_num, price=price,
                                   status="ON_HOLD", datetime=datetime.datetime.now())
            add_booking.save()
            booking = Bookings.objects.get(booking_num=booking_num)
            for item in passenger:
                if Passengers.objects.filter(passport_num=item[0]):
                    print(item[0])
                    passengers = Passengers.objects.get(passport_num=item[0])
                    add_passengersbookings = PassengersBookings(passengers=passengers, booking=booking)
                    add_passengersbookings.save()
                else:
                    print("=+++")
                    new_pass = Passengers(passport_num=item[0], name=item[1], gender=item[2], nationality=item[3])
                    new_pass.save()
                    add_passengersbookings = PassengersBookings(passengers=new_pass, booking=booking)
                    add_passengersbookings.save()

            return JsonResponse({"booking_num": booking.booking_num, "booking_status": booking.status,
                                 "total_price": booking.price}, status=200, content_type='text/plain')
        else:
            return JsonResponse({"message": "Incomplete information! Can not generate a booking."}, status=200,
                                content_type='text/plain')


@csrf_exempt
def payforbooking(request):
    if request.method == 'POST':
        requestParam = json.loads(request.body)
        if requestParam.get("booking_number") and requestParam.get("payment_provider_name"):
            booking_number = requestParam["booking_number"]
            payment_provider_name = requestParam["payment_provider_name"]
            payment_provider = PaymentProvider.objects.get(name=payment_provider_name)
            booking = Bookings.objects.get(booking_num=booking_number)
            price = booking.price
            airline_login_name = payment_provider.airline_login_name
            if payment_provider_name == "PayPal":
                url = 'http://arinnnnnn.pythonanywhere.com/createinvoice/'
            elif payment_provider_name == "WeChat Pay":
                url = 'http://sc19jz2.pythonanywhere.com/createinvoice/'
            elif payment_provider_name == "Alipay":
                url = 'http://sc19wc.pythonanywhere.com/createinvoice/'
            elif payment_provider_name == "Apple Pay":
                url = 'http://arinnnnnn.pythonanywhere.com/createinvoice/'
            else:
                return JsonResponse({'message': 'No Provider Found.'}, status=500, content_type='text/plain')

            resPayment = requests.post(url, json={"booking_number": booking_number,
                                                  "payment_provider_name": payment_provider_name,
                                                  "amount": price, "receiver_account_number": airline_login_name})
            resPayment = resPayment.json()
            invoice_num = resPayment["invoice_num"]
            stamp = resPayment["stamp"]
            datetime = resPayment["create_time"]
            invoice = Invoices(invoice_num=invoice_num, booking=booking, status=booking.status, date_time=datetime,
                               stamp=stamp, payment_provider_id=payment_provider)
            invoice.save()
            return JsonResponse({"invoice_num": invoice.invoice_num, "booking_status": booking.status,
                                 "price": price, "datetime": invoice.date_time, "booking_num": booking_number,
                                 "payment_provider_name": payment_provider.name}, status=200, content_type='text/plain')
        else:
            return JsonResponse({"message": "Missing information about payment."}, status=500,
                                content_type='text/plain')
    else:
        return JsonResponse({'message': 'Request Error.'}, status=500, content_type='text/plain')


@csrf_exempt
def bookingstatus(request):
    if request.method == 'POST':
        requestParam = json.loads(request.body)
        flag = requestParam.get("booking_number")
        if flag:
            booking_number = requestParam["booking_number"]
            booking = Bookings.objects.get(booking_num=booking_number)
            if booking:
                return JsonResponse({"booking_status": booking.status,
                                     "booking_num": booking.booking_num,
                                     "flight_num": booking.flight.flight_num,
                                     "booking_datetime": booking.datetime,
                                     "price": booking.price},
                                    status=200, safe=False)
            else:
                return JsonResponse({"message": "No booking found!"}, status=200, content_type='text/plain')
        else:
            return JsonResponse({"message": "Missing booking information!"}, status=500, content_type='text/plain')
    else:
        return JsonResponse({'message': 'Request Error.'}, status=500, content_type='text/plain')


@csrf_exempt
def cancelbooking(request):
    if request.method == 'POST':
        requestParam = json.loads(request.body)
        booking_number = requestParam["booking_number"]
        if not booking_number:
            return JsonResponse({"message": "Incomplete booking information!"}, status=500, )
        booking = Bookings.objects.get(booking_num=booking_number)
        if booking:
            booking.status = 'CANCELLED'
            booking.save()
            return JsonResponse({"booking_status": booking.status, "booking_number": booking_number}, safe=False)
        else:
            return JsonResponse({'message': 'No booking found.'}, status=200, content_type='text/plain')
    else:
        return JsonResponse({'message': 'Request Error.'}, status=500, content_type='text/plain')


@csrf_exempt
def finalizebooking(request):
    if request.method == "POST":
        requestParam = json.loads(request.body)
        flag = requestParam.get("booking_num") and requestParam.get("invoice_num") and requestParam.get("stamp")
        if flag:
            booking_num = requestParam["booking_num"]
            invoice_num = requestParam["invoice_num"]
            stamp = requestParam["stamp"]
            booking = Bookings.objects.get(booking_num=booking_num)
            invoice = Invoices.objects.get(invoice_num=invoice_num)
            invoice_stamp = invoice.stamp
            if stamp == invoice_stamp:
                invoice.status = "PAID"
                invoice.save()
                booking = Bookings.objects.get(booking_num=booking_num)
                booking.status = " FINISHED"
                booking.save()
                return JsonResponse({"booking_num": booking_num, "booking_status": booking.status}, status=200,
                                    content_type='text/plain')
            else:
                return JsonResponse({"message": "Wrong stamp."}, status=200, content_type='text/plain')
        else:
            return JsonResponse({"message": "Incomplete information!"}, status=500, content_type='text/plain')
    else:
        return JsonResponse({'message': 'Request Error.'}, status=500, content_type='text/plain')
