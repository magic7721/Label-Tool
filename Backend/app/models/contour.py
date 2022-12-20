from app import db


class Contour(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attributes = db.Column(db.String(512), nullable=True)
    other_attr = db.Column(db.String, nullable=True)
    frame_number = db.Column(db.Integer, default=0)
    slice_location = db.Column(db.Integer, default=0)
    knot_frames = db.Column(db.String, nullable=True)
    points = db.Column(db.String, nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey('image_series.id'), nullable=False)

    def __init__(self, series_id, contour_info):
        self.series_id = series_id
        self.slice_location = contour_info.get('sliceLocation')
        self.attributes = '|'.join(str(p) for p in contour_info.get('attributes'))
        self.other_attr = contour_info.get('otherAttribute')
        self.frame_number = 1
        self.knot_frames = contour_info.get('knotFrames')

        if type(contour_info.get('frameNumber')) is int:
            self.frame_number = contour_info.get('frameNumber')

        if contour_info.get('points') is not None:
            frame_points = []
            for i in range(self.frame_number):
                frame_points.append('|'.join(str(p) for p in contour_info.get('points')[i]))

            self.points = ';'.join(frame_points)
