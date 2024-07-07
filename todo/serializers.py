from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Todo

User = get_user_model()


class TodoSerializer(serializers.ModelSerializer):
    def validate_priority(self, priority):
        if priority < 1:
            raise serializers.ValidationError('Priority must be greater than 0.')
        return priority

    # def validate(self, attrs):
    #     print(f'{attrs = }')
    #     return super().validate(attrs)

    class Meta:
        model = Todo
        fields = '__all__'


# Nested Serializer
class UserSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = '__all__'
