from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from users.models import User
from .services import *
from .models import Client
from .permissions import SuperAdminPermission, SystemAdminPermission


class SignUpApi(APIView):
    permission_classes = [AllowAny, ]

    class RequestSerializer(serializers.Serializer):
        email = serializers.CharField(required=True, max_length=255)
        client_name = serializers.CharField(required=True, max_length=255)
        name = serializers.CharField(required=True, max_length=255)
        tel = serializers.CharField(required=True, max_length=255)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'is_active', 'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        client = create_client(data=request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClientDetailApi(APIView):
    permission_classes = [SuperAdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        user_num = serializers.ReadOnlyField()

        class Meta:
            model = Client
            fields = ['id', 'client_name', 'created_at', 'is_active', 'user_num', 'updated_at']

    def get(self, request, client_id):
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClientUpdateApi(APIView):
    permission_classes = [SuperAdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        client_name = serializers.CharField(required=True, max_length=255)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'is_active', 'created_at', 'updated_at']

    def put(self, request, client_id):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        client = update_client(client=client, data=request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClientDeactivateApi(APIView):
    permission_classes = [SuperAdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'is_active', 'created_at', 'updated_at']

    def delete(self, request, client_id):
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        client = deactivate_client(client=client)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClientActivateApi(APIView):
    permission_classes = [SystemAdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Client
            fields = ['id', 'client_name', 'is_active', 'created_at', 'updated_at']

    def put(self, request, client_id):
        client = get_deleted_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        client = activate_client(client=client)
        response_serializer = self.ResponseSerializer(client)
        return Response({
            'client': response_serializer.data
        }, status=status.HTTP_200_OK)


class ClientListUsersApi(APIView):
    permission_classes = [SuperAdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'email', 'name', 'tel', 'role', 'created_at')

    def get(self, request, client_id):
        client = get_client_by(id=client_id)
        self.check_object_permissions(request=request, obj=client)
        users = list(client.users.all())
        response_serializer = self.ResponseSerializer(users, many=True)
        return Response({
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)
