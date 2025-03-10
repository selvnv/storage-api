from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import UserRole, ApiUser, Storage, Item, StorageItem
from api.permissions import ProviderPermission
from api.serializers import UserRoleSerializer, ApiUserSerializer, StorageSerializer, ItemSerializer, \
    StorageItemSerializer


# Create your views here.

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

class ApiUserViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    serializer_class = ApiUserSerializer

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [ProviderPermission]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class StorageItemViewSet(viewsets.ModelViewSet):
    queryset = StorageItem.objects.all()
    serializer_class = StorageItemSerializer
