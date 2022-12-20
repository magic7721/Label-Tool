from app import db
from app.models.image import Image


class Slice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rows = db.Column(db.Integer, nullable=True)
    columns = db.Column(db.Integer, nullable=True)
    row_pixel_spacing = db.Column(db.Float, nullable=True)
    column_pixel_spacing = db.Column(db.Float, nullable=True)
    location = db.Column(db.Integer, nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey('image_series.id'), nullable=False)

    def __init__(self, image: Image, series_id: int):
        self.rows = image.rows
        self.columns = image.columns
        self.row_pixel_spacing = image.row_pixel_spacing
        self.column_pixel_spacing = image.column_pixel_spacing
        self.location = image.location
        self.series_id = series_id
