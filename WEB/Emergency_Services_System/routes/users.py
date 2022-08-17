import os
import sys
import hashlib
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

users = Blueprint("users", __name__, url_prefix="/users",
                  template_folder='templates', static_folder="../static")

sys.path.append(os.path.abspath('../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import users_queries as uq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)
static_folder = os.path.dirname(root)


# Route for user login
@users.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        request_data = request.get_json()

        email = request_data['email']
        psw = request_data['psw']

        if (len(email) == 0 or len(psw) == 0):

            return jsonify({'error': "Fields are empty!"})

        else:

            psw = hashlib.md5(psw.encode()).hexdigest()

            # Check email already exist
            details = uq.is_exist_user_by_email_and_psw(email, psw)
            if len(details) < 1:
                return jsonify({"status": "error", "msg": "Email or password incorrect!"})

            else:
                return jsonify({"status": "success", "msg": "User login success.", "id": str(details[0][0]), "name": str(details[0][1]) + " " + str(details[0][2])})

    return jsonify({'error': "Method invalid"})


# Route for user register
@users.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        request_data = request.get_json()

        first_name = request_data['first_name']
        last_name = request_data['last_name']
        email = request_data['email']
        nic = request_data['nic']
        number = request_data['number']
        address = request_data['address']
        psw = request_data['psw']

        if (len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or len(nic) == 0 or
                len(number) == 0 or len(address) == 0 or len(psw) == 0):

            return jsonify({'error': "Fields are empty!"})

        else:

            psw = hashlib.md5(psw.encode()).hexdigest()

            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'nic': nic,
                'number': number,
                'address': address,
                'psw': psw
            }

            # Check email already exist
            is_exist = uq.is_exist_email_in_users(email)
            if is_exist[0][0] > 0:
                return jsonify({"status": "error", 'msg': "Email already exist!"})

            else:
                is_created = uq.user_registration(data)
                if is_created > 0:
                    return jsonify({"status": "success", 'msg': "Account has been created. Please sign in!"})

                else:
                    return jsonify({"status": "error", 'msg': "Account not created. Please try again!"})

    return jsonify({'error': "Method invalid"})


@users.route('/<id>', methods=['GET', 'POST'])
def account_details(id):

    details = uq.get_account_details(id)
    return jsonify(details)


# Route for user update profile
@users.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == "POST":

        request_data = request.get_json()

        id = request_data['id']
        first_name = request_data['first_name']
        last_name = request_data['last_name']
        email = request_data['email']
        nic = request_data['nic']
        number = request_data['number']
        address = request_data['address']

        if (len(id) == 0 or len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or len(nic) == 0 or
                len(number) == 0 or len(address) == 0):

            return jsonify({'error': "Fields are empty!"})

        else:

            data = {
                'id': id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'nic': nic,
                'number': number,
                'address': address
            }

            # print(data)

            # Check email already exist
            is_exist = uq.is_exist_email_in_users(email)
            if is_exist[0][0] < 1:
                return jsonify({'error': "Email not exist!"})

            else:
                is_created = uq.update_user_details(data)
                if is_created > 0:
                    return jsonify({"status": "success", 'msg': "Account has been updated."})

                else:
                    return jsonify({"status": "error", 'msg': "Account not updated."})

    return jsonify({'error': "Method invalid"})


# Route for user update profile psw
@users.route('/update/psw', methods=['GET', 'POST'])
def update_psw():

    if request.method == "POST":

        request_data = request.get_json()

        email = request_data['email']
        psw = request_data['psw']

        if (len(email) == 0 or len(psw) == 0):

            return jsonify({'error': "Fields are empty!"})

        else:

            psw = hashlib.md5(psw.encode()).hexdigest()

            data = {
                'email': email,
                'psw': psw
            }

            # Check email already exist
            is_exist = uq.is_exist_email_in_users(email)
            if is_exist[0][0] < 1:
                return jsonify({'error': "Email not exist!"})

            else:
                is_created = uq.update_user_psw(data)
                if is_created > 0:
                    return jsonify({'success': "Account has been updated."})

                else:
                    return jsonify({'error': "Account not updated."})

    return jsonify({'error': "Method invalid"})
