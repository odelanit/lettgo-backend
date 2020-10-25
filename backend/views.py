import os

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from advert.models import Category, Area, Advert
from backend.serializers import UserSerializer, CategorySerializer, AreaSerializer, AdvertSerializer, \
    SimpleCategorySerializer, CategoryWriteSerializer


class UserList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if user.id == request.user.id:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class CategoryList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        queryset = Category.objects.filter(parent=None)
        queryset2 = Category.objects.filter(parent=None)
        serializer = CategorySerializer(queryset, many=True)
        serializer2 = SimpleCategorySerializer(queryset2, many=True)
        return Response({
            'categories_table': serializer.data,
            'categories_select': serializer2.data
        })


class CategoryCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategoryWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            queryset = Category.objects.filter(parent=None)
            queryset2 = Category.objects.filter(parent=None)
            serializer = CategorySerializer(queryset, many=True)
            serializer2 = SimpleCategorySerializer(queryset2, many=True)

            return Response({
                'categories_table': serializer.data,
                'categories_select': serializer2.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            queryset = Category.objects.filter(parent=None)
            queryset2 = Category.objects.filter(parent=None)
            serializer = CategorySerializer(queryset, many=True)
            serializer2 = SimpleCategorySerializer(queryset2, many=True)

            return Response({
                'categories_table': serializer.data,
                'categories_select': serializer2.data
            }, status=status.HTTP_200_OK)
        except Category.DoesNotExist as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class AreaList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        queryset = Area.objects.filter(parent=None)
        serializer = AreaSerializer(queryset, many=True)
        return Response(serializer.data)


class AreaCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AreaUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        area = Area.objects.get(pk=pk)
        serializer = AreaSerializer(area)
        return Response(serializer.data)

    def patch(self, request, pk):
        area = Area.objects.get(pk=pk)
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            area = Area.objects.get(pk=pk)
            area.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Area.DoesNotExist as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class AdvertList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        queryset = Advert.objects.filter(parent=None)
        serializer = AdvertSerializer(queryset, many=True)
        return Response(serializer.data)


class AdvertCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdvertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdvertUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        area = Advert.objects.get(pk=pk)
        serializer = AdvertSerializer(area)
        return Response(serializer.data)

    def patch(self, request, pk):
        area = Advert.objects.get(pk=pk)
        serializer = AdvertSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            area = Advert.objects.get(pk=pk)
            area.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Area.DoesNotExist as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_404_NOT_FOUND)


class ImageUploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        file = request.FILES['upload']
        fs = FileSystemStorage()
        filename = get_random_string(length=16) + os.path.splitext(file.name)[1]
        now = timezone.now()
        filepath = '{0}/{1}/{2}'.format(now.year, now.month, filename)
        uploaded_filepath = fs.save(filepath, file)
        uploaded_file_url = fs.url(uploaded_filepath)
        return Response({
            'message': 'Success',
            'url': uploaded_file_url
        })
