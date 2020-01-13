from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    Currencies = (
        (1, 'USD'),
        (2, 'RUB')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128, blank=True, null=True)
    money = models.FloatField(blank=True, default=0)
    currency = models.PositiveSmallIntegerField(choices=Currencies, default=1)
    name = models.CharField(max_length=64, blank=True, null=True)
    surname = models.CharField(max_length=64, blank=True, null=True)
    fatherName = models.CharField(max_length=64, blank=True, null=True)
    birthDate = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Package(models.Model):
    Types = (
        (1, 'Bronze'),
        (2, 'Silver'),
        (3, 'Gold'),
        (4, 'Platinum'),
        (5, 'Vip'),
    )
    Controls = (
        (1, 'Robot'),
        (2, 'Person')
    )
    Statuses = (
        (1, 'Active'),
        (2, 'Finished')
    )
    name = models.CharField(max_length=64)
    status = models.PositiveSmallIntegerField(choices=Statuses)
    type = models.PositiveSmallIntegerField(choices=Types)
    control = models.PositiveSmallIntegerField(choices=Controls)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    capital = models.IntegerField()
    dailyProfit = models.FloatField()
    startDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    amount = models.FloatField()
    sender = models.CharField(max_length=128)
    paymentSystem = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True)
    recipient = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipient
