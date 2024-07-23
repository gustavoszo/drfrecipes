from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ..serializers import AuthorSerializer
from ..permissions import MyPermission

from rest_framework import status
from rest_framework.response import Response

class AuthorApiViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        User = get_user_model()
        # Vai trazer apenas o user do usuário logado
        qs = User.objects.filter(username=self.request.user.username)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [MyPermission(), ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # detail = receber PK ou não
    @action(methods=['GET'], detail=False)
    def me(self, request, *args, **kwargs):
        print(*args)
        print(**kwargs)
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance = obj
        )
        return Response(serializer.data)
