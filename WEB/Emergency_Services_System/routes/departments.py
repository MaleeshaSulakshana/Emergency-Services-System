import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

departments = Blueprint("departments", __name__, url_prefix="/departments",
                        template_folder='templates', static_folder="../static")

sys.path.append(os.path.abspath('../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import departments_queries as dq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)
static_folder = os.path.dirname(root)


# Route for add departments
@departments.route('/add-departments')
def add_departments():
    if 'adminId' not in session:
        return redirect('/login')

    return render_template('departments/add_department.html')


# Route for view departments
@departments.route('/view-departments')
def view_departments():
    if 'adminId' not in session:
        return redirect('/login')

    departments = dq.get_all_departments()
    return render_template('departments/view_departments.html', departments=departments)


# Route for view departments details
@departments.route('/view-department-details')
def view_department_details():
    if 'adminId' not in session:
        return redirect('/login')

    department_id = request.args['id']
    details = dq.get_departments_account_details(department_id)
    return render_template('departments/view_department_details.html', details=details)


# Route for add department
@departments.route('/add_department_details', methods=['GET', 'POST'])
def add_department_details():

    if request.method == "POST":

        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            name = request.form.get('name')
            emergency_number = request.form.get('emergency_number')
            web_link = request.form.get('web_link')
            address = request.form.get('address')
            desc = request.form.get('desc')
            thumbnail = request.files.get('thumbnail')

            if (len(name) == 0 or len(emergency_number) == 0 or len(web_link) == 0 or
                    len(address) == 0 or len(desc) == 0 or thumbnail == None):

                return jsonify({'error': "Fields are empty!"})

            else:

                department_id = name.replace(
                    " ", "").strip() + ut.random_number_with_date()

                # Save uploaded images and get file names
                save_folder = os.path.join(
                    root, 'static/images/departments_images/')

                thumbnail_name, extention = ut.file_save(
                    thumbnail, save_folder, department_id)

                data = {
                    'name': name,
                    'emergency_number': emergency_number,
                    'web_link': web_link,
                    'address': address,
                    'desc': desc,
                    'department_id': department_id,
                    'thumbnail': thumbnail_name
                }

                is_created = dq.departments_registration(data)
                if is_created > 0:
                    return jsonify({'success': "Department registered successfully!"})

                else:
                    return jsonify({'error': "Department registered not successfully. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for update department
@departments.route('/update_department_details', methods=['GET', 'POST'])
def update_department_details():

    if request.method == "POST":

        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            department_id = request.form.get('id')
            name = request.form.get('name')
            emergency_number = request.form.get('emergency_number')
            web_link = request.form.get('web_link')
            address = request.form.get('address')
            desc = request.form.get('desc')

            if (len(department_id) == 0 or len(emergency_number) == 0 or len(web_link) == 0 or
                    len(address) == 0 or len(desc) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                data = {
                    'name': name,
                    'emergency_number': emergency_number,
                    'web_link': web_link,
                    'address': address,
                    'desc': desc,
                    'department_id': department_id
                }

                is_updated = dq.departments_update(data)
                if is_updated > 0:
                    return jsonify({'success': "Department details update successfully!"})

                else:
                    return jsonify({'error': "Department details update not successfully. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# For mobile app
# Route for get departments
@departments.route('/', methods=['GET', 'POST'])
def get_all_departments():

    details = dq.get_all_departments()
    return jsonify(details)


# Route for get department details by id
@departments.route('/<id>', methods=['GET', 'POST'])
def get_department(id):

    details = dq.get_departments_account_details(id)
    return jsonify(details)
