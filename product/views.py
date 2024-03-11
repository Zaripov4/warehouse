from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class InventoryCheckAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Warehouse inventory with more accurate quantities
        warehouse_inventory = [
            {
                "id": 1,
                "material_name": "Mato",
                "quantity": 20,
                "price": 1500,
            },  # Decreased quantity
            {"id": 2, "material_name": "Mato", "quantity": 150, "price": 1600},
            {"id": 3, "material_name": "Ip", "quantity": 40, "price": 500},
            {"id": 4, "material_name": "Ip", "quantity": 260, "price": 550},
            {"id": 5, "material_name": "Tugma", "quantity": 150, "price": 300},
            {"id": 6, "material_name": "Zamok", "quantity": 1000, "price": 2000},
        ]
        requested_products = (
            request.data
        )  # Assuming request contains product names and quantities
        response_data = self.check_inventory(requested_products, warehouse_inventory)
        if "error" in response_data:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data)

    def check_inventory(self, requested_products, warehouse_inventory):
        result = []

        product_materials_required = {
            "ko'ylak": {"mato": 0.8, "tugma": 5, "ip": 10},
            "shim": {"mato": 1.4, "ip": 15, "zamok": 1},
        }

        for product_name, quantity in requested_products.items():
            product_materials_data = []

            # Fetch inventory data for the requested product from warehouse_inventory
            product_inventory = [
                item
                for item in warehouse_inventory
                if item["material_name"] == product_name
            ]

            if not product_inventory:
                return {"error": f"Product '{product_name}' not found"}

            # Calculate the total quantities of materials required for the specified quantity of the product
            total_materials_required = {}
            for material, qty_per_product in product_materials_required[
                product_name
            ].items():
                total_materials_required[material] = qty_per_product * quantity

            # Check if enough quantity is available in the warehouse for each material
            for material, required_qty in total_materials_required.items():
                # Fetch inventory data for the material from warehouse_inventory
                material_inventory = [
                    item
                    for item in warehouse_inventory
                    if item["material_name"] == material
                ]

                if not material_inventory:
                    return {
                        "error": f"Material '{material}' not found for product '{product_name}'"
                    }

                total_qty_available = sum(
                    item["quantity"] for item in material_inventory
                )

                if total_qty_available < required_qty:
                    return {
                        "error": f"Insufficient inventory for material '{material}' to produce '{product_name}'"
                    }

                # Find the price of the material
                material_price = material_inventory[0][
                    "price"
                ]  # Assuming price is the same for all instances of the material

                product_materials_data.append(
                    {
                        "material_name": material,
                        "qty_required": required_qty,
                        "qty_available": total_qty_available,
                        "price": material_price,
                    }
                )

            # Add product data to the response
            result.append(
                {
                    "product_name": product_name,
                    "product_qty": quantity,
                    "product_materials": product_materials_data,
                }
            )

        return {"result": result}
