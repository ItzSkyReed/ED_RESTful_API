from django.urls import path

from app.views import *

urlpatterns = [
    path('guests/', GuestListView.as_view(), name='guest-list'),
    path('guests/<int:pk>/', GuestDetailView.as_view(), name='guest-detail'),
    path('guests/email/<str:email>/', GuestByEmailView.as_view(), name='guest-by-email'),

    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/num/<int:room_number>/', RoomByNumView.as_view(), name='room-num'),

    path('bookings/<str:check_in>/<str:check_out>/', BookingFilteredListView.as_view(), name='booking-list'),
    path('bookings/', BookingListView.as_view(), name='create-booking'),
    path('bookings/<int:pk>', BookingUpdateView.as_view(), name='update-booking'),
    path('bookings/<int:pk>', BookingUpdateView.as_view(), name='delete-booking'),
]
