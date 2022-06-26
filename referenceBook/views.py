from django.contrib.auth.models import User
from django.http import Http404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, inline_serializer, OpenApiExample
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render, redirect

from referenceBook.models import TelephoneNumber
from referenceBook.permissions import UserViewPermission, IsOwnerOrAdmin
from referenceBook.serializers import UserSerializer, TelephoneNumberSerializer


def index(request):
    if request.method == "POST":
        room_code = request.POST.get("room_code")
        char_choice = request.POST.get("character_choice")
        return redirect(
            '/play/%s?&choice=%s'
            %(room_code, char_choice)
        )
    return render(request, "index.html", {})

@extend_schema_view(
    list=extend_schema(
        summary="Get list of users",
        description="Only stuff can see all users",
        tags=["User"]
    ),
    retrieve=extend_schema(
        summary="Get user",
        tags=["User"]
    ),
    destroy=extend_schema(
        summary="Delete user",
        tags=["User"]
    ),
    create=extend_schema(
        summary="Register user",
        tags=["User"]
    ),
    exists=extend_schema(
        summary="Check user existence",
        methods=["HEAD"],
        tags=["User"]
    )
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewPermission]
    lookup_field = "username"

    def exists(self, request, *args, **kwargs):
        try:
            _ret = self.retrieve(request, *args, **kwargs)
            return Response(status=status.HTTP_200_OK)
        except Http404 as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    list=extend_schema(
        summary="Get list of telephone numbers",
        tags=["TelephoneNumber"]
    ),
    retrieve=extend_schema(
        summary="Get telephone number",
        tags=["TelephoneNumber"]
    ),
    destroy=extend_schema(
        summary="Delete telephone number",
        tags=["TelephoneNumber"]
    ),
    create=extend_schema(
        summary="Create telephone number",
        tags=["TelephoneNumber"]
    ),
    update=extend_schema(
        exclude=True
    ),
    partial_update=extend_schema(
        exclude=True
    )
)
class TelephoneNumberViewSet(viewsets.ModelViewSet):
    queryset = TelephoneNumber.objects.all()
    serializer_class = TelephoneNumberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]


telephoneNumberSerializer = inline_serializer(
                       name="telephoneNumber",
                       fields={
                           'message': serializers.CharField()
                       })