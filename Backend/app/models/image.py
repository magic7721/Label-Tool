from app import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rows = db.Column(db.Integer, nullable=True)
    columns = db.Column(db.Integer, nullable=True)
    row_pixel_spacing = db.Column(db.Float, nullable=True)
    column_pixel_spacing = db.Column(db.Float, nullable=True)
    location = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(512), nullable=True)
    frame_idx = db.Column(db.Integer, default=0)
    file_name = db.Column(db.String(512), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey('image_series.id'), nullable=False)

    def __init__(self, image_info):
        self.location = image_info.get('location')
        self.rows = image_info.get('rows')
        self.columns = image_info.get('columns')
        self.row_pixel_spacing = image_info.get('rowPixelSpacing')
        self.column_pixel_spacing = image_info.get('columnPixelSpacing')
        self.file_name = image_info.get('fileName')
        if type(image_info.get('frameIndex')) is int:
            self.frame_idx = image_info.get('frameIndex')
