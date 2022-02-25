from datetime import datetime
from werkzeug.datastructures import FileStorage
from flask.views import MethodView
from flask_smorest import Blueprint

from app.settings import db
from app.images.schemas import ImageListCrudSchema
from app.images.functions import process_instance_images

from .schemas import VariantSchema, VariantEditSchema
from .models import Variant, VariantImages


variant_blp = Blueprint("variants", "variants", url_prefix="/variants", description="Variants API List")
variant_blp.DEFAULT_PAGINATION_PARAMETERS = {"page": 1, "page_size": 15, "max_page_size": 30}


@variant_blp.route("/<variant_id>")
class VariantDetail(MethodView):

    @variant_blp.arguments(VariantEditSchema, location="form")
    @variant_blp.arguments(ImageListCrudSchema, location="files")
    @variant_blp.response(200, VariantSchema)
    def post(self, variant_data: dict, images: list[FileStorage],  variant_id: str):
        """
        Update a variant
        """
        images.extend(variant_data.pop("images", []))
        variant = Variant.query.get_or_404(variant_id)
        variant.set_from_dict(variant_data)

        if images:
            process_instance_images(variant, VariantImages, images)

        if variant_id or images:
            variant.updated_at = datetime.now()
        db.session.commit()
        return variant

    @variant_blp.response(204)
    def delete(self, variant_id: str):
        """
        Delete a variant
        """
        variant = Variant.query.get_or_404(variant_id)
        db.session.delete(variant)
        db.session.commit()
