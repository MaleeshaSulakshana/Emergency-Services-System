import db_connector as dbConn


# Function for branch users registration
def branch_user_registration(data):
    conn = dbConn.db_connector()

    name = data['name']
    branch_id = data['branch_id']
    email = data['email']
    psw = data['psw']

    query = ''
    row_count = 0

    query = ''' INSERT INTO branch_users (name, branch_id, email, psw) VALUES (%s, %s, %s, %s) '''
    values = (str(name), int(branch_id), str(email), str(psw))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all branch users
def get_all_branch_users_by_branch(branch_id):
    conn = dbConn.db_connector()

    query = ''' SELECT branch_users.id, branch_users.name, branch_users.branch_id, branch_users.email FROM branch_users
                INNER JOIN branches ON branches.branch_id = branch_users.branch_id WHERE branch_users.branch_id = %s '''

    values = (int(branch_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get branch details
def get_branch_user_account_details(user_id):
    conn = dbConn.db_connector()

    query = ''' SELECT branch_users.id, branch_users.branch_id, branch_users.name, branch_users.email FROM branch_users
                INNER JOIN branches ON branches.branch_id = branch_users.branch_id WHERE branch_users.id = %s '''
    values = (int(user_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for branch details remove
def branch_user_remove(id):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' DELETE FROM branch_users WHERE id = %s '''
    values = (int(id),)
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count
