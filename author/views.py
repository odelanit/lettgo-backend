from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from author.models import Profile
from author.serializers import ChangePasswordSerializer, ProfileSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'meta': {
                'token': token.key
            },
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
                'last_login': user.last_login,
            }
        })


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
            return Response({
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
            avatar = serializer.data.get('avatar')
            email = serializer.data.get('email')
            first_name = serializer.data.get('first_name')
            last_name = serializer.data.get('last_name')
            phone = serializer.data.get('phone')
            facebook_id = serializer.data.get('facebook_id')
            twitter_id = serializer.data.get('twitter_id')
            youtube_id = serializer.data.get('youtube_id')
            linkedin_id = serializer.data.get('linkedin_id')
            instagram_id = serializer.data.get('instagram_id')
            website = serializer.data.get('website')
            description = serializer.data.get('description')

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            try:
                profile = user.profile
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