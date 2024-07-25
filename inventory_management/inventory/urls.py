from django.urls import path
from . import views

urlpatterns = [
    path('stock_report/', views.stock_report, name='stock_report'),
    path('api/purchase/', views.PurchaseAPIView.as_view(), name='purchase-api'),
]