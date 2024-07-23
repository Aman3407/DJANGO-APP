from rest_framework import serializers
from .models import Item, Supplier
from django.contrib.auth.models import User

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    suppliers = serializers.PrimaryKeyRelatedField(many=True, queryset=Supplier.objects.all())

    class Meta:
        model = Item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class PurchaseItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class PurchaseSerializer(serializers.Serializer):
    purchases = serializers.ListSerializer(child=PurchaseItemSerializer())