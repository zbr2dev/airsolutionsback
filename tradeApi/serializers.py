from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'password',
            'currency',
            'money',
            'name',
            'surname',
            'fatherName',
            'birthDate',
            'phone',
        ]


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            'id',
            'name',
            'status',
            'type',
            'control',
            'user',
            'capital',
            'dailyProfit',
            'startDate',
            'endDate'
        ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'amount',
            'sender',
            'status',
            'paymentSystem',
            'recipient',
            'date'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]
