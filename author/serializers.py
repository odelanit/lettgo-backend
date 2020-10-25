from django.contrib.auth import password_validation
from django.contrib.auth.models import User
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

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ProfileSerializer(serializers.Serializer):
    avatar = serializers.ImageField(allow_null=True, required=False)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    phone = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    facebook_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    twitter_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    youtube_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    linkedin_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    instagram_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    website = serializers.URLField(allow_null=True, allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def validate_email(self, email):
        if email and self.user.email != email:
            try:
                User.objects.get(email=email)
                raise serializers.ValidationError("This email is already taken.")
            except User.DoesNotExist:
                return email
        return email

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
