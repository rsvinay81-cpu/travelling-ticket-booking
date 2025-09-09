
from django.urls import path
from.views import Registerview, LoginView, BusListCreateView,UserBookingView, BookingView

urlpatterns = [
    path('buses/',BusListCreateView.as_view(),name='buslist'),
    path('register/',Registerview.as_view(), name= 'register'),
    path('login/',LoginView.as_view(), name= 'login'),
    path('user_bookings/',UserBookingView.as_view(), name= 'user_bookings'),
    path('booking/',BookingView.as_view(), name='bookings')
]
