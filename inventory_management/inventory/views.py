from django.shortcuts import render
from django.db.models import F, FloatField, ExpressionWrapper
from .models import Item, Supplier
from rest_framework.decorators import api_view
from rest_framework import viewsets,status, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import SupplierSerializer,UserSerializer, PurchaseSerializer, ItemAdminSerializer, ItemCustomerSerializer
from .permissions import IsAdminUserOrReadOnlyForItems,IsAdminUserOrReadOnlyForSuppliers
from rest_framework.response import Response

import logging

logger = logging.getLogger('inventory')

class ItemDetailsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    permission_classes = [IsAdminUserOrReadOnlyForItems]
    logger = logging.getLogger('myapp')

    def get_serializer_class(self):
        logger.info(f'User {self.request.user} is accessing ItemDetailsViewSet')
        if self.request.user.is_staff or self.request.user.is_superuser:
            return ItemAdminSerializer
        return ItemCustomerSerializer

class SupplierDetailsViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnlyForSuppliers]
    logger = logging.getLogger('myapp')

    def list(self, request, *args, **kwargs):
        logger.info(f'User {request.user} is listing suppliers')
        return super().list(request, *args, **kwargs)



@api_view(['POST'])
def create_user(request):
    logger = logging.getLogger('myapp')
    logger.info('Creating a new user')
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info('User created successfully')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.error(f'Error creating user: {serializer.errors}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer
    logger = logging.getLogger('myapp')

    def put(self, request):
        logger.info(f'User {request.user} is making a purchase')
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
                error_message = f'Item not found: {item_id}'
                logger.error(error_message)
                errors.append({'item_id': item_id, 'error': error_message})
                continue

            if quantity <= 0:
                error_message = 'Quantity must be greater than zero'
                logger.error(f'Item {item_id}: {error_message}')
                errors.append({'item_id': item_id, 'error': error_message})
                continue

            if item.quantityInStock < quantity:
                error_message = 'Not enough stock available'
                logger.error(f'Item {item_id}: {error_message}')
                errors.append({'item_id': item_id, 'error': error_message})
                continue

            # Update item stock and revenue
            item.quantityInStock -= quantity
            item.quantitySold += quantity
            item.revenue += quantity * item.price
            bill += quantity * item.price
            item.save()

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f'Purchase successful, Amount to pay: {bill}')
        return Response({
                        'message': 'Purchase successful.',
                        'AmountToPay': bill
                         }, status=status.HTTP_200_OK)



def stock_report(request):
    logger = logging.getLogger('myapp')
    logger.info('Generating stock report')
    low_stock_items = Item.objects.filter(quantityInStock__lt=5)
    most_sold_item_revenue = Item.objects.annotate(
            total_revenue=ExpressionWrapper(
                F('quantitySold') * F('price'),
                output_field=FloatField()  
            )
        ).order_by('-total_revenue').first()
    most_sold_item_quantity = Item.objects.order_by('-quantitySold').first()

    context = {
        'low_stock_items': low_stock_items,
        'most_sold_item_revenue': most_sold_item_revenue,
        'most_sold_item_quantity': most_sold_item_quantity,
    }
    logger.info('Stock report generated successfully')
    return render(request, 'inventory/stock_report.html', context)
