# """
# URL configuration for restaurant_reservation_project project.
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.urls import path
# from rest_framework.routers import DefaultRouter
# from reservations.views import TableViewSet, ReservationViewSet, AvailableTablesView, RegisterUserView, UserLoginView
#
# router = DefaultRouter()
# router.register(r'tables', TableViewSet)
# router.register(r'reservations', ReservationViewSet)
#
# urlpatterns = [
#     path('register/', RegisterUserView.as_view(), name='register'),
#     path('login/', UserLoginView.as_view(), name='login'),
#     path('available-tables/', AvailableTablesView.as_view(), name='available-tables'),
# ]
#
# urlpatterns += router.urls

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
