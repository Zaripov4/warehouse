# models.py
from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
