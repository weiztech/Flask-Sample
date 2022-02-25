from io import BytesIO

from flask import send_file
from flask.views import MethodView
from flask_smorest import Blueprint
from depot.manager import DepotManager
from flask_smorest.pagination import PaginationParameters

from .models import Image
from .schemas import ImageSchema


image_blp = Blueprint("images", "images", url_prefix="/images", description="Images API List")


@image_blp.route("/<image_id>")
class ImageView(MethodView):
    '''
    for Development or use storage `LocalStoredFile`
    '''
    @image_blp.response(200)
    def get(self, image_id: str):
        """
        Get image file object by id
        """
        image = DepotManager.get_file(f"images/{image_id}")
        return send_file(
            BytesIO(image.read()), mimetype='image/png', attachment_filename=image.name)


@image_blp.route("/")
class ImageListView(MethodView):
    '''
    List of images
    '''
    @image_blp.paginate()
    @image_blp.response(200, ImageSchema(many=True))
    def get(self, pagination_parameters: PaginationParameters):
        """
        Get list images
        """
        return Image.query.paginate(
            page=pagination_parameters.page,
            per_page=pagination_parameters.page_size
        ).items
