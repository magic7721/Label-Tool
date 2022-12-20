import datetime
from app import db


class ImageSeries(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_name = db.Column(db.String(255), nullable=True)
    patient_id = db.Column(db.String(255), nullable=True)
    patient_birth_date = db.Column(db.String(255), nullable=True)
    patient_sex = db.Column(db.String(10), nullable=True)
    patient_age = db.Column(db.String(10), nullable=True)
    patient_weight = db.Column(db.String(10), nullable=True)
    patient_address = db.Column(db.String, nullable=True)
    patient_comments = db.Column(db.String, nullable=True)
    bethesda_level = db.Column(db.Integer, nullable=True)
    contour_color = db.Column(db.Integer, nullable=True)
    create_at = db.Column(db.DateTime, nullable=True)
    type = db.Column(db.Integer, nullable=True)
    contours = db.relationship('Contour', backref='image_series', cascade="all,delete", lazy=True)
    slices = db.relationship('Slice', backref='image_series', cascade="all,delete", lazy=True)
    images = db.relationship('Image', backref='image_series', cascade="all,delete", lazy=True)

    def __init__(self, patient_info, type):
        self.type = type
        self.create_at = datetime.datetime.now()
        self.patient_name = patient_info.get('patientName')
        self.patient_id = patient_info.get('patientID')
        self.patient_birth_date = patient_info.get('patientBirthDate')
        self.patient_sex = patient_info.get('patientSex')
        self.patient_age = patient_info.get('patientAge')
        self.patient_weight = patient_info.get('patientWeight')
        self.patient_address = patient_info.get('patientAddress')
        self.patient_comments = patient_info.get('patientComments')
        self.bethesda_level = patient_info.get('bethesdaLevel')
        self.contour_color = patient_info.get('contourColor')
        self.create_at = datetime.datetime.now()

