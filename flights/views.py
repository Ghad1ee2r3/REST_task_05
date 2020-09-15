from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from datetime import datetime
from django.utils import timezone
from .models import Flight, Booking
from rest_framework.permissions import BasePermission
from .serializers import FlightSerializer, BookingSerializer, BookingDetailsSerializer, UpdateBookingSerializer, RegisterSerializer ,UpdateBookingSerializerA
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

class FlightsList(ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class BookingsList(ListAPIView):#edit
    #queryset = Booking.objects.filter(date__gte=datetime.today())
    serializer_class = BookingSerializer
    def get_queryset(self):
        queryset = Booking.objects.filter(user=self.request.user,date__gte=timezone.now())
        return queryset



class BookingDetails(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailsSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'


class UpdateBooking(RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    #serializer_class = UpdateBookingSerializer


    #if serializer_class == IsAdminUser :

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UpdateBookingSerializer
        return UpdateBookingSerializerA
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'



    #    queryset = Booking.objects.all()

    #    serializer_class = UpdateBookingSerializer
    #    lookup_field = 'id'
    #    lookup_url_kwarg = 'booking_id'
    #elif serializer_class == IsAuthenticated :
    #    def partial_update(self, request, *args, **kwargs):
    #        kwargs['partial'] = True
    #        return self.update(request, *args, **kwargs)




class CancelBooking(DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'


class BookFlight(CreateAPIView):
    serializer_class = UpdateBookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, flight_id=self.kwargs['flight_id'])


class Register(CreateAPIView):
    serializer_class = RegisterSerializer
