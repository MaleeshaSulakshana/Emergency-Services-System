import hashlib
import os
import sys
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


# Route for view users
@branch.route('/view-users-details')
def view_users_details():
    if 'branchUserId' not in session:
        return redirect('/login')

    user_id = request.args['id']
    details = uq.get_account_details(user_id)
    return render_template('_branch/view_user_details.html', details=details)


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
