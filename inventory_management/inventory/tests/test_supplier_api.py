import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
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
def test_create_supplier_admin(api_client, admin_user):       # create supplier with admin
    api_client.force_authenticate(user=admin_user)
    url = reverse('supplier-list')
    data = {
        'name': 'New Supplier',
        'contact': '1234567890',
        'email': 'new_supplier@example.com',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db                                        # get all supplier
def test_list_suppliers_worker(api_client, worker_user):
    api_client.force_authenticate(user=worker_user)
    url = reverse('supplier-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db                                      
def test_create_supplier_worker(api_client, worker_user):       # create supplier with worker
    api_client.force_authenticate(user=worker_user)
    url = reverse('supplier-list')
    data = {
        'name': 'New Supplier',
        'contact': '1234567890',
        'email': 'new_supplier@example.com',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_retrieve_supplier(api_client, worker_user):            # get supplier with worker
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    api_client.force_authenticate(user=worker_user)
    url = reverse('supplier-detail', kwargs={'pk': supplier.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_supplier_admin(api_client, admin_user):         # get supplier with admin
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    api_client.force_authenticate(user=admin_user)
    url = reverse('supplier-detail', kwargs={'pk': supplier.pk})
    data = {
        'name': 'Updated Supplier',
        'contact': '0987654321',
        'email': 'updated_supplier@example.com',
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_supplier_admin(api_client, admin_user):         # delete supplier admin
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    item = Item.objects.create(item_id = 1, name='Test Item', quantityInStock=10, quantitySold=5, revenue=500.0, price=100.0)
    item.suppliers.add(supplier)
    item.save()

    api_client.force_authenticate(user=admin_user)
    url = reverse('supplier-detail', kwargs={'pk': supplier.pk})
    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    item.refresh_from_db()
    assert supplier not in item.suppliers.all()

@pytest.mark.django_db
def test_create_supplier_missing_field(api_client, admin_user):         # missing field supplier
    api_client.force_authenticate(user=admin_user)
    url = reverse('supplier-list')
    data = {
        'name': 'New Supplier',
        # contact and email fields are missing
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_supplier_invalid_email(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('supplier-list')
    data = {
        'name': 'New Supplier',
        'contact': '1234567890',
        'email': 'invalid_email',  # Invalid email
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_update_supplier_invalid_contact(api_client, admin_user):
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    api_client.force_authenticate(user=admin_user)
    url = reverse('supplier-detail', kwargs={'pk': supplier.pk})
    data = {
        'name': 'Updated Supplier',
        'contact': '',  # Invalid contact
        'email': 'updated_supplier@example.com',
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_delete_supplier_non_existent(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('supplier-detail', kwargs={'pk': 9999})  # Non-existent supplier ID
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_worker_update_supplier(api_client, worker_user):
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    api_client.force_authenticate(user=worker_user)
    url = reverse('supplier-detail', kwargs={'pk': supplier.pk})
    data = {
        'name': 'Updated Supplier Name',
        'contact': '0987654321',
        'email': 'updated@example.com'
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_worker_delete_supplier(api_client, worker_user):
    supplier = Supplier.objects.create(name='Test Supplier', contact='1234567890', email='test@example.com')
    api_client.force_authenticate(user=worker_user)
    url = reverse('supplier-detail', kwargs={'pk': supplier.pk})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_item_supplier_relationship():
    supplier1 = Supplier.objects.create(name='Supplier One', contact='1234567890', email='one@example.com')
    supplier2 = Supplier.objects.create(name='Supplier Two', contact='0987654321', email='two@example.com')
    item = Item.objects.create(
        item_id = 1, 
        name='Test Item',
        quantityInStock=10,
        quantitySold=5,
        revenue=500.0,
        price=100.0
    )
    item.suppliers.add(supplier1, supplier2)
    
    assert item.suppliers.count() == 2
    assert item.suppliers.filter(name='Supplier One').exists()
    assert item.suppliers.filter(name='Supplier Two').exists()