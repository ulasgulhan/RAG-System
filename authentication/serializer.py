from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        """
        Create a new user with the given validated data.

        Parameters:
        validated_data (dict): The validated data for creating a new user.

        Returns:
        User or bool: The created User object if the username is not taken, otherwise False.
        """
        chenck_username = User.objects.filter(username=validated_data["username"])
        if chenck_username:
            return False
        else:
            user = User.objects.create(
                username=validated_data["username"], email=validated_data["email"]
            )
            user.set_password(validated_data["password"])
            user.save()
            return user
