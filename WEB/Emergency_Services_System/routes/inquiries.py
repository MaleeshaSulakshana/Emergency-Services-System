import base64
import os
import sys
import hashlib
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

inquiries = Blueprint("inquiries", __name__, url_prefix="/inquiries",
                      template_folder='templates', static_folder="../static")

sys.path.append(os.path.abspath('../python/'))
sys.path.append(os.path.abspath('python/db/'))

# import utils as ut
# import mailer
# import user_queries as uq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)
static_folder = os.path.dirname(root)


# # Route for view inquiries
# @inquiries.route('/view-inquiries')
# def view_inquiries():
#     if 'adminId' not in session:
#         return redirect('/login')

#     inquiries = uq.get_all_inquiries()
#     return render_template('inquiries/view_inquiries.html', inquiries=inquiries)


# # Route for view inquiries
# @inquiries.route('/view-inquiries-details')
# def view_inquiries_details():
#     if 'adminId' not in session:
#         return redirect('/login')

#     user_id = request.args['id']
#     details = uq.get_account_details(user_id)
#     return render_template('inquiries/view_user_details.html', details=details)


# # Route for user login
# @inquiries.route('/login', methods=['GET', 'POST'])
# def login():

#     if request.method == "POST":

#         request_data = request.get_json()

#         email = request_data['email']
#         psw = request_data['psw']

#         if (len(email) == 0 or len(psw) == 0):

#             return jsonify({"status": "error", 'msg': "Fields are empty!"})

#         else:

#             psw = hashlib.md5(psw.encode()).hexdigest()

#             # Check email already exist
#             details = uq.is_exist_user_by_email_and_psw(email, psw)
#             if len(details) < 1:
#                 return jsonify({"status": "error", "msg": "Email or password incorrect!"})

#             else:
#                 return jsonify({"status": "success", "msg": "User login success.", "id": str(details[0][0]), "name": str(details[0][1]) + " " + str(details[0][2])})

#     return jsonify({"status": "error", 'msg': "Method invalid"})


# # Route for user register
# @inquiries.route('/register', methods=['GET', 'POST'])
# def register():

#     if request.method == "POST":

#         request_data = request.get_json()

#         first_name = request_data['first_name']
#         last_name = request_data['last_name']
#         email = request_data['email']
#         nic = request_data['nic']
#         number = request_data['number']
#         address = request_data['address']

#         if (len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or len(nic) == 0 or
#                 len(number) == 0 or len(address) == 0):

#             return jsonify({"status": "error", 'msg': "Fields are empty!"})

#         else:

#             gen_psw = ut.random_number()
#             psw = hashlib.md5(gen_psw.encode()).hexdigest()

#             data = {
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'email': email,
#                 'nic': nic,
#                 'number': number,
#                 'address': address,
#                 'psw': psw
#             }

#             # Check email already exist
#             is_exist = uq.is_exist_email_in_inquiries(email)
#             if is_exist[0][0] > 0:
#                 return jsonify({"status": "error", 'msg': "Email already exist!"})

#             else:
#                 is_created = uq.user_registration(data)

#                 subject = "Emergency Services System Account Password"
#                 msg = """Hi {} {}, <br>
#                         &emsp;Your account credentials is<br>
#                             &emsp;&emsp;Email : <b>{}</b><br>
#                             &emsp;&emsp;Password : <b>{}</b> <br><br>
#                         Thank you.""".format(str(first_name), str(last_name), str(email), str(gen_psw))

#                 if is_created > 0:
#                     mailer.send_mail(email, subject, msg)
#                     return jsonify({"status": "success", 'msg': "Password sent to mail and account has been created. Please sign in!"})

#                 else:
#                     return jsonify({"status": "error", 'msg': "Account not created. Please try again!"})

#     return jsonify({"status": "error", 'msg': "Method invalid"})


# @inquiries.route('/<id>', methods=['GET', 'POST'])
# def account_details(id):

#     details = uq.get_account_details(id)
#     return jsonify(details)


# # Route for user update profile
# @inquiries.route('/update', methods=['GET', 'POST'])
# def update():

#     if request.method == "POST":

#         request_data = request.get_json()

#         id = request_data['id']
#         first_name = request_data['first_name']
#         last_name = request_data['last_name']
#         email = request_data['email']
#         nic = request_data['nic']
#         number = request_data['number']
#         address = request_data['address']

#         if (len(id) == 0 or len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or len(nic) == 0 or
#                 len(number) == 0 or len(address) == 0):

#             return jsonify({"status": "error", 'msg': "Fields are empty!"})

#         else:

#             data = {
#                 'id': id,
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'email': email,
#                 'nic': nic,
#                 'number': number,
#                 'address': address
#             }

#             # print(data)

#             # Check email already exist
#             is_exist = uq.is_exist_email_in_inquiries(email)
#             if is_exist[0][0] < 1:
#                 return jsonify({"status": "error", 'msg': "Email not exist!"})

#             else:
#                 is_created = uq.update_user_details(data)
#                 if is_created > 0:
#                     return jsonify({"status": "success", 'msg': "Account has been updated."})

#                 else:
#                     return jsonify({"status": "error", 'msg': "Account not updated."})

#     return jsonify({'error': "Method invalid"})


# # Route for user update profile psw
# @inquiries.route('/update/psw', methods=['GET', 'POST'])
# def update_psw():

#     if request.method == "POST":

#         request_data = request.get_json()

#         id = request_data['id']
#         psw = request_data['psw']

#         if (len(id) == 0 or len(psw) == 0):

#             return jsonify({"status": "error", 'msg': "Fields are empty!"})

#         else:

#             psw = hashlib.md5(psw.encode()).hexdigest()

#             data = {
#                 'id': id,
#                 'psw': psw
#             }

#             # Check email already exist
#             is_exist = uq.is_exist_id_in_inquiries(id)
#             if is_exist[0][0] < 1:
#                 return jsonify({'error': "Email not exist!"})

#             else:
#                 is_created = uq.update_user_psw(data)
#                 if is_created > 0:
#                     return jsonify({"status": "success", 'msg': "Password has been updated."})

#                 else:
#                     return jsonify({"status": "error", 'msg': "Password not updated."})

#     return jsonify({"status": "error", 'msg': "Method invalid"})


# add_inquiry
@inquiries.route('/add_inquiry', methods=['GET', 'POST'])
def add_inquiry():

    images = request.json['images']
    details = request.json['details']
    location = request.json['location']
    contact = request.json['contact']
    user_id = request.json['user_id']
    branch = request.json['branch']

    if 'video' in request.json:
        video = request.json['video']

        print(f"********** {len(video)}")

        uploaded_video_path = os.path.join(
            root, 'static/videos/video1/')

        if not os.path.exists(uploaded_video_path):
            os.makedirs(uploaded_video_path)

        filename = user_id + ".mp4"

        img_url = uploaded_video_path + "/" + filename
        with open(img_url, "wb") as fh:
            fh.write(base64.b64decode(video))

    # if image == None:
    #     return jsonify({'error': "Image not uploaded"})

    # else:

    #     uploaded_img_path = os.path.join(
    #         root, 'static/images/inquiries_profile_pic/')

    #     if not os.path.exists(uploaded_img_path):
    #         os.makedirs(uploaded_img_path)

    #     filename = user_id + ".png"

    #     img_url = uploaded_img_path + "/" + filename
    #     with open(img_url, "wb") as fh:
    #         fh.write(base64.b64decode(image))

    #     if os.path.exists(img_url):
    #         is_updated = uq.update_profile_picture(user_id, filename)
    #         return jsonify({"status": "success", 'msg': "Profile picture uploaded."})

    #     return jsonify({"status": "error", 'msg': "Profile picture not uploaded."})

    return jsonify({"status": "error", 'msg': "Profile picture not uploaded."})
