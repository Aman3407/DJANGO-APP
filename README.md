# Inventory Management System

## Overview

The **Inventory Management System** is a Django-based web application designed to manage inventory items and suppliers. The application includes features for creating, reading, updating, and deleting both items and suppliers, as well as providing a reporting feature to track stock and sales. It also allows user to purchase multiple items at once and also reflects the changes on the database by decreasing the amount of stock left and increasing the revenue genrerated. The application uses Django REST Framework to provide a set of RESTful API endpoints for interacting with the inventory data.

## Project Setup

### Prerequisites

- Python
- Django 
- Django REST Framework 
- MySQL 
- pytest 

### Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/inventory-management-system.git
   cd inventory-management-system
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Required Packages:**
   Create a `requirements.txt` file with the following content:
   ```txt
   Django==5.0.7
   djangorestframework==3.15.0
   mysqlclient==2.1.1
   pytest==8.3.1
   pytest-django==4.8.0
   ```

   Then, install the packages using:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the Database:**
   Ensure that MySQL is running and create a database named `inventory_db`.

   Update the `DATABASES` setting in `inventory_management/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'inventory_db',
           'USER': 'inventory_user',
           'PASSWORD': 'Aman@123',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

6. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

### API Endpoints

#### Item Endpoints

- **List Items**
  - **GET** `/api/items/`
  - **Description:** Retrieve a list of all items.
   <img width="1010" alt="image" src="https://github.com/user-attachments/assets/3ef248f8-8235-4ff9-bf89-e97c98c603ad">

- **Create Item**
  - **POST** `/api/items/`
  - **Description:** Create a new item.
    
    Admin Creating item
     <img width="1019" alt="image" src="https://github.com/user-attachments/assets/3f335dcc-55eb-4cb9-8454-f6a92ce8b9ad">
    User Creating Item
    <img width="1017" alt="image" src="https://github.com/user-attachments/assets/22970965-47b0-4041-b49c-1d351f34adab">
    Trying to create same item twice
    <img width="1040" alt="image" src="https://github.com/user-attachments/assets/7224233f-4adb-4e4b-86d7-b2fd484f42b4">

- **Retrieve Item**
  - **GET** `/api/items/{id}/`
  - **Description:** Retrieve details of a specific item.
    <img width="1011" alt="image" src="https://github.com/user-attachments/assets/e3286dca-39f7-4d59-95e2-7fa4d6339eb7">

  if item does not exits
  <img width="1008" alt="image" src="https://github.com/user-attachments/assets/848743fb-3811-4703-a3fb-e647f0e96571">

- **Update Item**
  - **PUT** `/api/items/{id}/`
  - **Description:** Update details of a specific item.
    Admin updating item
    <img width="997" alt="image" src="https://github.com/user-attachments/assets/bec26a5b-3331-463c-b673-32ec6fc65785">
    User trying to update item
    <img width="1019" alt="image" src="https://github.com/user-attachments/assets/d5afcc4e-43f0-4b4c-8158-743b9093ab56">


- **Delete Item**
  - **DELETE** `/api/items/{id}/`
  - **Description:** Delete a specific item.
    Admin deleting item
    <img width="1019" alt="image" src="https://github.com/user-attachments/assets/a33dd443-ec75-4f89-8c5a-18b0f880dfbb">
    <img width="1004" alt="image" src="https://github.com/user-attachments/assets/04be944f-51f8-4ab9-9b67-c3a580a56c6a">
    <img width="1027" alt="image" src="https://github.com/user-attachments/assets/baaeb574-3be4-4ecd-8aa9-073d164f6d62">

    User trying to delete item
    <img width="1011" alt="image" src="https://github.com/user-attachments/assets/0a39256d-d689-4078-9936-c95cc7fe83b6">


#### Supplier Endpoints

- **List Suppliers**
  - **GET** `/api/suppliers/`
  - **Description:** Retrieve a list of all suppliers.
    <img width="1009" alt="image" src="https://github.com/user-attachments/assets/58a79b80-9c57-426b-b26d-72c4cb5d0a69">

- **Create Supplier**
  - **POST** `/api/suppliers/`
  - **Description:** Create a new supplier.
    Admin Creating Supplier
    <img width="1005" alt="image" src="https://github.com/user-attachments/assets/4ed12bb9-425e-44e7-a772-733de7ea40ce">

    if admin try to create supplier with same contact or email
    <img width="1012" alt="image" src="https://github.com/user-attachments/assets/a5c28202-5b38-4902-bfe7-b3140b804cd1">

    User Creating Supplier
    <img width="1003" alt="image" src="https://github.com/user-attachments/assets/3cc8bdf2-88b2-4fe3-bebe-3fadee4b476e">

- **Retrieve Supplier**
  - **GET** `/api/suppliers/{id}/`
  - **Description:** Retrieve details of a specific supplier.
    <img width="1004" alt="image" src="https://github.com/user-attachments/assets/d15e3460-414d-4b28-b1b9-c4e0dddbb0da">


- **Update Supplier**
  - **PUT** `/api/suppliers/{id}/`
  - **Description:** Update details of a specific supplier.
    <img width="1015" alt="image" src="https://github.com/user-attachments/assets/6b35deb5-a0eb-4ea8-82f7-658153c6ce43">

- **Delete Supplier**
  - **DELETE** `/api/suppliers/{id}/`
  - **Description:** Delete a specific supplier.
 
    Admin deleting supplier
    <img width="1003" alt="image" src="https://github.com/user-attachments/assets/bfc2092a-d4e4-4b0e-8765-431f5fd47b77">
    <img width="1012" alt="image" src="https://github.com/user-attachments/assets/9423e0be-9ca2-47a9-89aa-2885de99297e">
    <img width="1011" alt="image" src="https://github.com/user-attachments/assets/b4f52d1d-614f-490e-8a52-b3f427800063">

    Trying to delete user that does not exists
    <img width="999" alt="image" src="https://github.com/user-attachments/assets/8ed378bb-0098-45b5-b9f2-5d3f34db065c">


### Testing

To run tests and check coverage:

1. **Install Testing Dependencies:**
   ```bash
   pip install pytest pytest-django
   ```

2. **Run Tests:**
   ```bash
   pytest
   ```

3. **Check Test Coverage:**
   ```bash
   pytest --cov
   ```

## Project Structure

- `inventory/`: Contains the Django app for inventory management.
  - `models.py`: Defines the `Item` and `Supplier` models.
  - `views.py`: Contains API views for items and suppliers.
  - `serializers.py`: Serializers for the models.
  - `urls.py`: URL routing for the app.
- `inventory_management/`: Project settings and configuration.
  - `settings.py`: Configuration settings.
  - `urls.py`: Project-wide URL routing.

## Notes

- Ensure that MySQL server is running and accessible with the credentials provided.
- Adjust database configurations in `settings.py` as necessary.

For any issues or further questions, please refer to the [Django documentation](https://docs.djangoproject.com/en/stable/) or the [Django REST Framework documentation](https://www.django-rest-framework.org/).
```

You can copy and paste this markdown into a `README.md` file in your project repository. It includes an overview of the project, setup instructions, details about the API endpoints, and testing guidelines.