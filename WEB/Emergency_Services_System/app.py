import os
import sys
import random
import hashlib
from datetime import datetime
import datetime as dt
from flask import Flask, render_template, redirect, jsonify, url_for, request, session

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

sys.path.append(os.path.abspath('routes/'))
sys.path.append(os.path.abspath('routes/_branch'))

import utils
import users_queries as uq
import branches_queries as bq
import inquiry_queries as iq
import departments_queries as dq
import branch_user_queries as buq

# Import departments route files
from departments import departments

# Import branches route files
from branches import branches

# Import branch users route files
from branch_user import branch_user

# Import users route files
from users import users

# Import branch route files
from branch import branch

# Import inquiries route files
from inquiries import inquiries

app = Flask(__name__)
app.env = "development"
# app.static_folder = "../static"

# Blueprints
app.register_blueprint(departments)
app.register_blueprint(branches)
app.register_blueprint(branch_user)
app.register_blueprint(users)
app.register_blueprint(branch)
app.register_blueprint(inquiries)

app.secret_key = "Emergency_Services_System"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# Create the folder structure
def generate_folder():
    # Get date and time
    date_time = datetime.now()
    date_time = str(date_time.strftime("%d_%m_%Y_%H_%M_%S"))

    # Get random number
    random_no = str(random.randint(100000, 999999))

    # Paths
    folder_name = date_time + "_" + random_no + "/"
    folder_path = os.path.join(APP_ROOT, 'upload_images/')
    input_img = os.path.join(folder_path, folder_name)
    uploaded_img_path = os.path.join(input_img, 'images/')

    # Genarate folders
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    if not os.path.isdir(input_img):
        os.mkdir(input_img)

    if not os.path.isdir(uploaded_img_path):
        os.mkdir(uploaded_img_path)

    return input_img, uploaded_img_path


# Route for login
@app.route('/login')
def login():
    if 'adminId' in session:
        return redirect('/index')

    elif 'branchUserId' in session:
        return redirect('/branch/index')

    details = bq.get_all_branches()
    return render_template('login.html', details=details)


# Route for index/home page
@app.route('/')
@app.route('/index')
def index():
    if 'adminId' not in session:
        return redirect('/login')

    pending_inquires_count = 0
    ongoing_inquires_count = 0
    completed_inquires_count = 0
    users_count = 0
    departments_count = 0
    branches_count = 0
    branch_users_count = 0

    pending_inquires = iq.get_inquires("pending")
    ongoing_inquires = iq.get_inquires("ongoing")
    completed_inquires = iq.get_inquires("completed")
    users = uq.get_all_users()
    departments = dq.get_all_departments()
    branches = bq.get_all_branches()
    branch_users = buq.get_all_branch_users()

    pending_inquires_count = len(pending_inquires)
    ongoing_inquires_count = len(ongoing_inquires)
    completed_inquires_count = len(completed_inquires)
    users_count = len(users)
    departments_count = len(departments)
    branches_count = len(branches)
    branch_users_count = len(branch_users)

    return render_template('index.html', inquires=pending_inquires, users_count=users_count, departments_count=departments_count, branches_count=branches_count,
                           branch_users_count=branch_users_count, pending_inquires_count=pending_inquires_count, ongoing_inquires_count=ongoing_inquires_count,
                           completed_inquires_count=completed_inquires_count)


# Route for view inquiry
@app.route('/view-inquiry-details')
def view_inquiry_details():
    if 'adminId' not in session:
        return redirect('/login')

    id = request.args['id']

    details = iq.get_inquiry_by_id(id)
    images = iq.get_inquiry_images(id)
    videos = iq.get_inquiry_video(id)
    actions = iq.get_inquiry_action(id)
    comments = iq.get_inquiry_comment(id)
    branches = bq.get_all_branches()

    return render_template('view_inquiry_details.html', details=details, images=images, videos=videos, actions=actions, comments=comments, branches=branches)


# Route for get graph data
@app.route('/graph_data')
def graph_data():

    this_week_data = []
    last_week_data = []
    months_data = []

    today = dt.date.today()

    # This week days
    for i in range(0, 7):
        date = today - dt.timedelta(days=i)
        day = date.strftime("%A")

        inquiry_count = iq.get_inquiries_count_by_date(date)[0][0]
        this_week_data.append(
            {"day": f"{day}", "count": str(inquiry_count)})

    # Last week days
    for i in range(7, 14):
        date = today - dt.timedelta(days=i)
        day = date.strftime("%A")

        inquiry_count = iq.get_inquiries_count_by_date(date)[0][0]
        last_week_data.append(
            {"day": f"{day}", "count": str(inquiry_count)})

    # This and Last Months
    current = dt.datetime(today.year, today.month, today.day)
    start = current.replace(day=1)

    for x in range(0, 12):
        end = start - dt.timedelta(days=1)
        start = end.replace(day=1)
        month_year = start.date().strftime("%Y-%m")
        month_number = start.date().strftime("%m")
        month_name = start.date().strftime("%B")

        inquiry_count = iq.get_inquiries_count_by_date(month_year)[0][0]

        months_data.append(
            {"month": f"{month_name}", "count": str(inquiry_count)})

    return jsonify({"weekly": {"this_week": this_week_data, "last_week": last_week_data}, "monthly": months_data})


# Route for add admin
@app.route('/add-admin')
def add_admin():
    if 'adminId' not in session:
        return redirect('/login')

    return render_template('admin/add_admin.html')


# Route for view admins
@app.route('/view-admin')
def view_admin():
    if 'adminId' not in session:
        return redirect('/login')

    admins = uq.get_all_admins()
    return render_template('admin/view_admins.html', admins=admins)


# Route for view admin profile
@app.route('/profile')
def profile():
    if 'adminId' not in session:
        return redirect('/login')

    details = uq.get_admin_details_by_email(session['email'])
    return render_template('profile/profile.html', details=details)


# Route for view admin psw change
@app.route('/psw-change')
def psw_change():
    if 'adminId' not in session:
        return redirect('/login')

    return render_template('profile/change_psw.html')


# Route for sign out
@app.route('/sign-out')
def signout():
    if 'adminId' in session:
        session.pop('adminId', None)
        session.pop('email', None)
        session.pop('name', None)

    return redirect(url_for('index'))


# Route for admin register
@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():

    if request.method == "POST":

        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            name = request.form.get('name')
            email = request.form.get('email')
            psw = request.form.get('psw')

            if (len(name) == 0 or len(email) == 0 or len(psw) == 0):

                return jsonify({'error': "Fields are empty!"})

            elif utils.validate_email(email) == False:
                return jsonify({'error': "Email not valid. Please check your email!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()
                data = {
                    'email': email,
                    'psw': psw,
                    'full_name': name
                }

                # Check email already exist
                is_exist = uq.is_exist_email(email)
                if is_exist[0][0] > 0:
                    return jsonify({'error': "Email already exist!"})

                else:
                    is_created = uq.registration(data)
                    if is_created > 0:
                        return jsonify({'success': "Account has been created!"})

                    else:
                        return jsonify({'error': "Account not created. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for admin login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == "POST":

        if 'adminId' in session:
            return jsonify({'redirect': url_for('index')})

        else:
            email = request.form.get('email')
            psw = request.form.get('psw')
            branch = request.form.get('branch')

            if (len(email) == 0 or len(psw) == 0 or branch == 'none'):
                return jsonify({'error': "Fields are empty!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()

                if branch == 'admin':

                    # Check email already exist
                    details = uq.admin_login(email, psw)
                    if len(details) > 0:
                        session['adminId'] = str(details[0][1])
                        session['email'] = str(details[0][1])
                        session['name'] = str(details[0][3])
                        return jsonify({'redirect': url_for('index')})

                return jsonify({'error': "Sign in failed. Please try again!"})

    return jsonify({'redirect': url_for('sign-in')})


# Route for admin psw change
@app.route('/change_psw', methods=['GET', 'POST'])
def change_psw():

    if request.method == "POST":

        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if (len(psw) == 0 or len(cpsw) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()
                data = {
                    'email': session['adminId'],
                    'psw': psw
                }

                is_updated = uq.update_admin_psw(data)
                if is_updated > 0:
                    return jsonify({'success': "Account password has been updated!"})

                else:
                    return jsonify({'error': "Account password not updated. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for admin profile update
@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():

    if request.method == "POST":

        if 'adminId' not in session:
            return jsonify({'redirect': url_for('login')})

        else:
            name = request.form.get('name')

            if (len(name) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                data = {
                    'email': session['adminId'],
                    'name': name
                }

                is_updated = uq.update_admin_profile(data)
                if is_updated > 0:
                    return jsonify({'success': "Account has been updated!"})

                else:
                    return jsonify({'error': "Account not updated. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Main
if __name__ == '__main__':
    localhost = "0.0.0.0"
    port = "5000"
    app.run(host=localhost, port=port, debug=True)
