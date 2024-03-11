from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ProductMaterial, Warehouse


class InventoryCheckAPIView(APIView):
    def post(self, request, *args, **kwargs):
        warehouse_inventory = [
            {"id": 1, "material_name": "Mato", "quantity": 12, "price": 1500},
            {"id": 2, "material_name": "Mato", "quantity": 200, "price": 1600},
            {"id": 3, "material_name": "Ip", "quantity": 40, "price": 500},
            {"id": 4, "material_name": "Ip", "quantity": 300, "price": 550},
            {"id": 5, "material_name": "Tugma", "quantity": 500, "price": 300},
            {"id": 6, "material_name": "Zamok", "quantity": 1000, "price": 2000},
        ]
        requested_products = request.data
        response_data = self.check_inventory(requested_products, warehouse_inventory)
        if "error" in response_data:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data)

    def check_inventory(self, requested_products, warehouse_inventory):
        result = []

        for product_name, quantity in requested_products.items():
            # Retrieve warehouse inventory for the product
            product_inventory = [
                item
                for item in warehouse_inventory
                if item["material_name"] == product_name
            ]

            # Check if enough quantity is available in the warehouse
            total_quantity_available = sum(
                item["quantity"] for item in product_inventory
            )
            if int(total_quantity_available) < int(quantity):
                return {"error": f"Insufficient inventory for product {product_name}"}

            product_inventory.sort(key=lambda x: x["id"])  # Sorting by "id"
            used_inventory = []

            for item in product_inventory:
                qty_to_use = min(quantity, item["quantity"])
                used_inventory.append(
                    {
                        "warehouse_id": item["id"],
                        "material_name": product_name,
                        "qty": qty_to_use,
                        "price": item["price"],
                    }
                )
                quantity -= qty_to_use

                if quantity == 0:
                    break

            result.append(
                {
                    "product_name": product_name,
                    "product_qty": quantity,
                    "product_materials": used_inventory,
                }
            )

        return {"result": result}
