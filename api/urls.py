from rest_framework.routers import DefaultRouter

from api.views import (
    UserRoleViewSet,
    ApiUserViewSet,
    StorageViewSet,
    ItemViewSet,
    StorageItemViewSet,
)

router = DefaultRouter()
router.register("user_role", UserRoleViewSet)
router.register("user", ApiUserViewSet)
router.register("storage", StorageViewSet)
router.register("item", ItemViewSet)
router.register("inventory", StorageItemViewSet)

urlpatterns = []

urlpatterns.extend(router.urls)
