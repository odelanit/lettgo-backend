from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def validate_old_password(self, old_password):
        if self.user.check_password(old_password):
            return old_password
        else:
            raise serializers.ValidationError("Old password is incorrect.")

    def validate_password1(self, password1):
        password_validation.validate_password(password1)
        return password1

    def validate(self, data):
        if data['password1'] and data['password2'] != data['password1']:
            raise serializers.ValidationError({
                "password2": "password doesn't match"
            })
        return data
