from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from api.models import ApiUser, UserRole, Storage, Item, StorageItem
from api.filters import FilteredRoles


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ["id", "name", "description", "is_service"]
        extra_kwargs = {"id": {"read_only": True}}


class ApiUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50, validators=[UniqueValidator(queryset=ApiUser.objects.all())]
    )
    email = serializers.EmailField(validators=[UniqueValidator(queryset=ApiUser.objects.all())])

    roles = FilteredRoles(many=True)

    class Meta:
        model = ApiUser
        fields = ["id", "username", "email", "roles", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        roles = validated_data.pop("roles", [])
        user = ApiUser.objects.create(**validated_data)
        user.set_password(password)
        user.roles.set(roles)
        user.save()
        return user

    def update(self, instance, validated_data):
        if email := validated_data.get("email"):
            instance.email = email

        if password := validated_data.get("password"):
            instance.set_password(password)

        if roles := validated_data.get("roles", []):
            instance.roles.set(roles)

        instance.save()
        return instance


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}


class StorageItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageItem
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

    def update(self, instance, validated_data):
        if quantity := validated_data.get("quantity"):
            instance.quantity = quantity
        instance.save()
        return instance
