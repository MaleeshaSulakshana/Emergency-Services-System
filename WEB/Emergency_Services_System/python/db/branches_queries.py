import db_connector as dbConn


# Function for branches registration
def branches_registration(data):
    conn = dbConn.db_connector()

    department = data['department']
    location = data['location']
    emergency_number = data['emergency_number']
    address = data['address']
    branch_id = data['branch_id']
    map_url = data['map_url']

    query = ''
    row_count = 0

    query = ''' INSERT INTO branches (branch_id, department_id, location, emergency_number, address, map_url) VALUES 
                                    (%s, %s, %s, %s, %s, %s) '''
    values = (int(branch_id), str(department), str(
        location), str(emergency_number), str(address), str(map_url))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all branches
def get_all_branches():
    conn = dbConn.db_connector()

    query = ''' SELECT branches.id, branch_id, name, location, branches.emergency_number, branches.address, map_url FROM branches
                INNER JOIN departments ON departments.department_id = branches.department_id'''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get branch details
def get_branch_account_details(branch_id):
    conn = dbConn.db_connector()

    query = ''' SELECT branches.id, branch_id, branches.department_id, name, location, branches.emergency_number, branches.address, map_url FROM branches
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE branch_id = %s '''
    values = (int(branch_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for branch details update
def branch_details_update(data):
    conn = dbConn.db_connector()

    department = data['department']
    location = data['location']
    emergency_number = data['emergency_number']
    address = data['address']
    branch_id = data['branch_id']
    map_url = data['map_url']

    query = ''
    row_count = 0

    query = ''' UPDATE branches SET department_id = %s, location = %s, emergency_number = %s, address = %s, map_url = %s WHERE branch_id = %s '''
    values = (str(department), str(
        location), str(emergency_number), str(address), str(map_url), int(branch_id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


def branch_details_remove(branch_id):
    conn = dbConn.db_connector()

    query = ''' DELETE FROM branches WHERE branch_id = %s '''
    values = (int(branch_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all branches by department
def get_all_branches():
    conn = dbConn.db_connector()

    query = ''' SELECT branches.id, branches.branch_id, departments.name, branches.location, branches.emergency_number, branches.address,
                        departments.emergency_number, departments.web_link, departments.address, departments.description, departments.thumbnail,branches.map_url FROM branches
                INNER JOIN departments ON departments.department_id = branches.department_id '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get all branches by department
def get_all_branches_by_department(department_id):
    conn = dbConn.db_connector()

    query = ''' SELECT branches.id, branches.branch_id, departments.name, branches.location, branches.emergency_number, branches.address,
                        departments.emergency_number, departments.web_link, departments.address, departments.description, departments.thumbnail, branches.map_url FROM branches
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE departments.department_id = %s '''

    values = (str(department_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get branch by department
def get_branch_all_details_by_id(branch_id):
    conn = dbConn.db_connector()

    query = ''' SELECT branches.id, branches.branch_id, departments.name, branches.location, branches.emergency_number, branches.address,
                        departments.emergency_number, departments.web_link, departments.address, departments.description, departments.thumbnail, branches.map_url FROM branches
                INNER JOIN departments ON departments.department_id = branches.department_id WHERE branches.branch_id = %s '''

    values = (str(branch_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for check is available branches
def get_branch_count(department_id):
    conn = dbConn.db_connector()

    query = ''' SELECT COUNT(*) FROM branches WHERE department_id = %s '''
    values = (str(department_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()
