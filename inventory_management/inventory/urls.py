from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/new/', views.item_new, name='item_new'),
    path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('supplier/new/', views.supplier_new, name='supplier_new'),
    # path('api/item/new/', views.item_new_api, name='item_new_api'),
    # path('api/item/<int:pk>/edit/', views.item_edit_api, name='item_edit_api'),
    path('stock_report/', views.stock_report, name='stock_report'),
    path('api/purchase/', views.PurchaseAPIView.as_view(), name='purchase-api'),
]