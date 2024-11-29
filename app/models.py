import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import QuerySet


class Guest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16)

    def __str__(self):
        return f"Guest <{self.first_name} {self.last_name}>"


class Room(models.Model):
    room_number = models.IntegerField(unique=True)
    room_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Room <{self.room_number} {self.room_type}, price: {self.price}₽>)"

class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"Booking \"{self.id}\" for {self.guest} in Room {self.room.room_number} from {self.check_in} to {self.check_out}"

    @classmethod
    def create_booking(cls, guest_email: str, room_num: int, check_in: datetime.date, check_out: datetime.date):
        try:
            guest = Guest.objects.get(email=guest_email)

            room = Room.objects.get(room_number=room_num)

            # Проверка, не пересекаются ли даты с уже существующими бронированиями
            overlapping_bookings = cls.objects.filter(
                room=room,
                check_in__lte=check_out,  # Начало бронирования не позднее конца запрашиваемого
                check_out__gte=check_in  # Конец бронирования не раньше начала запрашиваемого
            )

            # Если есть пересекающиеся бронирования
            if overlapping_bookings.exists():
                raise ValueError(f"Room {room_num} is already booked for the selected dates.")

            # Если дат пересечения нет, создаем новое бронирование
            booking = cls.objects.create(
                guest=guest,
                room=room,
                check_in=check_in,
                check_out=check_out
            )

            return booking  # возвращаем объект нового бронирования

        except ObjectDoesNotExist:
            raise ValueError("Guest or Room not found.")
        except ValueError as ve:
            raise ve

    @classmethod
    def get_guest_bookings(cls, guest_email: str) -> QuerySet["Booking"] | QuerySet["Booking", ...]:
        try:
            guest = Guest.objects.get(email=guest_email)

            bookings = cls.objects.filter(guest=guest)

            return bookings

        except Guest.DoesNotExist:
            return cls.objects.none()


