from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from rest_framework import serializers

from advert.models import Category, Area, Advert


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username', 'email',
            'first_name', 'last_name', 'password',
            'is_active', 'is_staff', 'is_superuser',
            'last_login'
        ]
        read_only_fields = ['is_superuser', 'last_login', 'id']

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=validated_data['is_active'],
            is_staff=validated_data['is_staff']
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for(key, value) in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance

    def validate_password(self, password):
        if not self.instance:
            password_validation.validate_password(password)
        if self.instance and password:
            password_validation.validate_password(password)
        return password


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'parent',
            'name',
            'image_url',
            'marker_url',
            'icon_url',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'parent',
            'name',
            'image_url',
            'marker_url',
            'icon_url',
            '_showChildren',
            '_children',
        ]

        read_only_fields = ['id', '_children', '_showChildren']

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['_children'] = CategorySerializer(many=True)
        return fields


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'label',
            'children',
        ]

        read_only_fields = ['id', 'children']

    def get_fields(self):
        fields = super(SimpleCategorySerializer, self).get_fields()
        fields['children'] = SimpleCategorySerializer(many=True)
        return fields


class ChildAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            'id',
            'parent',
            'name',
            'address',
            'latitude',
            'longitude',
            'children'
        ]

        read_only_fields = ['id', 'children']


class AreaSerializer(serializers.ModelSerializer):
    children = ChildAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = [
            'id',
            'parent',
            'name',
            'address',
            'latitude',
            'longitude',
            'children'
        ]

        read_only_fields = ['id', 'children']


class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = [
            'id',
            'title',
            'description',
            'latitude',
            'longitude',
            'price',
            'sale_price',
            'category',
            'user',
        ]

        read_only_fields = ['id']
