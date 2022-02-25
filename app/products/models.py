from datetime import datetime

from app.settings import db
from app.common.models import ModelUtils

'''
class ProductImages(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    product_id = db.Column(db.String(355), db.ForeignKey('product.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
'''

ProductImages = db.Table(
    "ProductImages",
    db.Column("id", db.String(355), db.ForeignKey('product.id')),
    db.Column("image_id", db.Integer, db.ForeignKey('image.id'))
    )


class Product(ModelUtils, db.Model):
    id = db.Column(db.String(355), primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True, default='')
    images = db.relationship('Image', secondary=ProductImages, backref='products')
    logo_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    logo = db.relationship('Image', back_populates="logo_products")
    variants = db.relationship("Variant", back_populates="product")

    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    def set_from_dict(self, dict_data):
        for field, value in dict_data.items():
            setattr(self, field, value)
