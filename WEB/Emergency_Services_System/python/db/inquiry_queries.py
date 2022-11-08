import db_connector as dbConn


# # Function for check exist number
# def is_exist_email_in_users(email):
#     conn = dbConn.db_connector()

#     query = ''' SELECT count(email) FROM users WHERE email = %s '''
#     values = (str(email),)

#     cur = conn.cursor()
#     cur.execute(query, values)
#     return cur.fetchall()


# # Function for check exist number
# def is_exist_id_in_users(id):
#     conn = dbConn.db_connector()

#     query = ''' SELECT count(id) FROM users WHERE id = %s '''
#     values = (str(id),)

#     cur = conn.cursor()
#     cur.execute(query, values)
#     return cur.fetchall()


# # Function for registration
# def user_registration(data):
#     conn = dbConn.db_connector()

#     first_name = data['first_name']
#     last_name = data['last_name']
#     email = data['email']
#     nic = data['nic']
#     number = data['number']
#     address = data['address']
#     psw = data['psw']

#     query = ''
#     row_count = 0

#     query = ''' INSERT INTO users (first_name, last_name, email, nic, number, address, psw, profile_pic) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '''
#     values = (str(first_name), str(last_name), str(email),
#               str(nic), str(number), str(address), str(psw), "")
#     cur = conn.cursor()
#     cur.execute(query, values)
#     conn.commit()

#     row_count = cur.rowcount
#     return row_count


# # Function for check exist user by email and psw
# def is_exist_user_by_email_and_psw(email, psw):
#     conn = dbConn.db_connector()

#     query = ''' SELECT id, first_name, last_name, email, profile_pic FROM users WHERE email = %s AND psw = %s '''
#     values = (str(email), str(psw))

#     cur = conn.cursor()
#     cur.execute(query, values)
#     return cur.fetchall()


# # Function for get all users
# def get_all_users():
#     conn = dbConn.db_connector()

#     query = ''' SELECT id, first_name, last_name, email, nic, number, address, profile_pic FROM users '''

#     cur = conn.cursor()
#     cur.execute(query)
#     return cur.fetchall()


# # Function for get profile details
# def get_account_details(id):
#     conn = dbConn.db_connector()

#     query = ''' SELECT id, first_name, last_name, email, nic, number, address, profile_pic FROM users WHERE id = %s '''
#     values = (int(id),)

#     cur = conn.cursor()
#     cur.execute(query, values)
#     return cur.fetchall()


# # Function for update profile details
# def update_user_details(data):
#     conn = dbConn.db_connector()

#     id = data['id']
#     first_name = data['first_name']
#     last_name = data['last_name']
#     email = data['email']
#     nic = data['nic']
#     number = data['number']
#     address = data['address']

#     query = ''
#     row_count = 0

#     query = ''' UPDATE users SET first_name = %s, last_name = %s, nic = %s, number = %s, address = %s WHERE id = %s '''
#     values = (str(first_name), str(last_name),
#               str(nic), str(number), str(address), int(id))
#     cur = conn.cursor()
#     cur.execute(query, values)
#     conn.commit()

#     row_count = cur.rowcount
#     return row_count


# # Function for update user psw
# def update_user_psw(data):
#     conn = dbConn.db_connector()

#     id = data['id']
#     psw = data['psw']

#     query = ''
#     row_count = 0

#     query = ''' UPDATE users SET psw = %s WHERE id = %s '''
#     values = (str(psw), int(id))
#     cur = conn.cursor()
#     cur.execute(query, values)

#     conn.commit()
#     row_count = cur.rowcount

#     return row_count


# # Function for update user profile pic
# def update_profile_picture(user_id, filename):
#     conn = dbConn.db_connector()

#     query = ''
#     row_count = 0

#     query = ''' UPDATE users SET profile_pic = %s WHERE id = %s '''
#     values = (str(filename), int(user_id))
#     cur = conn.cursor()
#     cur.execute(query, values)

#     conn.commit()
#     row_count = cur.rowcount

#     return row_count


# # Function for admin login
# def admin_login(email, psw):
#     conn = dbConn.db_connector()

#     query = ''' SELECT id, email, account_type, full_name FROM admin WHERE email = %s AND psw = %s '''
#     values = (str(email), str(psw))

#     cur = conn.cursor()
#     cur.execute(query, values)
#     return cur.fetchall()


# # Function for registration
# def registration(data):
#     conn = dbConn.db_connector()

#     email = data['email']
#     psw = data['psw']
#     account_type = "admin"
#     full_name = data['full_name']

#     query = ''
#     row_count = 0

#     query = ''' INSERT INTO admin (email, psw, account_type, full_name) VALUES (%s, %s, %s, %s) '''
#     values = (str(email), str(psw), str(account_type), str(full_name))
#     cur = conn.cursor()
#     cur.execute(query, values)
#     conn.commit()

#     row_count = cur.rowcount
#     return row_count


# # Function for check exist email
# def is_exist_email(email):
#     conn = dbConn.db_connector()

#     query = ''' SELECT count(email) FROM admin WHERE email = %s '''
#     values = (str(email),)

#     cur = conn.cursor()
#     cur.execute(query, values)
#     return cur.fetchall()


# # Function for get all admins
# def get_all_admins():
#     conn = dbConn.db_connector()

#     query = ''' SELECT id, full_name, email FROM admin '''

#     cur = conn.cursor()
#     cur.execute(query)
#     return cur.fetchall()

# Function for get inquires by branch
def get_inquiry_by_id(id):
    conn = dbConn.db_connector()

    query = ''' SELECT auto_id, inquiries.id, details, inquiries.location, contact, user_id, branch, lat, lon, status, date, departments.name, branches.location FROM inquiries
                INNER JOIN branches ON branches.branch_id = inquiries.branch
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE inquiries.id = %s'''

    values = (str(id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get inquires by branch
def get_inquires_by_branch(branch, status):
    conn = dbConn.db_connector()

    query = ''' SELECT auto_id, inquiries.id, details, inquiries.location, contact, user_id, branch, lat, lon, status, date, departments.name, branches.location FROM inquiries
                INNER JOIN branches ON branches.branch_id = inquiries.branch
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE branch = %s AND status = %s'''

    values = (str(branch), str(status))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get inquires
def get_inquires_by_user(id):
    conn = dbConn.db_connector()

    query = ''' SELECT auto_id, inquiries.id, details, inquiries.location, contact, user_id, branch, lat, lon, status, date, departments.name, branches.location, thumbnail FROM inquiries
                INNER JOIN branches ON branches.branch_id = inquiries.branch
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE user_id = %s'''

    values = (str(id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for add inquiry
def add_inquiry_details(id, details, location, contact, user_id, branch, lat, lon, date):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' INSERT INTO inquiries (id, details, location, contact, user_id, branch, lat, lon, status, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '''
    values = (str(id), str(details), str(location), str(contact),
              str(user_id), str(branch), str(lat), str(lon), "pending", str(date))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Save images data
# Function for add inquiry images
def add_inquiry_images(inquiry_id, image_name):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' INSERT INTO inquiry_images (inquiry_id, image_name) VALUES (%s, %s) '''
    values = (str(inquiry_id), str(image_name))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get inquiry images
def get_inquiry_images(inquiry_id):
    conn = dbConn.db_connector()

    query = ''' SELECT ROW_NUMBER() OVER (Order by inquiry_images.id) AS number, inquiry_images.id, inquiry_id, image_name FROM inquiry_images
                INNER JOIN predictions ON predictions.image_id = inquiry_images.image_name WHERE inquiry_id = %s'''

    values = (str(inquiry_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Save video data
# Function for add inquiry video
def add_inquiry_video(inquiry_id, video_link):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' INSERT INTO inquiry_video (inquiry_id, video_link) VALUES (%s, %s) '''
    values = (str(inquiry_id), str(video_link))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get inquiry video
def get_inquiry_video(inquiry_id):
    conn = dbConn.db_connector()

    query = ''' SELECT ROW_NUMBER() OVER (Order by inquiry_video.id) AS number, id, inquiry_id, video_link FROM inquiry_video WHERE inquiry_id = %s'''

    values = (str(inquiry_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update branch
def update_inquiry_branch(id, branch):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE inquiries SET branch = %s WHERE id = %s '''
    values = (str(branch), str(id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for update status
def update_inquiry_status(id, status):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE inquiries SET status = %s WHERE id = %s '''
    values = (str(status), str(id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Save images prediction data
# Function for add inquiry images prediction
def add_prediction(image_id, prediction, accuracy):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' INSERT INTO predictions (image_id, prediction, accuracy) VALUES (%s, %s, %s) '''
    values = (str(image_id), str(prediction), str(accuracy))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Save comment data
# Function for add comment
def add_inquiry_comment(inquiry_id, comment):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' INSERT INTO inquiry_comments (inquiry_id, comment) VALUES (%s, %s) '''
    values = (str(inquiry_id), str(comment))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get inquiry comment
def get_inquiry_comment(inquiry_id):
    conn = dbConn.db_connector()

    query = ''' SELECT id, inquiry_id, comment FROM inquiry_comments WHERE inquiry_id = %s'''

    values = (str(inquiry_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Save action data
# Function for add action
def add_inquiry_action(inquiry_id, branch_id, branch_user_id, action, c_date_time):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' INSERT INTO inqury_actions (inquiry_id, branch_id, branch_user_id, action, date_time) VALUES (%s, %s, %s, %s, %s) '''
    values = (str(inquiry_id), str(branch_id),
              str(branch_user_id), str(action), str(c_date_time))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get inquiry action
def get_inquiry_action(inquiry_id):
    conn = dbConn.db_connector()

    query = ''' SELECT inqury_actions.id, inquiry_id, inqury_actions.branch_id, action, departments.name, branches.location, branch_users.name, date_time FROM inqury_actions
                INNER JOIN branches ON branches.branch_id = inqury_actions.branch_id
                INNER JOIN departments ON departments.department_id = branches.department_id
                INNER JOIN branch_users ON branch_users.id = inqury_actions.branch_user_id
                WHERE inquiry_id = %s'''

    values = (str(inquiry_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# # Function for update inquiry action
# def add_inquiry_action(inquiry_id, branch_id, branch_user_id, action):
#     conn = dbConn.db_connector()

#     query = ''
#     row_count = 0

#     query = ''' INSERT INTO inqury_actions (inquiry_id, branch_id, branch_user_id, action) VALUES (%s, %s) '''
#     values = (str(inquiry_id), str(branch_id),
#               str(branch_user_id), str(action))
#     cur = conn.cursor()
#     cur.execute(query, values)
#     conn.commit()

#     row_count = cur.rowcount
#     return row_count
