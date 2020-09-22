"""Module defined Serializer into data"""

# Libraries
from rest_framework import serializers

# Models
from . import models


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for data Product"""
    class Meta:
        model = models.Product
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for data Client"""
    class Meta:
        model = models.Client
        fields = ['id', 'first_name', 'last_name', 'email', 'identification']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: any):
        """Create Client Data"""
        user = models.Client(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            identification=validated_data['identification']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user.id



class BillSerializer(serializers.ModelSerializer):
    """Serializer for data Bill"""
    # products = ProductSerializer(read_only=True, many=True, allow_null=True)

    class Meta:
        model = models.Bill
        fields = ('id', 'client_id', 'company_name', 'nit', 'code')


class FileSerializer(serializers.ModelSerializer):
    """File Serializer"""
    class Meta():
        """Meta File Serializer"""
        model = models.File
        fields = '__all__'
