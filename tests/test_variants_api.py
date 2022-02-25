from io import BytesIO
import json

from app.products.models import Product

from app.images.models import Image
from app.variants.models import Variant
from app.variants.schemas import VariantSchema
from app.main import app, db


class TestVariantAPI:

    def new_variant(self):
        product = Product.query.first()
        variant = Variant(name="test", product_id=product.id)
        db.session.add(variant)
        db.session.commit()
        return variant

    def test_delete_variant(self, client):
        variant = self.new_variant()
        resp = client.delete(f"/variants/{variant.id}")
        assert resp.status_code == 204
        resp = client.delete(f"/variants/{variant.id}")
        assert resp.status_code == 404

    def test_edit_variant(self, client):
        variant = self.new_variant()
        image = Image.query.get(1)
        image2 = Image.query.get(2)
        with app.test_request_context():
            # update variant
            variant_data = {
                "logo_id": image2.id,
                "name": "Variant A",
                "size": "Big",
                "color": "Blue",
                "description": "Variant A description",
                "images": [
                    json.dumps({"id": image.id}),
                    json.dumps({"id": image2.id}),
                    (BytesIO(b"my image raw data"), 'test.png')
                ],
            }
            resp = client.post(f"/variants/{variant.id}", data=variant_data)
            variant = Variant.query.get(variant.id)
            assert resp.status_code == 200
            assert resp.json == VariantSchema().dump(variant)
            assert len(variant.images) == 3

            # update variant by delete 2 images
            resp = client.post(f"/variants/{variant.id}", data={
                "images": [
                    json.dumps({"id": image.id, "delete": "True"}),
                    json.dumps({"id": image2.id, "delete": "True"})
                ]
            })
            variant = Variant.query.get(variant.id)
            assert resp.status_code == 200
            assert resp.json == VariantSchema().dump(variant)
            assert len(variant.images) == 1

            db.session.delete(variant)
            db.session.commit()
