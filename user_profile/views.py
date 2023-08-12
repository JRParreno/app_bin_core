from django.shortcuts import render
from rest_framework import generics, permissions, response, status
from oauth2_provider.models import (
    Application,
    RefreshToken,
    AccessToken
)
from datetime import (
    datetime,
    timedelta
)
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.conf import settings

from user_profile.models import UserProfile, UserPairDevice
from user_profile.serializers import RegisterSerializer, ProfileSerializer, AddDeviceUserSerializer, MyDeviceUserSerializer
from api.serializers import UserSerializer
from api.paginate import ExtraSmallResultsSetPagination
from .serializers import UploadPhotoSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create_access_token(self, user):
        application = Application.objects.all()

        if application.exists():
            self.expire_seconds = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
            scopes = settings.OAUTH2_PROVIDER['SCOPES']
            expires = datetime.now() + timedelta(seconds=self.expire_seconds)
            token = get_random_string(32)
            refresh_token = get_random_string(32)

            access_token = AccessToken.objects.create(
                user=user,
                expires=expires,
                scope=scopes,
                token=token,
                application=application.first(),
            )

            refresh_token = RefreshToken.objects.create(
                user=user,
                access_token=access_token,
                token=refresh_token,
                application=application.first(),
            )

            return access_token, refresh_token

        return None

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        email = request.data.get('email')

        if User.objects.filter(email=email).exists():
            data = {
                "error_message": "Email already exists"
            }
            return response.Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != confirm_password:
            data = {
                "error_message": "Password does not match"
            }
            return response.Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=email, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user)

        oauth_token, refresh_token = self.create_access_token(
            user)

        data = {
            "access_token": oauth_token.token,
            "expires": self.expire_seconds,
            "token_type": "Bearer",
            "scope": oauth_token.scope,
            "refresh_token": refresh_token.token
        }

        return response.Response(
            data=data,
            status=status.HTTP_200_OK
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_profiles = UserProfile.objects.filter(user=user)

        if user_profiles.exists():
            user_profile = user_profiles.first()
            data = {
                "pk": str(user.pk),
                "username": user.username,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "profilePhoto": request.build_absolute_uri(user_profile.profile_photo.url) if user_profile.profile_photo else None,
                "profilePk": str(user_profile.pk),
            }

            return response.Response(data, status=status.HTTP_200_OK)

        else:
            error = {
                "error_message": "Please setup your profile"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        user_details = self.request.data.get('user')
        user_email = UserProfile.objects.filter(
            user__email=user_details['email']).exclude(user=user).exists()

        if user_email:
            error = {
                "error_message": "Email already exists"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfile.objects.get(user=user)

        user.email = user_details['email']
        user.first_name = user_details['first_name']
        user.last_name = user_details['last_name']
        user.username = user_details['email']
        user.save()

        user_profile.save()

        data = {
            "pk": str(user.pk),
            "username": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "profilePhoto": request.build_absolute_uri(user_profile.profile_photo.url) if user_profile.profile_photo else None,
            "profilePk": str(user_profile.pk),
        }

        return response.Response(data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request
        })
        return context


class UploadPhotoView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadPhotoSerializer
    queryset = UserProfile.objects.all()


class AddDeviceUser(generics.CreateAPIView):
    serializer_class = AddDeviceUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserPairDevice.objects.all()


class MyDeviceUser(generics.ListAPIView):
    serializer_class = MyDeviceUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserPairDevice.objects.all()
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return UserPairDevice.objects.filter(user_request__user=user)


class AcceptDeviceUser(generics.UpdateAPIView):
    serializer_class = AddDeviceUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserPairDevice.objects.all()
