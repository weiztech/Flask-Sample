from datetime import datetime

from app.settings import db
from app.common.models import ModelUtils


'''
class VariantImages(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    variant_id = db.Column(db.String(355), db.ForeignKey('variant.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
'''

VariantImages = db.Table(
    "VariantImages",
    db.Column("id", db.Integer, db.ForeignKey('variant.id')),
    db.Column("image_id", db.Integer, db.ForeignKey('image.id'))
    )


class Variant(ModelUtils, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    product_id = db.Column(db.String(355), db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates="variants")
    name = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True, default='')
    images = db.relationship('Image', secondary=VariantImages, backref='variants')
    logo_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    logo = db.relationship('Image', back_populates="logo_variants")

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)
