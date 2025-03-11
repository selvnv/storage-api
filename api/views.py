from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from api.models import UserRole, ApiUser, Storage, Item, StorageItem
from api.permissions import (
    ProviderOrReadOnlyPermission,
    AdminOrReadOnlyPermission,
    OwnerOrReadOnly,
    ConsumerOrReadOnlyPermission,
)
from api.serializers import (
    UserRoleSerializer,
    ApiUserSerializer,
    StorageSerializer,
    ItemSerializer,
    StorageItemSerializer,
)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [AdminOrReadOnlyPermission]


class ApiUserViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    serializer_class = ApiUserSerializer
    permission_classes = [OwnerOrReadOnly]


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [ProviderOrReadOnlyPermission]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [ProviderOrReadOnlyPermission]


class StorageItemViewSet(viewsets.ModelViewSet):
    queryset = StorageItem.objects.all()
    serializer_class = StorageItemSerializer

    def get_permissions(self):
        if self.action == "fetch_item":
            # Только для потребителей
            permission_classes = [ConsumerOrReadOnlyPermission]
        else:
            # Все остальные запросы только для поставщиков
            permission_classes = [ProviderOrReadOnlyPermission]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["post"])
    def fetch_item(self, request, pk=None):
        item = self.get_object()
        quantity = request.data.get("quantity")

        if quantity is None:
            return Response(data={"error": "No quantity specified"}, status=HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response(
                data={"error": "Quantity must be an integer"}, status=HTTP_400_BAD_REQUEST
            )

        if quantity <= 0:
            return Response(
                data={"error": "Quantity must be greater than zero"}, status=HTTP_400_BAD_REQUEST
            )

        if quantity > item.quantity:
            return Response(
                data={"error": f"Max quantity available is {item.quantity}"},
                status=HTTP_400_BAD_REQUEST,
            )

        item.quantity -= quantity
        item.save()
        return Response(StorageItemSerializer(item).data, HTTP_200_OK)
