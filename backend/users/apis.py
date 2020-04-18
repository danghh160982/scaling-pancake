from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from users.permissions import *
from .services import *
from .models import User


class SignInApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=255)
        password = serializers.CharField(required=True, max_length=255)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'role', 'tel', 'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        auth_token = authenticate_user(**request_serializer.validated_data)
        user = auth_token.user
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data,
            'token': auth_token.key
        }, status=status.HTTP_200_OK)


class UserDetailApi(APIView):
    permission_classes = [UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'role', 'tel', 'created_at', 'updated_at']

    def get(self, request, user_id):
        user = get_user_by(id=user_id)
        self.check_object_permissions(request, obj=user)
        response_serializer = self.ResponseSerializer(user)
        return Response({'user': response_serializer.data})


class UserUpdateApi(APIView):
    permission_classes = [UserPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        tel = serializers.CharField(max_length=255)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'role', 'tel', 'created_at', 'updated_at']

    def put(self, request, user_id):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        user = update_user(data=request_serializer.validated_data, user=user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)


class UserDeactivateApi(APIView):
    permission_classes = [UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'is_active', 'tel', 'created_at', 'updated_at']

    def delete(self, request, user_id):
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        user = deactivate_user(user)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)


class UserChangePasswordApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True, max_length=255)
        password = serializers.CharField(required=True, max_length=255)
        password_confirmation = serializers.CharField(required=True, max_length=255)

    def put(self, request, user_id):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        user = get_user_by(id=user_id)
        self.check_object_permissions(request=request, obj=user)
        change_password(user=user, data=request_serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class UserRequestResetPasswordApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=255)

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        generate_password_token(data=request_serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class UserResetPassword(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        reset_password_token = serializers.CharField(required=True, max_length=255)
        password = serializers.CharField(required=True, max_length=255)
        password_confirmation = serializers.CharField(required=True, max_length=255)

    def put(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        reset_password(data=request_serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class UserCreateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(required=True, max_length=255)
        email = serializers.CharField(required=True, max_length=255)
        tel = serializers.CharField(required=True, max_length=255)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'name', 'email', 'is_active', 'tel', 'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        self.check_permissions(request=request)
        client = request.user.client
        user = create_user(data=request_serializer.validated_data, role=0, client=client)
        response_serializer = self.ResponseSerializer(user)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)
