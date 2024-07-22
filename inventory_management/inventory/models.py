from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, unique=True)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    quantityInStock = models.PositiveIntegerField()
    quantitySold = models.PositiveIntegerField()
    revenue = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    suppliers = models.ManyToManyField(Supplier)

    def __str__(self):
        return self.name