from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from author.models import Profile
from author.serializers import ChangePasswordSerializer, ProfileSerializer, UserCreateSerializer, \
    CustomAuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        try:
            profile = user.profile
            if profile.avatar:
                avatar = profile.avatar.url
            else:
                avatar = None
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'avatar': avatar,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
                'last_login': user.last_login,
            }
            return Response({
                'meta': {
                    'token': token.key
                },
                'data': data
            })
        except Profile.DoesNotExist:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
                'last_login': user.last_login,
            }
            return Response({
                'meta': {
                    'token': token.key
                },
                'data': data
            })


class UserCreationView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
            current_site = get_current_site(request)
            subject = 'Activate Account'
            if request.is_secure():
                protocol = 'https'
            else:
                protocol = 'http'
            email_message = render_to_string('emails/account_activation.html', {
                'user': user,
                'protocol': protocol,
                # 'domain': current_site.domain,
                'domain': 'localhost',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            user.email_user(subject, email_message)
            message = 'We have sent activation email. Please confirm your email for further process.'
            return Response({
                'message': message
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivationView(APIView):
    def get(self, request, uid64, token):
        try:
            a = urlsafe_base64_decode(uid64)
            uid = force_text(a)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user)
            profile.email_verified_at = timezone.now()
            profile.save()
            return Response({
                'message': 'Thank you for confirming your mail.'
            })
        return Response({
            'message': 'Not found'
        }, status=status.HTTP_403_FORBIDDEN)


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, user=request.user)
        if serializer.is_valid():
            request.user.set_password(serializer.data.get('password1'))
            request.user.save()
            return Response(data={
                'message': 'Password updated successfully.'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileChangeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            profile = request.user.profile
            if profile.avatar:
                avatar = profile.avatar.url
            else:
                avatar = None
            return Response({
                'avatar': avatar,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': profile.phone,
                'facebook_id': profile.facebook_id,
                'twitter_id': profile.twitter_id,
                'youtube_id': profile.youtube_id,
                'linkedin_id': profile.linkedin_id,
                'instagram_id': profile.linkedin_id,
                'website': profile.website,
                'description': profile.description,
            })
        except Profile.DoesNotExist:
            return Response({
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            })

    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(data=request.data, user=user)
        if serializer.is_valid():
            avatar = serializer.validated_data.get('avatar')
            email = serializer.validated_data.get('email')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            phone = serializer.validated_data.get('phone')
            facebook_id = serializer.validated_data.get('facebook_id')
            twitter_id = serializer.validated_data.get('twitter_id')
            youtube_id = serializer.validated_data.get('youtube_id')
            linkedin_id = serializer.validated_data.get('linkedin_id')
            instagram_id = serializer.validated_data.get('instagram_id')
            website = serializer.validated_data.get('website')
            description = serializer.validated_data.get('description')

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            try:
                profile = user.profile
                if avatar:
                    profile.avatar = avatar
                profile.phone = phone
                profile.facebook_id = facebook_id
                profile.twitter_id = twitter_id
                profile.youtube_id = youtube_id
                profile.linkedin_id = linkedin_id
                profile.instagram_id = instagram_id
                profile.website = website
                profile.description = description
                profile.save()
            except Profile.DoesNotExist:
                Profile.objects.create(
                    user=user,
                    avatar=avatar,
                    phone=phone,
                    facebook_id=facebook_id,
                    twitter_id=twitter_id,
                    youtube_id=youtube_id,
                    linkedin_id=linkedin_id,
                    instagram_id=instagram_id,
                    website=website,
                    description=description
                )
            return Response(data={
                'message': 'Your profile is now up to date'
            })
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseAccount(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)