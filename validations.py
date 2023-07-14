import re
from datetime import datetime,timedelta

bot_name = "Sam"

def validate_name(name):
    if re.match(r"^[A-Za-z ]+[A-Za-z]$", name):
        return True
    else:
        return False


from datetime import datetime, date

from dateutil import parser

def validate_dob(dob):
    try:
        dob_date = parser.parse(dob).date()
        if dob_date.year > 1950 and dob_date < date.today():
            return True
        else:
            return False
    except ValueError:
        return False


def validate_contact_num(contact_number):
    while True:
        pattern = r"^\d{10}$"
        if re.match(pattern, contact_number):
            return True
        else:
            return False

def validate_insurance_number(insurance_number):
    while True:
        pattern = r"^\d{4}-\d{4}-\d{4}-\d{4}$"
        if re.match(pattern, insurance_number):
            return True
        else:
            return False


def validate_appointment_date(date):
    try:
        appointment_date = datetime.strptime(date, "%d %B %Y")
        if appointment_date >= datetime.now() and appointment_date <= datetime.now() + timedelta(days=30):
            return True
        else:
            return False
    except ValueError:
        return False

def validate_time(time_str):
    try:
        time = datetime.strptime(time_str, "%H:%M")
        if time >= datetime.strptime("10:00", "%H:%M") and time <= datetime.strptime("18:00", "%H:%M"):
            return True
        else:
            return False
    except ValueError:
        return False


def validate_email(email):
    while True:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
            return True
        else:
            return False



