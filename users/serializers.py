from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'age']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name must be a non-empty string.")
        return value.strip()

    def validate_age(self, value):
        if not (0 <= value <= 120):
            raise serializers.ValidationError("Age must be between 0 and 120.")
        return value