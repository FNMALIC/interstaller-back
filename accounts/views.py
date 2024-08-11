from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from djoser.social.views import ProviderAuthView
from rest_framework import status
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import UserAccountSerializer
from .models import UserAccount
#  'rest_framework.permissions.IsAuthenticated',
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# from rest_framework.decorators import api_view
from collections import Counter


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.get.data('access')
            refresh_token = response.get.data('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    # serializer_class = UserAccountSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

            response['a'] = "hello guys"
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response['a'] = "hello guys"

        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        print(request.COOKIES)
        if access_token:
            print(request.data["token"])
            request.data["token"] = str(access_token)
            # print(request)
            # response['a'] = "hello guys"

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    # TODO:there is the possibility of a bug
    # def get_queryset(self):
    #     return UserAccount.objects.all()

    def post(self, request, *args, **kwargs):
        print(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response


class SingleUser(APIView):
    permission_classes = [IsAuthenticated,]
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

    def get(self, request):
        print(self.serializer_class.data)

        return HttpResponse(self.serializer_class.data)


@api_view(['GET'])
def user_role_distribution(request):
    user_roles = UserAccount.objects.values_list('role', flat=True)
    role_counts = dict(Counter(user_roles))
    return Response(role_counts)


class UsersWithRoleUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = UserAccount.objects.filter(role='user')
        serializer = UserAccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def employee(request):
    serializer = UserAccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(role=request.data['role'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateEmployeeAccountView(APIView):
    permission_classes = []
    def create(self, request,*args,**kwargs):
        print(0)
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            # print(request.data)
            serializer.save(role='employee')
            print(0)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersWithRoleEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = UserAccount.objects.filter(role='employee')
        serializer = UserAccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = get_object_or_404(UserAccount, pk=pk)
        serializer = UserAccountSerializer(
            user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = get_object_or_404(UserAccount, pk=pk)
        serializer = UserAccountSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = get_object_or_404(UserAccount, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
