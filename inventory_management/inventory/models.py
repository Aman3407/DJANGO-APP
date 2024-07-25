from django.db import models
from django.core.validators import RegexValidator

class Supplier(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    contact = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact must be exactly 10 digits.'
            )
        ],
        blank=False,
        null=False
    )
    email = models.EmailField(blank=False, null=False, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    item_id = models.IntegerField(unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    quantityInStock = models.PositiveIntegerField(default=0)
    quantitySold = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    suppliers = models.ManyToManyField(Supplier)

    def __str__(self):
        return self.name