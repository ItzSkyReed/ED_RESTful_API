from rest_framework import serializers

from app.models import Guest, Room, Booking


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingGetSerializer(serializers.ModelSerializer):
    guest_email = serializers.EmailField(source='guest.email', read_only=True)  # Email гостя из его таблицы
    room_number = serializers.IntegerField(source='room.room_number', read_only=True)  # Номер комнаты из таблицы

    class Meta:
        model = Booking
        exclude = ['guest', 'room']  # Исключаем поля guest и room


class BookingRequestSerializer(serializers.Serializer):
    guest_email = serializers.EmailField(required=True)
    room_number = serializers.IntegerField(required=True)
    check_in = serializers.DateField(format='%Y-%m-%d', required=True)
    check_out = serializers.DateField(format='%Y-%m-%d', required=True)

