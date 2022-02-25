from werkzeug.datastructures import FileStorage

from app.settings import db
from app.images.models import Image


def process_instance_images(instance: db.Model, proxy_table: db.Table, images_data: list[FileStorage, dict]):
    '''
    Handle instance images on action: create, edit, and remove
    '''
    remove_images = []
    for image in images_data:
        if isinstance(image, FileStorage):
            image_instance = Image(file=image)
            db.session.add(image_instance)
            instance.images.append(image_instance)
            continue
        elif isinstance(image, dict):
            id = image.get("id")
            is_delete = image.get("delete")
            if not id:
                continue

            if is_delete:
                remove_images.append(id)
                continue

            instance.images.append(Image.query.get(id))

    if remove_images:
        db.session.execute(
            proxy_table.delete()
                       .where(proxy_table.columns.id == instance.id)
                       .where(proxy_table.columns.image_id.in_(remove_images))
        )
