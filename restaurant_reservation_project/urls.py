from django.urls import path
from reservations import views


urlpatterns = [
    path('tables/', views.TableList.as_view(), name='table_list'),
    path('reservations/', views.ReservationList.as_view(), name='reservation_list'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('cancel_reservation/', views.cancel_reservation, name='cancel_reservation'),
    path('update_reservation/', views.update_reservation, name='update_reservation'),
]
