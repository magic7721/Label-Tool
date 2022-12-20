from app import db
from app.models.contour import Contour
from flask import request, make_response, jsonify

from . import api


@api.route("/RTStruct/GetContourList", methods=["Get"])
def get_contour_list():
    series_id = request.args.get('seriesID', '')
    contours = Contour.query.filter_by(series_id=series_id).all()
    if contours is not None:
        response_object = {
            'status': 'success',
            'data': [],
        }
        for contour in contours:
            response_object['data'].append({
                'sliceLocation': contour.slice_location,
                'attributes': contour.attributes,
                'otherAttribute': contour.other_attr,
                'frameNumber': contour.frame_number,
                'knotFrames': contour.knot_frames,
                'points': contour.points,
            })
        return make_response(jsonify(response_object)), 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.',
        }

        return make_response(jsonify(response_object)), 401


@api.route("/RTStruct/SaveContours", methods=["Post"])
def save_contours():
    series_id = request.args.get('seriesID', '')
    Contour.query.filter_by(series_id=series_id).delete()
    contour_infos = request.get_json()
    if contour_infos is not None:
        for contour_info in contour_infos:
            contour = Contour(series_id, contour_info)
            db.session.add(contour)

    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'Save contours successful',
    }

    return make_response(jsonify(response_object)), 201
