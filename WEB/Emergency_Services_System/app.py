import os
import sys
import random
import hashlib
from datetime import datetime
from flask import Flask, render_template, redirect, jsonify, url_for, request, session

sys.path.append(os.path.abspath('python/'))
sys.path.append(os.path.abspath('python/db'))

sys.path.append(os.path.abspath('routes/'))
sys.path.append(os.path.abspath('routes/_branch'))

import utils
import users_queries as uq
import branches_queries as bq

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

app = Flask(__name__)
app.env = "development"
# app.static_folder = "../static"

# Blueprints
app.register_blueprint(departments)
app.register_blueprint(branches)
app.register_blueprint(branch_user)
app.register_blueprint(users)
app.register_blueprint(branch)

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

    details = bq.get_all_branches()
    return render_template('login.html', details=details)


# Route for index/home page
@app.route('/')
@app.route('/index')
def index():
    if 'adminId' not in session:
        return redirect('/login')

    return render_template('index.html')


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

        if 'adminId' in session:
            return jsonify({'redirect': url_for('index')})

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


# Route for admin user
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


# Main
if __name__ == '__main__':
    localhost = "0.0.0.0"
    port = "5000"
    app.run(host=localhost, port=port, debug=True)
