from django.shortcuts import render
from django.db.models import F, FloatField, ExpressionWrapper
from .models import Item, Supplier
from rest_framework.decorators import api_view
from rest_framework import viewsets,status, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import SupplierSerializer,UserSerializer, PurchaseSerializer, ItemAdminSerializer, ItemCustomerSerializer
from .permissions import IsAdminUserOrReadOnlyForItems,IsAdminUserOrReadOnlyForSuppliers
from rest_framework.response import Response
from .permissions import IsAdminUserOrReadOnlyForItems

class ItemDetailsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    permission_classes = [IsAdminUserOrReadOnlyForItems]

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return ItemAdminSerializer
        return ItemCustomerSerializer

class SupplierDetailsViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnlyForSuppliers]


@api_view(['PUT'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purchases = serializer.validated_data['purchases']
        bill = 0
        errors = []
        for purchase in purchases:
            item_id = purchase['item_id']
            quantity = purchase['quantity']

            try:
                item = Item.objects.get(pk=item_id)
            except Item.DoesNotExist:
                errors.append({'item_id': item_id, 'error': 'Item not found'})
                continue

            if quantity <= 0:
                errors.append({'item_id': item_id, 'error': 'Quantity must be greater than zero'})
                continue

            if item.quantityInStock < quantity:
                errors.append({'item_id': item_id, 'error': 'Not enough stock available'})
                continue

            # Update item stock and revenue
            item.quantityInStock -= quantity
            item.quantitySold += quantity
            item.revenue += quantity * item.price
            bill +=  quantity*item.price
            item.save()

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
                        'message': 'Purchase successful.',
                        'AmountToPay' : bill
                         }, status=status.HTTP_200_OK)


def stock_report(request):
    low_stock_items = Item.objects.filter(quantityInStock__lt=5)
    most_sold_item_revenue = Item.objects.annotate(
            total_revenue=ExpressionWrapper(
                F('quantitySold') * F('price'),
                output_field=FloatField()  
            )
        ).order_by('-total_revenue').first()
        # Most sold item by quantity
    most_sold_item_quantity = Item.objects.order_by('-quantitySold').first()

    context = {
        'low_stock_items': low_stock_items,
        'most_sold_item_revenue': most_sold_item_revenue,
        'most_sold_item_quantity': most_sold_item_quantity,
    }
    
    return render(request, 'inventory/stock_report.html', context)