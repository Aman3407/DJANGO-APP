from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Supplier
from .forms import ItemForm, SupplierForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.shortcuts import render
from .models import Item
from django.db.models import F, FloatField, ExpressionWrapper

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

def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/item_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'inventory/item_detail.html', {'item': item})

def item_new(request, pk=None):
    if pk:
        item = get_object_or_404(Item, pk=pk)
    else:
        item = None

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            # Save many-to-many relationships
            form.instance.suppliers.set(form.cleaned_data['suppliers'])
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'inventory/item_edit.html', {'form': form})

def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()  # Save the item instance
            # Manually save many-to-many relationships
            form.instance.suppliers.set(form.cleaned_data['suppliers'])
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'inventory/item_edit.html', {'form': form})


def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

# @csrf_exempt
# def item_new_api(request):
#     if request.method == "POST":
#         data = json.loads(request.body.decode('utf-8'))
#         form = ItemForm(data)
#         if form.is_valid():
#             item = form.save()
#             item.suppliers.set(data.get('suppliers', []))  # Set suppliers
#             return JsonResponse({'message': 'Item created successfully', 'item': item.id}, status=201)
#         return JsonResponse({'errors': form.errors}, status=400)
#     return JsonResponse({'message': 'Invalid method'}, status=405)

# @csrf_exempt
# def item_edit_api(request, pk):
#     item = get_object_or_404(Item, pk=pk)
#     if request.method == "PUT":
#         data = json.loads(request.body.decode('utf-8'))
#         form = ItemForm(data, instance=item)
#         if form.is_valid():
#             item = form.save()
#             item.suppliers.set(data.get('suppliers', []))  # Update suppliers
#             return JsonResponse({'message': 'Item updated successfully', 'item': item.id}, status=200)
#         return JsonResponse({'errors': form.errors}, status=400)
#     return JsonResponse({'message': 'Invalid method'}, status=405)


def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

def supplier_new(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'inventory/supplier_edit.html', {'form': form})


from rest_framework import viewsets,status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Item, Supplier
from .serializers import ItemSerializer, SupplierSerializer,UserSerializer
from .permissions import IsAdminUserOrReadOnly
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventory.serializers import PurchaseSerializer

class ItemDetailsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

class SupplierDetailsViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]


@api_view(['POST'])
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
            item.save()

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Purchase successful.'}, status=status.HTTP_200_OK)
