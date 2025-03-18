from rest_framework.serializers import ModelSerializer, Serializer,SerializerMethodField
from .models import CustomUser ,UserBalance
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import models, transaction


class CustomUserSerializer(ModelSerializer):
    balance = SerializerMethodField()
    class Meta:
        model = CustomUser
        fields =("id", "email","balance")

    def get_balance(self, obj):
        balance_obj = UserBalance.objects.filter(user=obj).first()
        return balance_obj.balance if balance_obj else 0  # Return 0 if no balance is found
    

class RegisterUserSerializer(ModelSerializer): 
    balance = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, default=0.00)  # Allow balance input, default to 0.00

    class Meta:
        model = CustomUser 
        fields = ('email', 'password','balance')
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        try:
            # Begin a transaction block
            with transaction.atomic():
                balance = validated_data.pop('balance', 0.00)
                user = CustomUser.objects.create_user(**validated_data)
                  # Create the user's balance with the provided value or default to 0.00
                UserBalance.objects.create_user_balance(user=user, balance=balance)
                return user
        except Exception as e:
            # If an exception occurs, the transaction will be rolled back automatically
            raise serializers.ValidationError(f"Error during registration: {e}")

class LoginUserSerializer(Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials!")
