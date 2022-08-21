import db_connector as dbConn


# Function for departments registration
def departments_registration(data):
    conn = dbConn.db_connector()

    name = data['name']
    emergency_number = data['emergency_number']
    web_link = data['web_link']
    address = data['address']
    desc = data['desc']
    department_id = data['department_id']
    thumbnail = data['thumbnail']

    query = ''
    row_count = 0

    query = ''' INSERT INTO departments (department_id, name, emergency_number, web_link, 
                                    address, description, thumbnail) VALUES 
                                    (%s, %s, %s, %s, %s, %s, %s) '''
    values = (str(department_id), str(name), str(emergency_number), str(web_link),
              str(address), str(desc), str(thumbnail))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for departments update
def departments_update(data):
    conn = dbConn.db_connector()

    name = data['name']
    emergency_number = data['emergency_number']
    web_link = data['web_link']
    address = data['address']
    desc = data['desc']
    department_id = data['department_id']

    query = ''
    row_count = 0

    query = ''' UPDATE departments SET name = %s, emergency_number = %s, web_link = %s, 
                                    address = %s, description = %s WHERE department_id = %s '''
    values = (str(name), str(emergency_number), str(web_link),
              str(address), str(desc), int(department_id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all departments
def get_all_departments():
    conn = dbConn.db_connector()

    query = ''' SELECT department_id, name, emergency_number, web_link, 
                                    address, description, thumbnail FROM departments '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get department details
def get_departments_account_details(department_id):
    conn = dbConn.db_connector()

    query = ''' SELECT department_id, name, emergency_number, web_link, 
                                    address, description, thumbnail FROM departments WHERE department_id = %s '''
    values = (int(department_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()
