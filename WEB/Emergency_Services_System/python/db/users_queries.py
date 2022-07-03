import db_connector as dbConn


# Function for check exist number
def is_exist_number(number):
    conn = dbConn.db_connector()

    query = ''' SELECT count(number) FROM users WHERE number = %s '''
    values = (str(number),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for login
def login(number, psw):
    conn = dbConn.db_connector()

    query = ''' SELECT nic, number FROM users WHERE number = %s AND psw = %s '''
    values = (str(number), str(psw))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for registration
def user_registration(data):
    conn = dbConn.db_connector()

    name = data['name']
    nic = data['nic']
    address = data['address']
    number = data['number']
    psw = data['psw']

    query = ''
    row_count = 0

    query = ''' INSERT INTO users (number, name, nic, address, psw) VALUES (%s, %s, %s, %s, %s) '''
    values = (int(number), str(name), str(nic), str(address), str(psw))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all users
def get_all_users(is_approved):
    conn = dbConn.db_connector()

    query = ''' SELECT number, name, address, number FROM users '''

    values = (str(is_approved),)

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get profile details
def get_account_details(email):
    conn = dbConn.db_connector()

    query = ''' SELECT number, name, address, number FROM users WHERE number = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update user details
def update_user_details(data):
    conn = dbConn.db_connector()

    name = data['name']
    nic = data['nic']
    address = data['address']
    number = data['number']
    psw = data['psw']

    query = ''
    row_count = 0

    query = ''' UPDATE users_details SET name = %s, nic = %s, address = %s WHERE number = %s '''
    values = (str(name), str(nic), str(address), int(number))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for update user psw
def update_user_psw(number, psw):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE users SET psw = %s WHERE number = %s '''
    values = (str(psw), str(number))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for login
def login(email, psw):
    conn = dbConn.db_connector()

    query = ''' SELECT id, email, account_type FROM admin WHERE email = %s AND psw = %s '''
    values = (str(email), str(psw))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for registration
def registration(data):
    conn = dbConn.db_connector()

    email = data['email']
    psw = data['psw']
    account_type = "admin"
    full_name = data['full_name']

    query = ''
    row_count = 0

    query = ''' INSERT INTO admin (email, psw, account_type, full_name) VALUES (%s, %s, %s, %s) '''
    values = (str(email), str(psw), str(account_type), str(full_name))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for check exist email
def is_exist_email(email):
    conn = dbConn.db_connector()

    query = ''' SELECT count(email) FROM admin WHERE email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()
