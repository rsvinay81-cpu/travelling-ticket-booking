
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status,generics
from rest_framework.views import APIView
from.serializers import UserRegisterserializer, BusSerializers, BookingSerializers
from rest_framework.response import Response
from.models import Bus, Seat, Booking

class Registerview(APIView):
    def post(self, request):
        serializer = UserRegisterserializer(data= request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username, password = password)

        if user:
            token, reated = Token.objects.get_or_create(user=user)
            return Response({
                'token':token.key,
                'user_id':user.id
            },status= status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        

class BusListCreateView(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializers

class BusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializers

class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seat_id = request.data.get('seat')

        try:
            seat = Seat.objects.get(id = seat_id)
            if Seat.is_booked:
                return Response({'error':'seat already booked'},status=status.HTTP_400_BAD_REQUEST)
            
            seat.is_booked =True
            seat.save()

            bookings = Booking.objects.create(
                user = request.user,
                bus = seat.bus,
                seat = seat
            )
            serializer = BookingSerializers(bookings)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Seat.DoesNotExist:
            return Response({'error':'Invalid Seat ID'},status=status.HTTP_400_BAD_REQUEST)
        
class UserBookingView(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({'error':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
        
        Bookings = Booking.objects.filter(user_id= user_id)
        serializer= BookingSerializers(Bookings, many=True)
        return Response(serializer.data)

            
