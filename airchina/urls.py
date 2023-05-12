from django.urls import path
from .views import *

urlpatterns = [
    path('findflight/', find_flight),
    path('paymentmethods/', payment_methods),
    path('bookflight/', bookflight),
    path('bookingstatus/', bookingstatus),
    path('cancelbooking/', cancelbooking),
    path('finalizebooking/', finalizebooking),
    path('payforbooking/', payforbooking)
]