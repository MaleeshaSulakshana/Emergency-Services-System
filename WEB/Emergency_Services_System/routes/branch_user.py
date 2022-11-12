import os
import sys
import hashlib
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

branch_user = Blueprint("branch_user", __name__, url_prefix="/branch_user",
                        template_folder='templates', static_folder="../static")

sys.path.append(os.path.abspath('../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import branch_user_queries as buq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)
static_folder = os.path.dirname(root)


# Route for view branch details
@branch_user.route('/view-branch-user-details')
def view_branch_user_details():
    if 'adminId' not in session:
        return redirect('/login')

    branch_user_id = request.args['id']

    details = buq.get_branch_user_account_details(branch_user_id)
    return render_template('branch_user/view_branch_user_details.html', details=details)


# Route for add branch
@branch_user.route('/add_branch_user', methods=['GET', 'POST'])
def add_branch_user():

    if request.method == "POST":
        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:

            branch_id = request.form.get('bid')
            name = request.form.get('buname')
            email = request.form.get('buemail')
            psw = request.form.get('bupsw')

            if (len(branch_id) == 0 or len(name) == 0 or len(email) == 0 or len(psw) == 0):
                return jsonify({'error': "Fields are empty!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()

                data = {
                    'branch_id': branch_id,
                    'name': name,
                    'email': email,
                    'psw': psw
                }

                is_created = buq.branch_user_registration(data)

                if is_created > 0:
                    return jsonify({'success': "Branch user registered successfully!"})

                else:
                    return jsonify({'error': "Branch user registered not successfully. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for add branch
@branch_user.route('/remove', methods=['GET', 'POST'])
def remove():

    if request.method == "POST":
        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:

            id = request.form.get('id')

            if (len(id) == 0):
                return jsonify({'error': "Fields are empty!"})

            else:

                is_created = buq.branch_user_remove(id)

                if is_created > 0:
                    return jsonify({'success': "Branch user remove successfully!"})

                else:
                    return jsonify({'error': "Branch user remove not successfully. Please try again!"})

    return jsonify({'redirect': url_for('index')})
