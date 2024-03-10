from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ProductMaterial, Warehouse


class InventoryCheckAPIView(APIView):
    def post(self, request, *args, **kwargs):
        requested_products = request.data
        response_data = self.check_inventory(requested_products)
        return Response(response_data)

    def check_inventory(self, requested_products):
        result = []
        error = None

        for product_name, quantity in requested_products.items():
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                error = {"error": f"Product '{product_name}' not found"}
                break

            product_materials = ProductMaterial.objects.filter(product=product)
            product_material_data = []

            for product_material in product_materials:
                warehouse = Warehouse.objects.filter(
                    material=product_material.material
                ).first()

                if warehouse:
                    if warehouse.remainder >= quantity * product_material.quantity:
                        product_material_data.append(
                            {
                                "warehouse_id": warehouse.id,
                                "material_name": product_material.material.name,
                                "qty": quantity * product_material.quantity,
                                "price": warehouse.price,
                            }
                        )
                    else:
                        product_material_data.append(
                            {
                                "warehouse_id": None,
                                "material_name": product_material.material.name,
                                "qty": warehouse.remainder,
                                "price": warehouse.price,
                            }
                        )
                else:
                    product_material_data.append(
                        {
                            "warehouse_id": None,
                            "material_name": product_material.material.name,
                            "qty": 0,
                            "price": None,
                        }
                    )

            result.append(
                {
                    "product_name": product.name,
                    "product_qty": quantity,
                    "product_materials": product_material_data,
                }
            )

        if error:
            return error
        else:
            return {"result": result}
