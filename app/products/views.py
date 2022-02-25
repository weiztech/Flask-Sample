from datetime import datetime
from werkzeug.datastructures import FileStorage

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_smorest.pagination import PaginationParameters

from app.settings import db
from app.common.classes import QueryUtils
from app.images.schemas import ImageListCrudSchema
from app.images.functions import process_instance_images
from app.variants.schemas import VariantSchema, VariantsAddSchema, VariantQuerySchema
from app.variants.models import Variant, VariantImages

from .schemas import ProductQuerySchema, ProductSchema, ProductCRUDSchema
from .models import Product, ProductImages


product_blp = Blueprint("products", "products", url_prefix="/products", description="Products API List")
product_blp.DEFAULT_PAGINATION_PARAMETERS = {"page": 1, "page_size": 15, "max_page_size": 30}


@product_blp.route("/")
class Products(QueryUtils, MethodView):

    CUSTOM_QUERY = {
        "name": Product.name.contains,
        "description": Product.description
    }

    @product_blp.arguments(ProductQuerySchema, location="query")
    @product_blp.paginate()
    @product_blp.response(200, ProductSchema(many=True), example=[{
        "description": "this is product description",
        "logo_id": 1,
        "id": "sample-product",
        "created_at": "2022-02-16T08:51:39.460Z",
        "updated_at": "2022-02-16T08:51:39.460Z",
        "name": "Sample Product"
    }])
    def get(self, query: dict, pagination_parameters: PaginationParameters):
        """
        List of products
        """
        queries = self.queries(query)
        products = Product.query.filter(*queries).paginate(
            page=pagination_parameters.page,
            per_page=pagination_parameters.page_size
        )
        return products.items

    @product_blp.arguments(ImageListCrudSchema, location="files")
    @product_blp.arguments(ProductCRUDSchema, location="form")
    @product_blp.response(201, ProductSchema)
    def post(self, images_data: list[FileStorage], product_data: dict):
        """
        Create product
        """
        images_data.extend(product_data.pop("images"))
        # save product
        product = Product(**product_data)
        db.session.add(product)
        # update images
        if images_data:
            process_instance_images(product, ProductImages, images_data)
        db.session.commit()
        return product


@product_blp.route("/<product_id>")
class ProductDetail(MethodView):
    @staticmethod
    def get_product(product_id):
        return Product.query.get_or_404({"id": product_id})

    @product_blp.response(200, ProductSchema)
    def get(self, product_id: str):
        """
        Get product by id
        """
        product = self.get_product(product_id)
        return product

    @product_blp.arguments(ImageListCrudSchema, location="files")
    @product_blp.arguments(ProductCRUDSchema, location="form")
    @product_blp.response(200, ProductSchema)
    def post(self, images_data: list[FileStorage], product_data: dict, product_id: str):
        """
        Update product by id
        """
        images_data.extend(product_data.pop("images"))
        product = self.get_product(product_id)
        # update product
        if product_data:
            product.set_from_dict(product_data)
        # update product images
        if images_data:
            process_instance_images(product, ProductImages, images_data)

        if product_data or images_data:
            product.updated_at = datetime.now()

        db.session.commit()
        return product

    @product_blp.response(204)
    def delete(self, product_id: str):
        """
        Delete product by id
        """
        product = self.get_product(product_id)
        db.session.delete(product)
        db.session.commit()


@product_blp.route("/<product_id>/variants")
class Variants(QueryUtils, MethodView):

    CUSTOM_QUERY = {
        "name": Variant.name.contains,
        "description": Variant.description.contains,
        "size": Variant.size,
        "colors": Variant.color
    }

    @product_blp.arguments(VariantQuerySchema, location="query")
    @product_blp.paginate()
    @product_blp.response(200, VariantSchema(many=True))
    def get(self, query: dict, pagination_parameters: PaginationParameters, product_id: str):
        """
        Product variants list
        """
        product = Product.query.get_or_404(product_id)
        variants = Variant.query.filter_by(product_id=product.id).filter(*self.queries(query)).paginate(
            page=pagination_parameters.page,
            per_page=pagination_parameters.page_size
        )
        return variants.items

    @product_blp.arguments(VariantsAddSchema, location="form")
    @product_blp.response(201, VariantSchema(many=True))
    def post(self, variants_data: list[dict], product_id: str):
        """
        Product add multiple variants
        """
        Product.query.get_or_404(product_id)
        variants = []
        for idx, data in enumerate(variants_data.get("variants")):
            images = data.pop("images", []) + request.files.getlist(f"images_{idx}")
            variant = Variant(**data)
            variants.append(variant)
            db.session.add(variant)

            if images:
                process_instance_images(variant, VariantImages, images)

        db.session.commit()
        return variants
