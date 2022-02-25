from flask import request
from slugify import slugify
from marshmallow import pre_load, ValidationError, validates

from app.settings import ma
from app.variants.schemas import VariantSchema
from app.images.schemas import ImageSchema
from app.images.models import Image
from app.common.functions import convert_raw_list

from .models import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    images = ma.Nested(ImageSchema, many=True)

    class Meta:
        model = Product
        include_fk = True


class ProductDetailSchema(ma.SQLAlchemyAutoSchema):
    images = ma.Nested(ImageSchema, many=True)
    variants = ma.Nested(VariantSchema, many=True)

    class Meta:
        model = Product
        include_fk = True


class ProductQuerySchema(ma.SQLAlchemySchema):
    name = ma.auto_field(required=False)
    description = ma.auto_field(required=False)

    class Meta:
        model = Product


class ProductCRUDSchema(ma.SQLAlchemySchema):
    id = ma.auto_field(required=False)
    name = ma.auto_field()
    description = ma.auto_field()
    images = ma.Nested(ImageSchema, many=True)
    logo_id = ma.auto_field()

    class Meta:
        model = Product

    def validate_images(self, data, images_data):
        '''
        process images data
        '''
        field_name = "images"
        data[field_name] = convert_raw_list(field_name, images_data)

    def validate_id(self, data):
        '''
        slugify id by data `id` or `name` and set `id` as slug if not exists
        '''
        edit_product_id = request.view_args.get("product_id")
        product_id = slugify(data.get("id") or data.get("name") or edit_product_id)
        if edit_product_id != product_id and Product.query.filter_by(id=product_id).first():
            raise ValidationError({"id": "Product id already exists"})

        if not edit_product_id:
            data["id"] = product_id

    @pre_load
    def validate_data(self, data, **kwargs):
        is_edit = request.view_args.get("product_id")
        if is_edit:
            self.fields["name"].required = False

        images = data.getlist("images")
        data = data.to_dict()
        self.validate_id(data)
        self.validate_images(data, images)
        return data

    @validates("logo_id")
    def validate_logo_id(self, logo_id, **kwargs):
        if logo_id is not None and not Image.query.filter_by(id=logo_id).first():
            raise ValidationError({"logo_id": "Logo not found"})
