from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    SEATING_CHOICES = (
        (2, '2 persons'),
        (3, '3 persons'),
        (6, '6 persons'),
    )

    table_id = models.CharField(max_length=20, unique=True)
    seating_capacity = models.IntegerField(choices=SEATING_CHOICES)
    is_reserved = models.BooleanField(default=False)

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100)

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
