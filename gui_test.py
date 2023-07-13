import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from show import display_profile,display_appointments

from validations import validate_email,validate_name,validate_dob,validate_contact_num,validate_insurance_number,validate_appointment_date,validate_time

from db_connect import search_login_credentials,search_email_from_healthdata,write_dictionary_to_table,find_person_by_item,find_bookings,update_items

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"
healthdata = {
    "name": None,
    "date_of_birth": None,
    "address": None,
    "contact_no":None,
    "Insurance_provider":None,
    "Insurance_num":None,
    "email": None,
    "pass": None,
    "MRN": None
}
current_appointments = {}


is_login_state = False
is_register_state = False
state_booking = False
password_change_active = False
address_change_active = False
contact_change_active = False

def get_response(msg):
    global  is_login_state,is_register_state,state_booking,password_change_active,address_change_active,contact_change_active
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == "profile":
                return display_profile(personal_info=healthdata)
            elif tag == "login" or is_login_state == True:
                is_login_state = True
                return login(msg)
            elif tag == "register" or is_register_state == True:
                is_register_state = True
                return registration(msg)
            elif tag == "appointment" or state_booking == True:
                state_booking = True
                return do_booking(msg)
            elif tag == "change_password" or password_change_active ==True:
                password_change_active = True
                return password_update(msg)
            elif tag == "change_address" or address_change_active ==True:
                address_change_active = True
                return address_update(msg)
            elif tag == "update_contact_number" or contact_change_active == True:
                contact_change_active  = True
                return contact_update(msg)
            elif tag == "scheduled_appointments":
                return display_appointments(current_appointments=current_appointments)
            elif tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "I do not understand..."

login_pass = []
count = 1
def login(msg):
    global healthdata,is_login_state,count,login_pass,current_appointments
    if count == 1:
        count += 1
        print("here")
        return "Please enter your Email: "
    elif count == 2:
        if validate_email(msg) == True:
            count += 1
            login_pass.append(msg)
            return "Please enter your Password!"
        else:
            return "Invalid email address format. Please enter an email address in the format username@domain.com."
    elif count == 3:
        login_pass.append(msg)
        if search_login_credentials(login_pass[0],login_pass[1]) == True:
            count += 1
            healthdata.update(search_email_from_healthdata(login_pass[0]))
            is_login_state = False
            mrn_num = healthdata["MRN"]
            current_appointments = find_bookings("bookings", "MRN", mrn_num)
            return "Login Successful"
        else:
            count = 2
            login_pass.clear()
            return "Please enter correct Email: "

regisration_details = {
    "name": None,
    "date_of_birth": None,
    "address": None,
    "contact_no": None,
    "Insurance_provider": None,
    "Insurance_num": None,
    "email": None,
    "pass": None,
    "MRN": None
}
count_reg = 1
def registration(msg):
    global healthdata, is_register_state,count_reg,regisration_details
    if count_reg == 1:
        count_reg += 1
        return "May I know your email address for registration, please?"
    elif count_reg == 2:
        print("entered")
        if validate_email(msg) == True:
            count_reg += 1
            regisration_details["email"]=msg
            return "Please enter your Password to register!"
        else:
            return "Invalid email address format. Please enter an email address in the format username@domain.com."
    elif count_reg == 3:
        count_reg += 1
        regisration_details["pass"] = msg
        return "May I know your name, please?"
    elif count_reg == 4:
        if validate_name(msg) == True:
            count_reg += 1
            regisration_details["name"] = msg
            return "Could you please provide your date of birth (dob)?"
        else:
            return "Provide a Valid Name please."
    elif count_reg == 5:
        if validate_dob(msg) == True:
            count_reg += 1
            regisration_details["date_of_birth"] = msg
            return "Can you also provide me with your address?"
        else:
            return "Provide a Valid Date of Birth please."
    elif count_reg == 6:
        count_reg += 1
        regisration_details["address"] = msg
        return "Can you also provide me with your contact number?"
    elif count_reg == 7:
        if validate_contact_num(msg) == True:
            count_reg += 1
            regisration_details["contact_no"] = msg
            return "Do you have health insurance -> yes/no?"
        else:
            return "Provide a Valid contact number please."
    elif count_reg == 8:
        if msg.lower() == "no":
            count_reg = 1
            regisration_details.clear()
            is_register_state = False
            return "Sorry, for further assistance, you need to have insurance."
        else:
            count_reg += 1
            return "Great! Can you also provide me with the name of your Insurance Provider?"
    elif count_reg == 9:
        if validate_name(msg) == True:
            count_reg += 1
            regisration_details["Insurance_provider"] = msg
            return "Can you also provide me with your Insurance Number?"
        else:
            return "Provide a Valid Name for the Insurance Company please."
    elif count_reg == 10:
        if validate_insurance_number(msg) == True:
            count_reg += 1
            regisration_details["Insurance_num"] = msg
            is_register_state = False
            while True:
                Medical_record_num = random.randint(1000, 10000)
                existing_mrn = find_person_by_item("health_data", "MRN", Medical_record_num)
                if existing_mrn is False:
                    regisration_details["MRN"] = Medical_record_num
                    break

            write_dictionary_to_table(regisration_details,"health_data")
            user_email = regisration_details["email"]
            user_password = regisration_details["pass"]
            write_dictionary_to_table({"email": user_email, "pass": user_password}, "username_password")
            healthdata.update((regisration_details))
            regisration_details.clear()
            return "Perfect! I have all the information I need."
        else:
            return "Provide a Valid Insurance number please."


var_dict = {}
count_book = 1
def do_booking(msg):
    global var_dict,count_book,healthdata,state_booking
    if count_book == 1:
        count_book+=1
        mrn_number = healthdata["MRN"]
        var_dict.update({"MRN": mrn_number})
        return "Please enter your preferred date for the appointment"
    elif count_book == 2:
        if validate_appointment_date(msg) == True:
            count_book+=1
            var_dict.update({"appoint_date": msg})
            return "Please enter your preferred time. Our business hours are from 10:00 am to 6:00 pm."
        else:
            return "Invalid appointment date. Please enter a date within 30 days from the current date."
    elif count_book == 3:
        if validate_time(msg) == True:
            count_book += 1
            var_dict.update({"appoint_time": msg})
            return "Please enter the name of the Healthcare Provider."
        else:
            return "Invalid time format. Please enter a time in the format HH:MM (24-hour format)"
    elif count_book == 4:
        if validate_name(msg) == True:
            count_book += 1
            var_dict.update({"provider": msg})
            write_dictionary_to_table(var_dict, "bookings")
            var_dict.pop("MRN")
            current_booking_size = len(current_appointments)+1
            var_dict_new = {}
            for key,value in var_dict.items():
                if key == "appoint_date":
                    var_dict_new.update({"Appointment Date":value})
                elif key == "appoint_time":
                    var_dict_new.update({"Appointment Time": value})
                else:
                    var_dict_new.update({"Healthcare Provider": value})

            current_appointments.update({current_booking_size:var_dict})
            state_booking = False
            return "Appointment Booking Complete."

count_pass_update = 1
def password_update(msg):
    global count_pass_update,healthdata,password_change_active
    if count_pass_update == 1:
        count_pass_update+=1
        return "So you want to change your password, Enter new password."
    elif count_pass_update == 2:
        count_pass_update+=1
        mail_id = healthdata["email"]
        healthdata["pass"] = msg
        update_items("pass",msg,mail_id)
        password_change_active = False
        count_pass_update = 1
        return "Password successfully changed."

count_address_update = 1
def address_update(msg):
    global count_address_update,healthdata,address_change_active
    if count_address_update == 1:
        count_address_update+=1
        return "So you want to change your Address, Enter new Address."
    elif count_address_update == 2:
        count_address_update+=1
        mail_id = healthdata["email"]
        healthdata["address"] = msg
        update_items("address",msg,mail_id)
        address_change_active = False
        count_address_update = 1
        return "Address successfully changed."

count_contact_update = 1
def contact_update(msg):
    global count_contact_update,healthdata,address_change_active
    if count_contact_update == 1:
        count_contact_update+=1
        return "So you want to change your Contact Number, Enter new Contact Number."
    elif count_contact_update == 2:
        if validate_contact_num(msg) == True:
            count_contact_update+=1
            mail_id = healthdata["email"]
            healthdata["contact_no"] = msg
            update_items("contact_no",msg,mail_id)
            address_change_active = False
            count_contact_update = 1
            return "Contact Number successfully changed."
        else:
            return "Provide a Valid Contact Number."

