# from django.contrib.auth import authenticate
# from rest_framework import viewsets
# from .models import Table, Reservation
# from .serializers import TableSerializer, ReservationSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from datetime import datetime
# from rest_framework.decorators import action
# from rest_framework import status
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from django.db.models import Q
#
#
# class RegisterUserView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         phone_number = request.data.get('phone_number')
#         name = request.data.get('name')
#
#         if not email or not password or not phone_number or not name:
#             return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = User.objects.create_user(username=email, email=email, password=password)
#         user.phone_number = phone_number
#         user.name = name
#         user.save()
#
#         return Response({'message': 'User registered successfully'})
#
#
# class UserLoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         if not email or not password:
#             return Response({'error': 'Both email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = authenticate(username=email, password=password)
#
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#
# class TableViewSet(viewsets.ModelViewSet):
#     queryset = Table.objects.all()
#     serializer_class = TableSerializer
#
# class ReservationViewSet(viewsets.ModelViewSet):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#
#
# class AvailableTablesView(APIView):
#     def get(self, request):
#         date = request.query_params.get('date')
#         time = request.query_params.get('time')
#
#         if not date or not time:
#             return Response({'error': 'Both date and time parameters are required'}, status=400)
#
#         try:
#             datetime_obj = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
#         except ValueError:
#             return Response({'error': 'Invalid date or time format'}, status=400)
#
#         available_tables = Table.objects.filter(is_reserved=False)
#
#         reservations = Reservation.objects.filter(date=date, time=time)
#         reserved_table_ids = reservations.values_list('table__id', flat=True)
#
#         available_tables = available_tables.exclude(id__in=reserved_table_ids)
#
#         return Response(TableSerializer(available_tables, many=True).data)
#
#
# class ReservationViewSet(viewsets.ModelViewSet):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#
#     @action(detail=False, methods=['post'])
#     def reserve_table(self, request):
#         table_id = request.data.get('table_id')
#         date = request.data.get('date')
#         time = request.data.get('time')
#
#         # Check if the table is available for reservation
#         table = Table.objects.get(id=table_id)
#         if table.is_reserved:
#             return Response({'error': 'Table is already reserved'}, status=400)
#
#         # Create new reservation
#         reservation = Reservation.objects.create(user=request.user, table=table, date=date, time=time)
#         table.is_reserved = True
#         table.save()
#
#         return Response({'message': 'Table reserved successfully'})
#
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .jwt_utils import create_jwt_token
from .models import Table, Reservation, Profile
from .serializers import TableSerializer, ReservationSerializer, ReservationUpdateSerializer, ProfileSerializer


class TableList(APIView):
    def get(self, request):
        # Получаем все доступные столики, которые не заняты
        tables = Table.objects.filter(is_reserved=False)

        # Создаем список доступных столов
        available_tables = []
        for table in tables:
            table_data = {
                'table_id': table.table_id,
                'seating_capacity': table.seating_capacity,
            }
            available_tables.append(table_data)

        return Response(available_tables)


class ReservationList(APIView):
    def post(self, request):
        table_id = request.data.get('table_id')
        date = request.data.get('date')
        time = request.data.get('time')

        table = Table.objects.get(pk=table_id)

        existing_reservation = Reservation.objects.filter(table=table, date=date, start_time=time).first()
        if existing_reservation:
            return Response("Table already reserved for this date and time", status=status.HTTP_400_BAD_REQUEST)

        if table.is_reserved:
            return Response("Table already reserved", status=status.HTTP_400_BAD_REQUEST)

        # Make reservation logic

        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            table.is_reserved = True
            table.save()
            return Response("Reservation successful", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Регистрация пользователя
@api_view(['POST'])
def register_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        name = request.data.get('name')

        user = User.objects.create_user(username=email, email=email, password=password)
        profile = Profile.objects.create(user=user, phone_number=phone_number, name=name)

        token = create_jwt_token(user.id)
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Авторизация пользователя
@api_view(['POST'])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            token = create_jwt_token(user.id)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Отмена бронирования
class TableList(APIView):
    def get(self, request):
        try:
            self.client.force_authenticate(user=request.user)
            # Получаем все доступные столики, которые не заняты
            tables = Table.objects.filter(is_reserved=False)

            # Создаем список доступных столов
            available_tables = []
            for table in tables:
                table_data = {
                    'table_id': table.table_id,
                    'seating_capacity': table.seating_capacity,
                }
                available_tables.append(table_data)

            return Response(available_tables)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Изменение бронирования
@api_view(['PUT'])
def update_reservation(request):
    table_id = request.data.get('table_id')
    new_date = request.data.get('date')
    new_start_time = request.data.get('start_time')
    new_end_time = request.data.get('end_time')

    reservation = Reservation.objects.get(table_id=table_id)
    if (reservation.date - timezone.now().date()).days > 1:
        serializer = ReservationUpdateSerializer(reservation, data={'date': new_date, 'start_time': new_start_time,
                                                                'end_time': new_end_time})

        if serializer.is_valid():
            serializer.save()
            return Response("Reservation updated successfully", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Unable to update reservation less than 1 day before booking date", status=status.HTTP_400_BAD_REQUEST)