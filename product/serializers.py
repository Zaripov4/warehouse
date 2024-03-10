from rest_framework import serializers

from .models import Material, Product, ProductMaterial, Warehouse


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class ProductMaterialSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = ProductMaterial
        fields = ["product", "material", "quantity"]


class WarehouseSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = Warehouse
        fields = ["id", "material", "remainder", "price"]


class ProductSerializer(serializers.ModelSerializer):
    materials = ProductMaterialSerializer(source="productmaterial_set", many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "code", "materials"]
