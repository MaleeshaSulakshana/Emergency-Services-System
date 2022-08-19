import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

branches = Blueprint("branches", __name__, url_prefix="/branches",
                     template_folder='templates', static_folder="../static")

sys.path.append(os.path.abspath('../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import branches_queries as bq
import departments_queries as dq

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)
static_folder = os.path.dirname(root)


# Route for add branches
@branches.route('/add-branches')
def add_branches():
    if 'adminId' not in session:
        return redirect('/login')

    departments = dq.get_all_departments()
    return render_template('branches/add_branch.html', departments=departments)


# Route for view branches
@branches.route('/view-branches')
def view_branches():
    if 'adminId' not in session:
        return redirect('/login')

    branches_details = bq.get_all_branches()
    return render_template('branches/view_branches.html', branches=branches_details)


# Route for view branch details
@branches.route('/view-branch-details')
def view_department_details():
    if 'adminId' not in session:
        return redirect('/login')

    branch_id = request.args['id']

    details = bq.get_branch_account_details(branch_id)
    departments = dq.get_all_departments()

    return render_template('branches/view_branch_details.html', details=details, departments=departments)


# Route for add branch
@branches.route('/add_branch_details', methods=['GET', 'POST'])
def add_branch_details():

    if request.method == "POST":
        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:

            department = request.form.get('department')
            location = request.form.get('location')
            emergency_number = request.form.get('emergency_number')
            address = request.form.get('address')

            if (len(department) == 0 or len(location) == 0 or len(emergency_number) == 0 or len(address) == 0):
                return jsonify({'error': "Fields are empty!"})

            else:

                branch_id = ut.random_number_with_date()

                data = {
                    'department': department,
                    'location': location,
                    'emergency_number': emergency_number,
                    'address': address,
                    'branch_id': branch_id
                }

                is_created = bq.branches_registration(data)

                if is_created > 0:
                    return jsonify({'success': "Branch registered successfully!"})

                else:
                    return jsonify({'error': "Branch registered not successfully. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for update branch
@branches.route('/update_branch_details', methods=['GET', 'POST'])
def update_branch_details():

    if request.method == "POST":
        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:

            branch_id = request.form.get('id')
            department = request.form.get('department')
            location = request.form.get('location')
            emergency_number = request.form.get('emergency_number')
            address = request.form.get('address')

            if (len(branch_id) == 0 or len(department) == 0 or len(location) == 0 or len(emergency_number) == 0 or len(address) == 0):
                return jsonify({'error': "Fields are empty!"})

            else:

                data = {
                    'department': department,
                    'location': location,
                    'emergency_number': emergency_number,
                    'address': address,
                    'branch_id': branch_id
                }

                is_created = bq.branches_registration(data)

                if is_created > 0:
                    return jsonify({'success': "Branch details update successfully!"})

                else:
                    return jsonify({'error': "Branch details update not successfully. Please try again!"})

    return jsonify({'redirect': url_for('index')})
