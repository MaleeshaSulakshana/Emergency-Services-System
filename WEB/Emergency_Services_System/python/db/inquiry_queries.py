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
def get_inquires_by_id(id):
    conn = dbConn.db_connector()

    query = ''' SELECT auto_id, inquiries.id, details, inquiries.location, contact, user_id, branch, lat, lon, status, date, departments.name, branches.location FROM inquiries
                INNER JOIN branches ON branches.id = inquiries.branch
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE inquiries.id = %s'''

    values = (str(id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get inquires by branch
def get_inquires_by_branch(branch):
    conn = dbConn.db_connector()

    query = ''' SELECT auto_id, inquiries.id, details, inquiries.location, contact, user_id, branch, lat, lon, status, date, departments.name, branches.location FROM inquiries
                INNER JOIN branches ON branches.id = inquiries.branch
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE branch = %s'''

    values = (str(branch),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get inquires
def get_inquires_by_user(email):
    conn = dbConn.db_connector()

    query = ''' SELECT auto_id, inquiries.id, details, inquiries.location, contact, user_id, branch, lat, lon, status, date, departments.name, branches.location FROM inquiries
                INNER JOIN branches ON branches.id = inquiries.branch
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE user_id = %s'''

    values = (str(email),)

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
