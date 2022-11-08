import base64
import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

inquiries = Blueprint("inquiries", __name__, url_prefix="/inquiries",
                      template_folder='templates', static_folder="../static")

sys.path.append(os.path.abspath('../python/'))
sys.path.append(os.path.abspath('python/db/'))
sys.path.append(os.path.abspath('python/prediction/'))

import utils as ut
import inquiry_queries as iq
import prediction

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)
static_folder = os.path.dirname(root)


# add_inquiry
@inquiries.route('/add_inquiry', methods=['GET', 'POST'])
def add_inquiry():

    images = request.json['images']
    details = request.json['details']
    location = request.json['location']
    contact = request.json['contact']
    user_id = request.json['user_id']
    branch = request.json['branch']
    lat = request.json['lat']
    lon = request.json['lon']
    date = ut.date_picker()

    video = ""
    if 'video' in request.json:
        video = request.json['video']

    if (len(images) == 0 or len(details) == 0 or len(location) == 0
            or len(contact) == 0 or len(branch) == 0 or len(lat) == 0 or len(lon) == 0):
        return jsonify({"status": "error", 'msg': "Fields are empty!"})

    else:

        rand_no = ut.random_number_with_date()

        inquiries_uploaded_images_pred_path = os.path.join(
            root, 'static/images/inquiries', rand_no)

        inquiries_uploaded_path = os.path.join(
            inquiries_uploaded_images_pred_path, "images")

        if not os.path.exists(inquiries_uploaded_path):
            os.makedirs(inquiries_uploaded_path)

        for image in enumerate(images):
            filename = rand_no + "_" + str(image[0]) + ".png"
            img_url = inquiries_uploaded_path + "/" + filename
            with open(img_url, "wb") as fh:
                fh.write(base64.b64decode(image[1]['image']))
                iq.add_inquiry_images(rand_no, filename)

        if os.path.exists(inquiries_uploaded_images_pred_path):
            predict_data = prediction.predict_images(
                inquiries_uploaded_images_pred_path)

            for pred in predict_data:
                iq.add_prediction(
                    pred['IMAGE_NAME'], pred['PREDICTED_CLASS'], pred['ACCURACY'])

        if video != "":
            iq.add_inquiry_video(rand_no, video)

        if os.path.exists(inquiries_uploaded_path):
            is_added = iq.add_inquiry_details(
                rand_no, details, location, contact, user_id, branch, lat, lon, date)
            if (is_added > 0):
                return jsonify({"status": "success", 'msg': "Inquiry details uploaded."})

        return jsonify({"status": "error", 'msg': "Inquiry details not uploaded."})


@inquiries.route('/<id>', methods=['GET', 'POST'])
def get_inquiry_by_id(id):

    details = iq.get_inquires_by_id(id)
    return jsonify(details)


@inquiries.route('/<id>/user', methods=['GET', 'POST'])
def get_inquiry_by_user_id(id):

    details = iq.get_inquires_by_user(id)
    return jsonify(details)


@inquiries.route('/<id>/actions', methods=['GET', 'POST'])
def get_inquiry_actions_by_id(id):

    details = iq.get_inquiry_action(id)
    return jsonify(details)


@inquiries.route('/<id>/comments', methods=['GET', 'POST'])
def get_inquiry_comments_by_id(id):

    details = iq.get_inquiry_comment(id)
    return jsonify(details)
