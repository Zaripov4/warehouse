from django.urls import path

from .views import InventoryCheckAPIView

urlpatterns = [
    path("check/", InventoryCheckAPIView.as_view(), name="inventory-check"),
]
