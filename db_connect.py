import mysql.connector

def establish_con():
    cnx = mysql.connector.connect(
        host="localhost",
        user="your_sql_username",
        password="Your_sql_password",
        database="Your_Database_name"
    )
    return cnx

def write_dictionary_to_table(dictionary, table_name):

    cnx = establish_con()
     # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # Prepare the INSERT query to write the dictionary to the table
    columns = ', '.join(dictionary.keys())
    values = ', '.join(['%s'] * len(dictionary))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

    # Execute the INSERT query with the dictionary values
    cursor.execute(query, tuple(dictionary.values()))

    # Commit the changes to the database
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

def update_items(item_name, value, mail):
    # Create a cursor object to execute SQL queries
    cnx = establish_con()
    cursor = cnx.cursor()

    if item_name == "pass" or item_name == "email":
        # Update health_data table
        query_health_data = f"UPDATE health_data SET {item_name} = %s WHERE email = %s;"
        cursor.execute(query_health_data, (value, mail))

        # Update username_password table
        query_username_password = f"UPDATE username_password SET {item_name} = %s WHERE email = %s;"
        cursor.execute(query_username_password, (value, mail))
    else:
        # Update health_data table only
        query_health_data = f"UPDATE health_data SET {item_name} = %s WHERE email = %s;"
        cursor.execute(query_health_data, (value, mail))

    # Commit the changes to the database
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()


def delete_data_from_table_using_contact_no(table_name,contact_no):
    # Create a cursor object to execute SQL queries
    cnx = establish_con()
    cursor = cnx.cursor()

    # Prepare the DELETE query to remove data from the table based on contact number
    query = f"DELETE FROM {table_name} WHERE contact_no = %s"

    # Execute the DELETE query with the contact number value
    cursor.execute(query, (contact_no,))

    # Commit the changes to the database
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

def find_person_by_item(table_name, item_name, item_value):
    # Create a cursor object to execute SQL queries
    cnx = establish_con()
    cursor = cnx.cursor(dictionary=True) 

    # Execute the SELECT query to retrieve data from the table based on the item_name and item_value
    query = f"SELECT * FROM {table_name} WHERE {item_name} = %s"
    cursor.execute(query, (item_value,))

    # Fetch the row from the result set
    row = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Return true if user found and false if not found
    return row

def search_login_credentials(email, password):
    # Establish a connection to the MySQL database
    email = str(email)
    password = str(password)

    cnx = establish_con()
    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor(dictionary=True)

    # Execute the SELECT query to search for the login credentials
    query = "SELECT * FROM username_password WHERE email = %s AND pass = %s"
    cursor.execute(query, (email, password))

    # Fetch the row from the result set
    row = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return row

def search_email_from_healthdata(email):
    # Establish a connection to the MySQL database
    email = str(email)

    cnx = establish_con()
    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor(dictionary=True)

    # Execute the SELECT query to search for the login credentials
    query = "SELECT * FROM health_data WHERE email = %s"
    cursor.execute(query, (email,))

    # Fetch the row from the result set
    row = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return row

def find_bookings(table_name, item_name, item_value):
    # Create a cursor object to execute SQL queries
    cnx = establish_con()
    cursor = cnx.cursor(dictionary=True)

    # Execute the SELECT query to retrieve bookings based on the MRN number
    query = f"SELECT * FROM {table_name} WHERE {item_name} = %s"
    cursor.execute(query, (item_value,))

    # Initialize the current_appointments dictionary
    current_appointments = {}

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Process each row and add to current_appointments
    count = 1
    for row in rows:
        appointment_info = {
            "Appointment Date": row["appoint_date"],
            "Appointment Time": row["appoint_time"],
            "Healthcare Provider": row["provider"],
        }
        current_appointments[count] = appointment_info
        count+=1

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return current_appointments
