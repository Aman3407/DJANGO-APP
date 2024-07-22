from django import forms
from .models import Item, Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact', 'email']

class ItemForm(forms.ModelForm):
    suppliers = forms.ModelMultipleChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # or forms.SelectMultiple if you prefer a dropdown
        required=False
    )
    class Meta:
        model = Item
        fields = ['name', 'quantityInStock', 'quantitySold', 'revenue', 'price', 'suppliers']