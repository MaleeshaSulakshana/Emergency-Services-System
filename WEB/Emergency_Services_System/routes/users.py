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

        name = request_data['name']
        nic = request_data['nic']
        address = request_data['address']
        number = request_data['number']
        psw = request_data['psw']

        if (len(name) == 0 or len(nic) == 0 or len(address) == 0 or len(number) == 0 or len(psw) == 0):

            return jsonify({'error': "Fields are empty!"})

        else:

            psw = hashlib.md5(psw.encode()).hexdigest()

            data = {
                'name': name,
                'nic': nic,
                'address': address,
                'number': number,
                'psw': psw
            }

            print(data)

            # Check number already exist
            is_exist = uq.is_exist_number(number)
            if is_exist[0][0] > 0:
                return jsonify({'error': "Mobile number already exist!"})

            else:
                is_created = uq.user_registration(data)
                if is_created > 0:
                    return jsonify({'success': "Account has been created. Please sign in!"})

                else:
                    return jsonify({'error': "Account not created. Please try again!"})

    return jsonify({'error': "Method invalid"})
