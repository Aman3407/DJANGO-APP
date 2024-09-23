from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import ItemDetailsViewSet,SupplierDetailsViewSet, create_user
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'items', ItemDetailsViewSet, basename='item')
router.register(r'suppliers', SupplierDetailsViewSet, basename='supplier')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # Your custom URLs
    path('api/',include(router.urls)),
    path('api/create_user/', create_user, name='create_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]