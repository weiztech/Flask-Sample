from io import BytesIO
import json

from app.products.schemas import ProductSchema
from app.products.models import Product

from app.images.models import Image
from app.variants.models import Variant
from app.variants.schemas import VariantSchema
from app.main import app, db


class TestProductAPI:

    def test_list_products(self, client):
        resp = client.get("/products/")
        assert resp.status_code == 200
        assert len(resp.json) == 2
        products = Product.query.all()
        with app.test_request_context():
            assert resp.json == ProductSchema(many=True).dump(products)

    def test_get_products(self, client):
        resp = client.get("/products/laser-beem")
        assert resp.status_code == 200
        product = Product.query.get("laser-beem")
        with app.test_request_context():
            assert resp.json == ProductSchema().dump(product)

    def test_crud_products(self, client):
        with app.test_request_context():
            image = Image.query.get(1)
            # Create new product with add new file images
            product_data = {
               "logo_id": 1,
               "name": "my product",
               "description": "my description",
               "images": [
                   (BytesIO(b"my image raw data"), 'test.png')],
            }
            resp = client.post("/products/", data=product_data)
            assert resp.status_code == 201
            product = Product.query.get(resp.json["id"])

            for field in ["logo_id", "name", "description"]:
                assert getattr(product, field) == product_data[field]

            assert len(product.images) == 1
            assert resp.json == ProductSchema().dump(product)

            # Update product with
            # - link to exists images ( +2 image)
            # - add new image (+1 image)
            # - remove/delete the first image ( -1 image)
            image2 = Image.query.get(2)
            product_data = {
                "logo_id": image2.id,
                "name": "my new product",
                "description": "my new description",
                "images": [
                    json.dumps({"id": image.id}),
                    json.dumps({"id": image2.id}),
                    json.dumps({"id": product.images[0].id, "delete": "True"}),
                    (BytesIO(b"my image raw data"), 'test.png')
                ],
            }
            resp = client.post(
                f"/products/{product.id}", data=product_data)

            assert resp.status_code == 200
            product = Product.query.get(resp.json["id"])
            for field in ["name", "description"]:
                assert getattr(product, field) == product_data[field]

            assert len(product.images) == 3
            assert resp.json == ProductSchema().dump(product)

            # Delete Product
            resp = client.delete(f"/products/{product.id}")
            assert resp.status_code == 204
            assert Product.query.get(product.id) is None

    def test_product_variants_api(self, client):
        # Add multiple variants under product API
        product = Product(name="master product", id="master-product")
        db.session.add(product)
        db.session.commit()

        image = Image.query.get(1)
        image2 = Image.query.get(2)
        with app.test_request_context():
            variant_a_data = {
                "logo_id": image2.id,
                "name": "Variant A",
                "size": "Big",
                "color": "Blue",
                "description": "Variant A description",
                "images": [
                    json.dumps({"id": image.id}),
                    json.dumps({"id": image2.id}),
                    # (BytesIO(b"my image raw data"), 'test.png')
                ],
            }
            variant_b_data = {
                "logo_id": image.id,
                "name": "Variant B",
                "size": "Small",
                "color": "Green",
                "description": "Variant B description",
                "images": [
                    json.dumps({"id": image.id}),
                 ],
            }
            variants_data = {"variants": [
                json.dumps(variant_a_data),
                json.dumps(variant_b_data)],
                "images_0": [(BytesIO(b"my image raw data"), 'add_to_variant_1.png')],
                "images_1": [(BytesIO(b"my image raw data"), 'add_to_variant_2.png')]
            }
            resp = client.post(
                f"/products/{product.id}/variants", data=variants_data)
            assert resp.status_code == 201

            variant_a = Variant.query.filter_by(name="Variant A").first()
            assert len(variant_a.images) == 3
            for field in ["logo_id", "name", "size", "color", "description"]:
                assert getattr(variant_a, field) == variant_a_data[field]

            variant_b = Variant.query.filter_by(name="Variant B").first()
            assert len(variant_b.images) == 2
            for field in ["logo_id", "name", "size", "color", "description"]:
                assert getattr(variant_b, field) == variant_b_data[field]

            assert resp.json == VariantSchema(many=True).dump([variant_a, variant_b])

            # Product Query Variants API
            resp = client.get(f"/products/{product.id}/variants?page=1")
            assert resp.status_code == 200
            assert resp.json == VariantSchema(many=True).dump([variant_a, variant_b])
