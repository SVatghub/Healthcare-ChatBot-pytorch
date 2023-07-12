import re
from datetime import datetime,timedelta

bot_name = "Sam"
def validate_name(name):
    while not re.match(r"^[A-Za-z ]+[A-Za-z]$", name):
        print(f"{bot_name}: Invalid name format. Please enter a name using alphabetic characters and spaces, with at least one character.")
        name = input("You: ")
    return name

def validate_dob(dob):
    while True:
        try:
            date = datetime.strptime(dob, "%d-%m-%Y")
            if date.year < 1900 or date > datetime.now():
                print(f"{bot_name}: Invalid date of birth. Please enter a valid date.")
                dob = input("You: ")
                continue
            return dob
        except ValueError:
            print(f"{bot_name}: Invalid date of birth format. Please enter a date in the format DD-MM-YYYY.")
            dob = input("You: ")

def validate_contact_num(contact_number):
    flag = False
    while flag == False:
        pattern = r"^\d{10}$"
        if re.match(pattern, contact_number):
            flag = True
        else:
            print(f"{bot_name}:Invalid contact number format. Please enter a 10-digit number without any spaces or special characters.")
            contact_number = input("You: ")
    return contact_number

def validate_insurance_number(insurance_number):
    flag = False
    while flag == False:
        pattern = r"^\d{4}-\d{4}-\d{4}-\d{4}$"
        if re.match(pattern, insurance_number):
            flag = True
        else:
            print(f"{bot_name}:Invalid insurance number format. Please enter a 16-digit number in the format 1234-5678-1234-5678.")
            insurance_number = input("You: ")
    return insurance_number

def validate_appointment_date(date):
    while True:
        try:
            appointment_date = datetime.strptime(date, "%d-%m-%Y")
            if appointment_date < datetime.now() or appointment_date > datetime.now() + timedelta(days=30):
                print(f"{bot_name}: Invalid appointment date. Please enter a date within 30 days from the current date.")
                date = input("You: ")
                continue
            return date
        except ValueError:
            print(f"{bot_name}: Invalid date format. Please enter a date in the format DD-MM-YYYY.")
            date = input("You: ")

def validate_time(time_str):
    while True:
        try:
            time = datetime.strptime(time_str, "%H:%M")
            if time < datetime.strptime("10:00", "%H:%M") or time > datetime.strptime("18:00", "%H:%M"):
                print(f"{bot_name}: Invalid time. Please enter a time between 10:00 and 18:00 hours.")
                time_str = input("You: ")
                continue
            return time_str
        except ValueError:
            print(f"{bot_name}: Invalid time format. Please enter a time in the format HH:MM (24-hour format).")
            time_str = input("You: ")

def validate_email(email):
    while True:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return email
        else:
            print("Invalid email address format. Please enter an email address in the format username@domain.com.")



