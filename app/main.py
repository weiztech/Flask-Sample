import os

import click

from app.images import models as imodels
from app.products import models as pmodels
from app.variants import models as vsmodels

from app.products.views import product_blp
from app.images.views import image_blp
from app.variants.views import variant_blp

from .settings import api, app, db

FILE_PATH = os.path.dirname(os.path.abspath(__file__))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    click.echo('Initialized the database.')

    im, im1 = imodels.Image(file=open(os.path.join(FILE_PATH, "media/image-potrait_op_1.jpeg"), "rb")),\
        imodels.Image(file=open(os.path.join(FILE_PATH, "media/bg_landscape_op_0.12.jpg"), "rb"))
    db.session.add_all([im, im1])
    # db.session.commit()
    pd = pmodels.Product(id="laser-beem", name="Laser Beem", logo_id=im.id, images=[im, im1])
    pd1 = pmodels.Product(id="laser-Gold", name="Laser Gold", logo_id=im1.id, images=[im1])
    db.session.add_all([pd, pd1])
    # db.session.commit()
    vd = vsmodels.Variant(name="Laser X Beem", product=pd, logo=im1)
    vd1 = vsmodels.Variant(name="Laser G Beem", product=pd, logo=im)
    db.session.add_all([vd, vd1])
    db.session.commit()

    click.echo('Sample data created successfully.')


def create_app():
    for blp in (product_blp, image_blp, variant_blp):
        api.register_blueprint(blp)

    app.cli.add_command(init_db_command)
    return app


create_app()
