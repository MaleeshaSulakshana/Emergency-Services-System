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

            # print(data)

            # Check email already exist
            is_exist = uq.is_exist_email_in_users(email)
            if is_exist[0][0] > 0:
                return jsonify({'error': "Email already exist!"})

            else:
                is_created = uq.user_registration(data)
                if is_created > 0:
                    return jsonify({'success': "Account has been created. Please sign in!"})

                else:
                    return jsonify({'error': "Account not created. Please try again!"})

    return jsonify({'error': "Method invalid"})


# Route for user update profile
@users.route('/update', methods=['GET', 'POST'])
def update():

    if request.method == "POST":

        request_data = request.get_json()

        first_name = request_data['first_name']
        last_name = request_data['last_name']
        email = request_data['email']
        nic = request_data['nic']
        number = request_data['number']
        address = request_data['address']

        if (len(first_name) == 0 or len(last_name) == 0 or len(email) == 0 or len(nic) == 0 or
                len(number) == 0 or len(address) == 0):

            return jsonify({'error': "Fields are empty!"})

        else:

            psw = hashlib.md5(psw.encode()).hexdigest()

            data = {
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
                    return jsonify({'success': "Account has been updated."})

                else:
                    return jsonify({'error': "Account not updated."})

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
