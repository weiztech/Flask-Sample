from flask import current_app
from flask_smorest.fields import Upload
from marshmallow import ValidationError, post_load, pre_load, EXCLUDE, validates

from app.settings import ma, db

from .models import Image


class ImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Image
        unknown = EXCLUDE

    id = ma.auto_field()
    url = ma.Method("get_file_url")
    delete = ma.Boolean(required=False, load_only=True)

    def get_file_url(self, obj):
        if (obj.file.file.public_url):
            return obj.file.file.public_url
        return f"{current_app.config['HOST']}/{obj.file.path}"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["id"].required = False

    @validates("id")
    def validate_id(self, id, **kwargs):
        if not id:
            return

        if not db.session.query(Image.query.filter_by(id=id).exists()).scalar():
            raise ValidationError({"id": "Image id not found"})


class ImageCrudSchema(ma.SQLAlchemySchema):
    id = ma.auto_field()
    delete = ma.Boolean(required=False)

    class Meta:
        model = Image

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["id"].required = False


class ImageListCrudSchema(ma.Schema):
    images = ma.List(Upload(), required=False)

    @pre_load(pass_many=True)
    def validate_new_images(self, data, many, **kwargs):
        new_images = data.get("images")
        if not new_images:
            return data

        images = []
        for image in new_images:
            images.append(image)

        return {"images": images}

    @post_load
    def deserialize_data(self, data, **kwargs):
        return data.get("images", [])
