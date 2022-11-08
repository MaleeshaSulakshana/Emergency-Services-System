import hashlib
import os
import sys
from datetime import datetime
from flask import Blueprint, render_template, redirect, jsonify, url_for, request, session

branch = Blueprint("branch", __name__, url_prefix="/branch",
                   template_folder='templates', static_folder="../../static")

sys.path.append(os.path.abspath('../../python/'))
sys.path.append(os.path.abspath('python/db/'))

import utils as ut
import inquiry_queries as iq
import branches_queries as bq
import users_queries as uq
import branch_user_queries as buq
import departments_queries as dq

import mailer

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)
static_folder = os.path.dirname(root)


# Route for branch index/home page
@branch.route('/')
@branch.route('index')
def index():
    if 'branchUserId' not in session:
        return redirect('/login')

    details = iq.get_inquires_by_branch(session['branchId'], "pending")
    return render_template('_branch/index.html', details=details)


# Route for view ongoing inquires
@branch.route('ongoing')
def ongoing():
    if 'branchUserId' not in session:
        return redirect('/login')

    details = iq.get_inquires_by_branch(session['branchId'], "ongoing")
    return render_template('_branch/ongoing_inquiries.html', details=details)


# Route for view completed inquires
@branch.route('completed')
def completed():
    if 'branchUserId' not in session:
        return redirect('/login')

    details = iq.get_inquires_by_branch(session['branchId'], "completed")
    return render_template('_branch/completed_inquiries.html', details=details)


# Route for view branch user profile
@branch.route('/profile')
def profile():
    if 'branchUserId' not in session:
        return redirect('/login')

    details = buq.get_branch_user_account_details(session['branchUserId'])
    return render_template('_branch/profile/profile.html', details=details)


# Route for sign out
@branch.route('/sign-out')
def signout():
    if 'branchUserId' in session:
        session.pop('branchId', None)
        session.pop('branchUserId', None)
        session.pop('email', None)
        session.pop('name', None)

    return redirect(url_for('index'))


# Route for branch user login
@branch.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('index')})

        elif 'branchUserId' in session:
            return jsonify({'redirect': url_for('branch.index')})

        else:
            email = request.form.get('email')
            psw = request.form.get('psw')
            branch = request.form.get('branch')

            if (len(email) == 0 or len(psw) == 0 or branch == 'none'):
                return jsonify({'error': "Fields are empty!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()

                if branch != 'admin':

                    # Check email already exist
                    details = buq.branch_user_login(email, psw)

                    if len(details) > 0:
                        session['branchId'] = str(details[0][1])
                        session['branchUserId'] = str(details[0][0])
                        session['email'] = str(details[0][3])
                        session['name'] = str(details[0][2])

                        return jsonify({'redirect': url_for('branch.index')})

                return jsonify({'error': "Sign in failed. Please try again!"})

    return jsonify({'error': "Sign in failed"})


# Route for view inquiry details
@branch.route('/view-inquiry-details')
def view_inquiry_details():
    if 'branchUserId' not in session:
        return redirect('/login')

    status = [["Pending", "pending"], [
        "Ongoing", "ongoing"], ["Completed", "completed"]]

    id = request.args['id']

    details = iq.get_inquiry_by_id(id)
    images = iq.get_inquiry_images(id)
    videos = iq.get_inquiry_video(id)
    actions = iq.get_inquiry_action(id)
    comments = iq.get_inquiry_comment(id)
    branches = bq.get_all_branches()

    return render_template('_branch/view_inquiry_details.html', details=details, images=images, videos=videos, actions=actions, comments=comments, branches=branches, status=status)


# Route for update_inquiry_branch
@branch.route('/update_inquiry_branch', methods=['GET', 'POST'])
def update_inquiry_branch():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('index')})

        elif 'branchUserId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            id = request.form.get('id')
            branch = request.form.get('branch')
            cbranch = request.form.get('cbranch')
            nbranch = request.form.get('nbranch')

            if (len(id) == 0 or branch == "none" or len(cbranch) == 0 or len(nbranch) == 0):
                return jsonify({'error': "Fields are empty!"})

            else:

                inquiry = iq.get_inquiry_by_id(id)
                user = uq.get_account_details(inquiry[0][5])

                c_date_time = ut.date_time_picker()

                is_updated = iq.update_inquiry_branch(id, branch)

                if is_updated > 0:
                    iq.add_inquiry_action(
                        id, cbranch, session['branchUserId'], f"department or branch change from {str(inquiry[0][11])} - {str(inquiry[0][12])} to {nbranch.strip()}", c_date_time)

                    subject = "Changed Department or Branch"
                    msg = """Hi {} {}, <br>
                            &emsp;Your ({}) inquiry branch or department change from <b>{} - {}</b> to <b>{}</b><br><br>
                            Thank you.""".format(str(user[0][1]), str(user[0][2]), str(inquiry[0][1]), str(inquiry[0][11]), str(inquiry[0][12]), str(nbranch.strip()))

                    mailer.send_mail(user[0][3], subject, msg)

                    return jsonify({"success": "Inquiry branch update successfully!"})

        return jsonify({"error": "Inquiry branch not updated!"})

    return jsonify({'redirect': url_for('branch.index')})


# Route for update_inquiry_status
@branch.route('/update_inquiry_status', methods=['GET', 'POST'])
def update_inquiry_status():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('index')})

        elif 'branchUserId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            id = request.form.get('id')
            status = request.form.get('status')

            if (len(id) == 0 or status == "none"):
                return jsonify({'error': "Fields are empty!"})

            else:

                inquiry = iq.get_inquiry_by_id(id)
                user = uq.get_account_details(inquiry[0][5])
                c_date_time = ut.date_time_picker()

                is_updated = iq.update_inquiry_status(id, status)

                if is_updated > 0:

                    iq.add_inquiry_action(
                        id, inquiry[0][6], session['branchUserId'], f"Status change from {inquiry[0][9]} to {status.strip()}", c_date_time)

                    subject = "Changed Inquiry Status"
                    msg = """Hi {} {}, <br>
                            &emsp;Your ({}) inquiry status change from <b>{}</b> to <b>{}</b><br><br>
                            Thank you.""".format(str(user[0][1]), str(user[0][2]), str(inquiry[0][1]), str(inquiry[0][9]), str(status.strip()))

                    mailer.send_mail(user[0][3], subject, msg)

                    return jsonify({"success": "Inquiry status update successfully!"})

        return jsonify({"error": "Inquiry status not updated!"})

    return jsonify({'redirect': url_for('branch.index')})


# Route for add_inquiry_actions
@branch.route('/add_inquiry_actions', methods=['GET', 'POST'])
def add_inquiry_actions():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('index')})

        elif 'branchUserId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            id = request.form.get('id')
            action = request.form.get('action')

            if (len(id) == 0 or len(action) == 0):
                return jsonify({'error': "Fields are empty!"})

            else:

                inquiry = iq.get_inquiry_by_id(id)
                user = uq.get_account_details(inquiry[0][5])
                c_date_time = ut.date_time_picker()

                is_updated = iq.add_inquiry_action(
                    id, session['branchId'], session['branchUserId'], action, c_date_time)

                if is_updated > 0:

                    subject = "Got Action"
                    msg = """Hi {} {}, <br>
                            &emsp;Got action for your ({}) inquiry. Check your inquires on app.<br><br>
                            Thank you.""".format(str(user[0][1]), str(user[0][2]), str(inquiry[0][1]))

                    mailer.send_mail(user[0][3], subject, msg)

                    return jsonify({"success": "Inquiry action added successfully!"})

        return jsonify({"error": "Inquiry action not added!"})

    return jsonify({'redirect': url_for('branch.index')})


# # Route for add branches
# @branches.route('/add-branches')
# def add_branches():
#     if 'adminId' not in session:
#         return redirect('/login')

#     departments = dq.get_all_departments()
#     return render_template('branches/add_branch.html', departments=departments)


# # Route for view branches
# @branches.route('/view-branches')
# def view_branches():
#     if 'adminId' not in session:
#         return redirect('/login')

#     branches_details = bq.get_all_branches()
#     return render_template('branches/view_branches.html', branches=branches_details)


# # Route for view branch details
# @branches.route('/view-branch-details')
# def view_department_details():
#     if 'adminId' not in session:
#         return redirect('/login')

#     branch_id = request.args['id']

#     details = bq.get_branch_account_details(branch_id)
#     departments = dq.get_all_departments()
#     branch_users = buq.get_all_branch_users_by_branch(branch_id)

#     return render_template('branches/view_branch_details.html', details=details, departments=departments, branch_users=branch_users)


# # Route for add branch
# @branches.route('/add_branch_details', methods=['GET', 'POST'])
# def add_branch_details():

#     if request.method == "POST":
#         if 'adminId' not in session:
#             return jsonify({'redirect': url_for('login')})

#         else:
#             department = request.form.get('department')
#             location = request.form.get('location')
#             emergency_number = request.form.get('emergency_number')
#             address = request.form.get('address')
#             map_url = request.form.get('map_url')

#             if (len(department) == 0 or len(location) == 0 or len(emergency_number) == 0 or len(address) == 0 or len(map_url) == 0):
#                 return jsonify({'error': "Fields are empty!"})

#             else:

#                 branch_id = ut.random_number_with_date()

#                 data = {
#                     'department': department,
#                     'location': location,
#                     'emergency_number': emergency_number,
#                     'address': address,
#                     'branch_id': branch_id,
#                     'map_url': map_url
#                 }

#                 is_created = bq.branches_registration(data)

#                 if is_created > 0:
#                     return jsonify({'success': "Branch registered successfully!"})

#                 else:
#                     return jsonify({'error': "Branch registered not successfully. Please try again!"})

#     return jsonify({'redirect': url_for('index')})


# # Route for update branch
# @branches.route('/update_branch_details', methods=['GET', 'POST'])
# def update_branch_details():

#     if request.method == "POST":
#         if 'adminId' not in session:
#             return jsonify({'redirect': url_for('login')})

#         else:

#             branch_id = request.form.get('id')
#             department = request.form.get('department')
#             location = request.form.get('location')
#             emergency_number = request.form.get('emergency_number')
#             address = request.form.get('address')
#             map_url = request.form.get('map_url')

#             if (len(branch_id) == 0 or len(department) == 0 or len(location) == 0 or
#                 len(emergency_number) == 0 or len(address) == 0 or len(map_url) == 0):
#                 return jsonify({'error': "Fields are empty!"})

#             else:

#                 data = {
#                     'department': department,
#                     'location': location,
#                     'emergency_number': emergency_number,
#                     'address': address,
#                     'branch_id': branch_id,
#                     'map_url': map_url
#                 }

#                 is_created = bq.branch_details_update(data)

#                 if is_created > 0:
#                     return jsonify({'success': "Branch details update successfully!"})

#                 else:
#                     return jsonify({'error': "Branch details update not successfully. Please try again!"})

#     return jsonify({'redirect': url_for('index')})


# # Route for remove branch
# @branches.route('/remove_branch_details', methods=['GET', 'POST'])
# def remove_branch_details():

#     if request.method == "POST":
#         if 'adminId' not in session:
#             return jsonify({'redirect': url_for('login')})

#         else:

#             branch_id = request.form.get('id')

#             if (len(branch_id) == 0):
#                 return jsonify({'error': "Fields are empty!"})

#             else:

#                 is_available = buq.get_branch_user_count(branch_id)[0][0]

#                 if is_available != 0:
#                     return jsonify({'error': "Branch users available. Please delete them!"})

#                 is_deleted = bq.branch_details_remove(branch_id)

#                 if is_deleted > 0:
#                     return jsonify({'success': "Branch details delete successfully!"})

#                 else:
#                     return jsonify({'error': "Branch details delete not successfully. Please try again!"})

#     return jsonify({'redirect': url_for('index')})

# # For mobile app
# # Route for get all branches


# @branches.route('/all', methods=['GET', 'POST'])
# def get_all_branches():

#     details = bq.get_all_branches()
#     return jsonify(details)


# # Route for get branches
# @branches.route('/all/<id>', methods=['GET', 'POST'])
# def get_all_branches_by_department(id):

#     details = bq.get_all_branches_by_department(id)
#     return jsonify(details)


# # Route for get branch details by id
# @branches.route('/<id>', methods=['GET', 'POST'])
# def get_branch(id):

#     details = bq.get_branch_all_details_by_id(id)
#     return jsonify(details)
