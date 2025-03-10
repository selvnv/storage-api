from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class ApiUserRole(models.Model):
    """Provides possibility to use role model for authorization"""

    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class ApiUser(AbstractUser):
    """User model extended with the role model functional"""

    roles = models.ManyToManyField(ApiUserRole, related_name="users", blank=True)


class Storage(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class StorageItem(models.Model):
    storage = models.ForeignKey(Storage, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="storages", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        # Уникальность по нескольким полям
        constraints = [UniqueConstraint(fields=["storage", "item"], name="unique_storage_item")]

    def __str__(self):
        return f"{self.item.name} on storage {self.storage.name}: {self.quantity} pcs"
