from django.urls import path
from .views import InventoryCheckAPIView

urlpatterns = [
    path('inventory-check/', InventoryCheckAPIView.as_view(), name='inventory-check'),
]
