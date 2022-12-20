import os

from app import db
from app.models.image_series import ImageSeries
from app.models.slice import Slice
from app.models.image import Image
from app.models.user import User
from flask import request, make_response, jsonify
from werkzeug.utils import secure_filename

import uuid

from app.image_import_export import *
from . import api


@api.route("/Images/Upload", methods=["POST"])
def upload_dicom_files():
    files = request.files
    series_id = request.args.get('seriesID', '')
    staff_id = request.headers.get('StaffId')
    upload_folder = '{0}/dicom_storage/{1}/series_{2}'.format(os.getcwd(), staff_id, series_id)

    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)

    for file in files.getlist('dicom'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
    
    responseObject = {
        'status': 'success',
    }
    return make_response(jsonify(responseObject)), 201

@api.route("/Images/Create", methods=["POST"])
def create_image_series():
    access, msg = User.check_login(request.headers.get('Authorization'))
    if not access:
        responseObject = {
            'status': 'fail',
            'message': 'Authentication failed',
        }
        return make_response(jsonify(responseObject)), 401

    patient_info = request.get_json()
    try:
        user = User.query.filter_by(email=request.headers.get('StaffId')).first()
        series = ImageSeries(patient_info, user.type)

        # create th image series
        db.session.add(series)
        db.session.commit()

        responseObject = {
            'status': 'success',
            'message': 'Successfully created.',
            'data': series.id
        }
        return make_response(jsonify(responseObject)), 201
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return make_response(jsonify(responseObject)), 401


@api.route("/Images/DeleteSeries", methods=["POST"])
def delete_image_series():
    series_id = request.args.get('seriesID', '')
    series = ImageSeries.query.filter_by(id=series_id).first()
    if series is not None:
        db.session.delete(series)
        db.session.commit()
        responseObject = {
            'status': 'success',
        }
        return make_response(jsonify(responseObject)), 202
    else:
        responseObject = {
            'status': 'fail',
        }
        return make_response(jsonify(responseObject)), 402


@api.route('/Images/InsertImage', methods=['Post'])
def insert_image():
    series_id = request.args.get('seriesID', '')
    image_info = request.get_json()
    staff_id = request.headers.get('StaffId')

    image = Image(image_info)
    image_series_url = '{0}/image_storage/{1}/series_{2}'.format(os.getcwd(), staff_id, series_id)
    image_url = '{0}/{1}.jpg'.format(image_series_url, uuid.uuid1())
    if not os.path.isdir(image_series_url):
        os.mkdir(image_series_url)

    try:
        save_image(image_info['imageData'], image_url)
        image.image_url = image_url
        image.series_id = series_id
        slice = Slice.query.filter_by(location=image.location, series_id=series_id).first()
        if slice is None:
            slice = Slice(image, series_id)
            db.session.add(slice)
            db.session.commit()

    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }

        return make_response(jsonify(responseObject)), 400

    try:
        db.session.add(image)
        db.session.commit()
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }

        return make_response(jsonify(responseObject)), 400

    responseObject = {
        'status': 'success',
        'data': image.id,
    }
    return make_response(jsonify(responseObject)), 201


@api.route('/Images/UpdatePatientInfo', methods=['Post'])
def update_patient_info():
    series_id = request.args.get('seriesID', '')
    patient_info = request.get_json()
    series = ImageSeries.query.filter_by(id=series_id).first()
    if series is not None:
        series.patient_name = patient_info.get('patientName')
        series.patient_id = patient_info.get('patientID')
        series.patient_birth_date = patient_info.get('patientBirthDate')
        series.patient_sex = patient_info.get('patientSex')
        series.patient_age = patient_info.get('patientAge')
        series.patient_weight = patient_info.get('patientWeight')
        series.patient_address = patient_info.get('patientAddress')
        series.patient_comments = patient_info.get('patientComments')
        series.bethesda_level = patient_info.get('bethesdaLevel')
        series.contour_color = patient_info.get('contourColor')
        db.session.commit()
        responseObject = {
            'status': 'success'
        }
        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.',
        }

        return make_response(jsonify(responseObject)), 400


@api.route('/Images/GetPatientInfo', methods=['Post'])
def get_patient_info():
    series_id = request.args.get('seriesID', '')
    series = ImageSeries.query.filter_by(id=series_id).first()
    if series is not None:
        responseObject = {
            'status': 'success',
            'data': {
                'patientName': series.patient_name,
                'patientID': series.patient_id,
                'patientBirthDate': series.patient_birth_date,
                'patientSex': series.patient_sex,
                'patientAge': series.patient_age,
                'patientWeight': series.patient_weight,
                'patientAddress': series.patient_address,
                'patientComments': series.patient_comments,
                'bethesdaLevel': series.bethesda_level,
                'contourColor': series.contour_color,
            }
        }
        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.',
        }

        return make_response(jsonify(responseObject)), 400


@api.route('/Images/GetSeriesList', methods=['Post'])
def get_series_list():
    access, msg = User.check_login(request.headers.get('Authorization'))
    if not access:
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.',
        }

        return make_response(jsonify(responseObject)), 400

    try:
        user = User.query.filter_by(email=request.headers.get('StaffId')).first()
        series_list = ImageSeries.query.filter_by(type=user.type).all()

        if series_list is not None:
            responseObject = {
                'status': 'success',
                'data': [],
            }
            for series in series_list:
                responseObject['data'].append({
                    'seriesID': series.id,
                    'seriesName': series.patient_name,
                    'imageNumber': len(series.images),
                    'createAt': series.create_at
                })
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.',
            }
            return make_response(jsonify(responseObject)), 400

    except Exception as e:
        print(e)
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return make_response(jsonify(responseObject)), 401


@api.route('/Images/GetImagePixelData', methods=['Get'])
def get_image_pixel_data():
    image_id = request.args.get('imageID', '')
    image = Image.query.filter_by(id=image_id).first()

    if image is None:
        responseObject = {
            'status': 'success',
            'message': 'image not found',
        }

        return make_response(jsonify(responseObject)), 400
    else:
        image_data = get_image(image.image_url)
        responseObject = {
            'status': 'success',
            'data': image_data,
        }
        return make_response(jsonify(responseObject)), 200


@api.route('/Images/GetImageInfoList', methods=['Get'])
def get_all_image_info():
    seriesID = request.args.get('seriesID', '')

    slices = Slice.query.filter_by(series_id=seriesID).all()

    if slices is not None:
        responseObject = {
            'status': 'success',
            'data': [],
        }
        for slice in slices:
            images = Image.query.filter_by(series_id=seriesID, location=slice.location).all()
            imageIDList = [image.id for image in images]
            imageFileNames = [image.file_name for image in images]
            responseObject['data'].append({
                'imageIDs': imageIDList,
                'fileNames': imageFileNames,
                'rows': slice.rows,
                'columns': slice.columns,
                'rowPixelSpacing': slice.row_pixel_spacing,
                'columnPixelSpacing': slice.column_pixel_spacing,
                'location': slice.location,
                'seriesID': slice.series_id,
            })
        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.',
        }
        return make_response(jsonify(responseObject)), 400
