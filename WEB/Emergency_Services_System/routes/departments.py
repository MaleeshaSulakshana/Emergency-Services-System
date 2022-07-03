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


# Route for add department
@departments.route('/add_department_details', methods=['GET', 'POST'])
def add_department_details():

    if request.method == "POST":

        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            name = request.form.get('name')
            emergency_number_1 = request.form.get('emergency_number_1')
            emergency_number_2 = request.form.get('emergency_number_2')
            web_link = request.form.get('web_link')
            address = request.form.get('address')
            desc = request.form.get('desc')
            thumbnail = request.files.get('thumbnail')

            if (len(name) == 0 or len(emergency_number_1) == 0 or len(emergency_number_2) == 0 or len(web_link) == 0 or
                    len(address) == 0 or len(desc) == 0 or thumbnail == None):

                return jsonify({'error': "Fields are empty!"})

            else:

                department_id = ut.random_number_with_date()

                # Save uploaded images and get file names
                save_folder = os.path.join(
                    static_folder, 'static/images/departments_images/')
                thumbnail_name, extention = ut.file_save(
                    thumbnail, save_folder, department_id)

                data = {
                    'name': name,
                    'emergency_number_1': emergency_number_1,
                    'emergency_number_2': emergency_number_2,
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
