from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import ItemDetailsViewSet,SupplierDetailsViewSet, create_user

router = DefaultRouter()
router.register(r'items',ItemDetailsViewSet)
router.register(r'suppliers',SupplierDetailsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # Your custom URLs
    path('api/',include(router.urls)),
    path('api/create_user/', create_user, name='create_user'),
]