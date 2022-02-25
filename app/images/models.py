from app.settings import db
from depot.fields.sqlalchemy import UploadedFileField


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    # path = db.Column(db.String(300), nullable=False)
    file = db.Column(UploadedFileField(upload_storage='images'))
    logo_products = db.relationship("Product", back_populates="logo")
    logo_variants = db.relationship("Variant", back_populates="logo")
