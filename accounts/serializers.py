from rest_framework import serializers
from .models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_active',
                  'sex',
                  'interest',
                  'city',
                  'business'
                  ]

    def create(self, validated_data):
        print(validated_data)
        user = UserAccount.objects.create_user(**validated_data)
        return user

# class UserTokenSerializer(serializers.ModelSerializer):
