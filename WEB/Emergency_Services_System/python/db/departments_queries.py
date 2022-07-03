import db_connector as dbConn


# Function for departments registration
def departments_registration(data):
    conn = dbConn.db_connector()

    name = data['name']
    emergency_number_1 = data['emergency_number_1']
    emergency_number_2 = data['emergency_number_2']
    web_link = data['web_link']
    address = data['address']
    desc = data['desc']
    department_id = data['department_id']
    thumbnail = data['thumbnail']

    query = ''
    row_count = 0

    query = ''' INSERT INTO departments (department_id, name, emergency_number_1, emergency_number_2, web_link, 
                                    address, description, thumbnail) VALUES 
                                    (%s, %s, %s, %s, %s, %s, %s, %s) '''
    values = (int(department_id), str(name), str(emergency_number_1), str(emergency_number_2), str(web_link),
              str(address), str(desc), str(thumbnail))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all departments
def get_all_departments():
    conn = dbConn.db_connector()

    query = ''' SELECT department_id, name, emergency_number_1, emergency_number_2, web_link, 
                                    address, description, thumbnail FROM departments'''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get department details
def get_departments_account_details(department_id):
    conn = dbConn.db_connector()

    query = ''' SELECT department_id, name, emergency_number_1, emergency_number_2, web_link, 
                                    address, description, thumbnail WHERE campaign_id = %s '''
    values = (int(department_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()
