from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Guest, Room, Booking
from .serializers import GuestSerializer, RoomSerializer, BookingSerializer, BookingRequestSerializer, BookingGetSerializer


class GuestListView(APIView):
    @swagger_auto_schema(
        operation_description="Получить список всех гостей",
        responses={
            200: GuestSerializer(many=True),
        }
    )
    def get(self, request: Request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Создать нового гостя",
        request_body=GuestSerializer,
        responses={
            201: GuestSerializer,
            400: openapi.Response(description="Неправильный ввод данных"),
        }
    )
    def post(self, request: Request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuestDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Получить гостя по id",
        responses={
            200: GuestSerializer,
            404: openapi.Response(description="Гость не найден"),
        }
    )
    def get(self, request: Request, pk: int):
        guest = Guest.objects.filter(pk=pk).first()
        if guest:
            serializer = GuestSerializer(guest)
            return Response(serializer.data)
        return Response({"detail": "Не найдено."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Обновить данные существующего гостя",
        request_body=GuestSerializer,
        responses={
            200: GuestSerializer,
            404: openapi.Response(description="Гость не найден"),
        }
    )
    def put(self, request: Request, pk: int):
        guest = Guest.objects.filter(pk=pk).first()
        if not guest:
            return Response({"detail": "Не найдено."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Удаление существующего гостя",
        responses={
            204: openapi.Response(description="Гость успешно удален"),
            404: openapi.Response(description="Гость не найден"),
        }
    )
    def delete(self, request: Request, pk: int):
        guest = Guest.objects.filter(pk=pk).first()
        if not guest:
            return Response({"detail": "Не найдено."}, status=status.HTTP_404_NOT_FOUND)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GuestByEmailView(APIView):
    @swagger_auto_schema(
        operation_description="Получить гостя по E-mail",
        responses={
            200: GuestSerializer,
            404: openapi.Response(description="Гость не найден"),
        }
    )
    def get(self, request: Request, email: str):
        guest = Guest.objects.filter(email=email).first()
        if guest:
            serializer = GuestSerializer(guest)
            return Response(serializer.data)
        return Response({"detail": "Не найдено."}, status=status.HTTP_404_NOT_FOUND)


class RoomListView(APIView):
    @swagger_auto_schema(
        operation_description="Получить список всех комнат",
        responses={
            200: RoomSerializer(many=True),
        }
    )
    def get(self, request: Request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Создать новую комнату",
        request_body=RoomSerializer,
        responses={
            201: RoomSerializer,
            400: openapi.Response(description="Неправильный ввод данных"),
        }
    )
    def post(self, request: Request):
        room = RoomSerializer(data=request.data)
        if room.is_valid():
            room.save()
            return Response(room.data, status=status.HTTP_201_CREATED)
        return Response(room.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailView(APIView):
    @swagger_auto_schema(
        operation_description="Получить комнату по id",
        responses={
            200: RoomSerializer,
            404: openapi.Response(description="Комнаты с таким id"),
        }
    )
    def get(self, request: Request, pk: int):
        room = Room.objects.filter(pk=pk).first()
        if room:
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Обновить данные существующей комнаты",
        request_body=RoomSerializer,
        responses={
            200: RoomSerializer,
            404: openapi.Response(description="Комната не найдена"),
        }
    )
    def put(self, request: Request, pk: int):
        room = Room.objects.filter(pk=pk).first()
        if not room:
            return Response({"detail": "Не найдено."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Удаление существующей комнаты",
        responses={
            204: openapi.Response(description="Комната успешно удалена"),
            404: openapi.Response(description="Комната не найдена"),
        }
    )
    def delete(self, request: Request, pk: int):
        room = Room.objects.filter(pk=pk).first()
        if not room:
            return Response({"detail": "Не найдено."}, status=status.HTTP_404_NOT_FOUND)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomByNumView(APIView):
    @swagger_auto_schema(
        operation_description="Получить комнату по её номеру",
        responses={
            200: RoomSerializer,
            404: openapi.Response(description="Комнаты с таким номером нет"),
        }
    )
    def get(self, request: Request, room_number: int):
        room = Room.objects.filter(room_number=room_number).first()
        if room:
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        return Response({"detail": "Не найдено."}, status=status.HTTP_404_NOT_FOUND)


class BookingFilteredListView(APIView):
    @swagger_auto_schema(
        operation_description="Получить список всех резервирований с обязательной фильтрацией по датам.",
        responses={200: BookingSerializer(many=True)},
        parameters=[
            openapi.Parameter('check_in', openapi.IN_PATH, description="Дата начала бронирования", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('check_out', openapi.IN_PATH, description="Дата окончания бронирования", type=openapi.TYPE_STRING, required=True),
        ]
    )
    def get(self, request, check_in, check_out):
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Неправильный формат даты. Используйте YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if check_out_date < check_in_date:
            return Response({"error": "Дата выезда раньше даты въезда."}, status=status.HTTP_400_BAD_REQUEST)

        # Фильтрация по датам
        bookings = Booking.objects.filter(check_in__gte=check_in_date, check_out__lte=check_out_date)

        # Сериализация и возврат данных
        return Response(BookingGetSerializer(bookings, many=True).data)


class BookingListView(APIView):
    @swagger_auto_schema(
        operation_description="Создать новое резервирование",
        request_body=BookingRequestSerializer,
        responses={201: BookingSerializer, 400: openapi.Response(description="Неправильный ввод данных")}
    )
    def post(self, request: Request):
        serializer = BookingRequestSerializer(data=request.data)
        if serializer.is_valid():
            guest_email = serializer.validated_data['guest_email']
            room_number = serializer.validated_data['room_number']
            check_in = serializer.validated_data['check_in']
            check_out = serializer.validated_data['check_out']

            # Преобразуем строки в даты
            try:
                check_in_date = datetime.strptime(str(check_in), '%Y-%m-%d').date()
                check_out_date = datetime.strptime(str(check_out), '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Неправильный формат даты. Используйте YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

            if check_out_date < check_in_date:
                return Response({"error": "Дата выезда раньше даты въезда."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                booking = Booking.create_booking(guest_email, room_number, check_in_date, check_out_date)
                booking.save()
                return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Получить список всех резервирований",
        responses={200: BookingSerializer(many=True)},
    )
    def get(self, request: Request):
        return Response(BookingGetSerializer(Booking.objects.all(), many=True).data)


class BookingUpdateView(APIView):
    @swagger_auto_schema(
        operation_description="Обновить данные существующей резервации",
        request_body=BookingRequestSerializer,
        responses={
            200: BookingSerializer,
            404: openapi.Response(description="Комната или гость не найдены"),
        }
    )
    def put(self, request, pk: int):
        guest_email = request.data.get('guest_email')
        room_number = request.data.get('room_number')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')

        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Неправильный формат даты. Используйте YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if check_out_date < check_in_date:
            return Response({"error": "Дата выезда раньше даты въезда."}, status=status.HTTP_400_BAD_REQUEST)

        room = Room.objects.filter(room_number=room_number).first()
        if not room:
            return Response({"detail": "Комната не найдена."}, status=status.HTTP_404_NOT_FOUND)

        overlapping_bookings = Booking.objects.filter(
            room=room,
            check_in__lte=check_out,  # Начало бронирования не позднее конца запрашиваемого
            check_out__gte=check_in,  # Конец бронирования не раньше начала запрашиваемого
        )

        if overlapping_bookings.exists():
            return Response(f"Комната {room.room_number} уже забронирована на существующие даты.")

        guest = Guest.objects.filter(email=guest_email).first()
        if not guest:
            return Response({"detail": "Гость не найден."}, status=status.HTTP_404_NOT_FOUND)

        booking = Booking.objects.filter(pk=pk).first()
        if not booking:
            return Response({"detail": "Бронирование не найдено."}, status=status.HTTP_404_NOT_FOUND)

        # Обновляем данные бронирования
        booking.guest = guest
        booking.room = room
        booking.check_in = check_in_date
        booking.check_out = check_out_date
        booking.save()

        return Response(BookingGetSerializer(booking).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Удаление существующего бронирования по id",
        responses={
            204: openapi.Response(description="Комната успешно удалена"),
            404: openapi.Response(description="Комната не найдена"),
        }
    )
    def delete(self, request: Request, pk: int):
        booking = Booking.objects.filter(pk=pk).first()
        if not Booking:
            return Response({"detail": "Не Найдено."}, status=status.HTTP_404_NOT_FOUND)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
