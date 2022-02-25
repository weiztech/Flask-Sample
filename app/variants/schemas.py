from marshmallow import pre_load, post_load, validates, ValidationError
from flask import request

from app.settings import ma, db
from app.common.functions import convert_raw_list
from app.images.schemas import ImageSchema
from app.images.models import Image

from .models import Variant


class VariantSchema(ma.SQLAlchemyAutoSchema):
    images = ma.Nested(ImageSchema, many=True)

    class Meta:
        model = Variant
        include_fk = True


class VariantQuerySchema(ma.SQLAlchemySchema):
    name = ma.auto_field(required=False)
    size = ma.auto_field(required=False)
    color = ma.auto_field(required=False)
    description = ma.auto_field(required=False)

    class Meta:
        model = Variant


class VariantCrudSchema(ma.SQLAlchemySchema):
    id = ma.auto_field(required=False)
    name = ma.auto_field()
    size = ma.auto_field()
    color = ma.auto_field()
    description = ma.auto_field()
    logo_id = ma.auto_field()
    images = ma.Nested(ImageSchema, many=True)
    delete = ma.Boolean(required=False, load_only=True)

    class Meta:
        model = Variant
        include_fk = True

    @pre_load
    def validate_data(self, data, **kwargs):
        product_id = request.view_args.get("product_id")
        variant_id = data.get("id")
        if product_id:
            if variant_id and not db.session.query(
                    Variant.query.filter_by(id=variant_id, product_id=product_id).exists()).scalar():
                raise ValidationError(f"Invalid variant id {variant_id}")

        if not isinstance(data, dict):
            images = data.getlist("images")
            data = data.to_dict()
        else:
            images = data.get("images")

        if images:
            data["images"] = convert_raw_list("images", images)

        return data

    @post_load
    def deserialize_data(self, data, **kwargs):
        product_id = request.view_args.get("product_id")
        if product_id:
            data["product_id"] = product_id

        return data

    @validates("logo_id")
    def validate_logo_id(self, logo_id, **kwargs):
        if logo_id is not None and not db.session.query(Image.query.filter_by(id=logo_id).exists()).scalar():
            raise ValidationError({"logo_id": "Logo not found"})


class VariantEditSchema(VariantCrudSchema):
    name = ma.auto_field(required=False)


class VariantsAddSchema(ma.Schema):
    variants = ma.Nested(VariantCrudSchema, many=True)

    @pre_load
    def validate_data(self, data, **kwargs):
        variants = data.getlist("variants")
        data = data.to_dict()
        if variants:
            variants = convert_raw_list("variants", variants)

        data["variants"] = variants
        return data
