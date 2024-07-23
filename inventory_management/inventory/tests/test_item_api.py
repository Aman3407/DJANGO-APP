import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from inventory.models import Item, Supplier

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username='admin', password='password', is_staff=True)
    return user

@pytest.fixture
def worker_user(db):
    user = User.objects.create_user(username='worker', password='password', is_staff=False)
    return user

@pytest.mark.django_db
def test_create_item_admin(api_client, admin_user):                 #creating item using admin
    api_client.force_authenticate(user=admin_user)
    url = reverse('item-list')
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    data = {
        'name': 'New Item',
        'quantityInStock': 10,
        'quantitySold': 5,
        'revenue': 500.0,
        'price': 50.0,
        'suppliers': [supplier.id],
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db                                          # get list of all items
def test_list_items_worker(api_client, worker_user):
    api_client.force_authenticate(user=worker_user)
    url = reverse('item-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db                                          # create item using worker
def test_create_item_worker(api_client, worker_user):
    api_client.force_authenticate(user=worker_user)
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    url = reverse('item-list')
    data = {
        'name': 'New Item',
        'quantityInStock': 10,
        'quantitySold': 5,
        'revenue': 500.0,
        'price': 50.0,
        'suppliers': [supplier.id],
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db                                          #get particular item 
def test_retrieve_item(api_client, worker_user):
    item = Item.objects.create(name='Test Item', quantityInStock=10, quantitySold=5, revenue=500.0, price=100.0)
    api_client.force_authenticate(user=worker_user)
    url = reverse('item-detail', kwargs={'pk': item.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_item_admin(api_client, admin_user):           #update item
    item = Item.objects.create(name='Test Item', quantityInStock=10, quantitySold=5, revenue=500.0, price=100.0)
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    api_client.force_authenticate(user=admin_user)
    url = reverse('item-detail', kwargs={'pk': item.pk})
    data = {
        'name': 'Updated Item',
        'quantityInStock': 20,
        'quantitySold': 10,
        'revenue': 1000.0,
        'price': 50.0,
        'suppliers': [supplier.id],
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_item_admin(api_client, admin_user):             # delete item
    item = Item.objects.create(name='Test Item', quantityInStock=10, quantitySold=5, revenue=500.0, price=100.0)
    api_client.force_authenticate(user=admin_user)
    url = reverse('item-detail', kwargs={'pk': item.pk})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_worker_update_item(api_client, worker_user):           # update item
    item = Item.objects.create(name='Test Item', quantityInStock=10, quantitySold=5, revenue=500.0, price=100.0)
    api_client.force_authenticate(user=worker_user)
    url = reverse('item-detail', kwargs={'pk': item.pk})
    data = {
        'name': 'Updated Item Name',
        'quantityInStock': 20,
        'quantitySold': 10,
        'revenue': 1000.0,
        'price': 200.0,
        'suppliers': []  # Assuming suppliers are not updated in this case
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db      
def test_worker_delete_item(api_client, worker_user):           #worker trying to delete item
    item = Item.objects.create(name='Test Item', quantityInStock=10, quantitySold=5, revenue=500.0, price=100.0)
    api_client.force_authenticate(user=worker_user)
    url = reverse('item-detail', kwargs={'pk': item.pk})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_item_missing_field(api_client, admin_user):     #missing field
    api_client.force_authenticate(user=admin_user)
    url = reverse('item-list')
    data = {
        'name': 'Test Item',
        'quantityInStock': 10,
        # Missing quantitySold, revenue, and price fields
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_item_invalid_price(api_client, admin_user):     # invalid price 
    api_client.force_authenticate(user=admin_user)
    url = reverse('item-list')
    data = {
        'name': 'Test Item',
        'quantityInStock': 10,
        'quantitySold': 5,
        'revenue': 500,
        'price': 'invalid_price',  # Invalid price
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_update_item_invalid_data(api_client, admin_user):      # invalid date
    item = Item.objects.create(name='Test Item', quantityInStock=10, quantitySold=5, revenue=500, price=100.0)
    api_client.force_authenticate(user=admin_user)
    url = reverse('item-detail', kwargs={'pk': item.pk})
    data = {
        'name': 'Updated Item',
        'quantityInStock': -10,  # Invalid quantity
        'quantitySold': 5,
        'revenue': 500,
        'price': 100.0,
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_item_with_nonexistent_supplier(api_client, admin_user):         #trying to add supplierthat does not exists
    api_client.force_authenticate(user=admin_user)
    url = reverse('item-list')
    non_existent_supplier_id = -1  # using -1 as the non-existent supplier ID
    data = {
        'name': 'Test Item',
        'quantityInStock': 10,
        'quantitySold': 5,
        'revenue': 500,
        'price': 100.0,
        'suppliers': [non_existent_supplier_id]
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'suppliers' in response.data

@pytest.mark.django_db
def test_purchase_multiple_items_success():         #purchase items 
    user = User.objects.create_user(username='testuser', password='password')
    item1 = Item.objects.create(name='Item 1', quantityInStock=10, quantitySold=0, revenue=0.0, price=100.0)
    item2 = Item.objects.create(name='Item 2', quantityInStock=20, quantitySold=0, revenue=0.0, price=150.0)
    
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/purchase/', {
        'purchases': [
            {'item_id': item1.id, 'quantity': 5},
            {'item_id': item2.id, 'quantity': 10}
        ]
    }, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Purchase successful.'
    
    item1.refresh_from_db()
    item2.refresh_from_db()
    
    assert item1.quantityInStock == 5
    assert item1.revenue == 500.0
    assert item2.quantityInStock == 10
    assert item2.revenue == 1500.0

@pytest.mark.django_db
def test_purchase_multiple_items_with_errors():
    user = User.objects.create_user(username='testuser', password='password')
    item1 = Item.objects.create(name='Item 1', quantityInStock=10, quantitySold=0, revenue=0.0, price=100.0)
    
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/purchase/', {
        'purchases': [
            {'item_id': item1.id, 'quantity': 15},  # Not enough stock
            {'item_id': 999, 'quantity': 5},  # Item does not exist
            {'item_id': item1.id, 'quantity': -5}  # Invalid quantity
        ]
    }, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    errors = response.data['errors']
    assert len(errors) == 3
    assert any(error['item_id'] == item1.id and error['error'] == 'Not enough stock available' for error in errors)
    assert any(error['item_id'] == 999 and error['error'] == 'Item not found' for error in errors)
    assert any(error['item_id'] == item1.id and error['error'] == 'Quantity must be greater than zero' for error in errors)

