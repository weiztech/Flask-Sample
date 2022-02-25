from app.settings import db
from app.products.models import Product
from werkzeug.datastructures import FileStorage

from .models import Variant


def process_variant_images(variant: Variant, images: list[FileStorage]):
    pass
    # remove_images


def process_instance_variants(product: Product, variants_data: list[dict]):
    remove_variants = []
    for data in variants_data:
        delete = data.pop("delete", None)
        variant_id = data.get("id")
        query_variant = {"id": variant_id, "product_id": product.id}

        if not variant_id:
            new_variant = Variant(**data)
            db.session.add(new_variant)
            product.variants.append(new_variant)
            continue

        if variant_id:
            if delete:
                remove_variants.append(variant_id)
                continue

            variant = Variant.query.filter_by(**query_variant).first()
            if variant:
                variant.set_from_dict(data)

    if remove_variants:
        Variant.query.filter_by(**query_variant).delete()
