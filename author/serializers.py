from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


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


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError("Username is already registered.")
        except User.DoesNotExist:
            return username

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError("Email is already registered.")
        except User.DoesNotExist:
            return email

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
        username = validated_data['username']
        email = validated_data['email']
        password1 = validated_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password1)
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
