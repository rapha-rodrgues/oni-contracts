from rest_framework.response import Response
from rest_framework import status
from core.api.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, mixins


class UserCreate(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates the user.
    """
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            token = Token.objects.create(user=serializer.instance)
            json = serializer.data
            json['token'] = token.key
            headers = self.get_success_headers(serializer.data)
            return Response(json, status=status.HTTP_201_CREATED,
                            headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
