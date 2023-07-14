import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from show import display_profile,display_appointments

from validations import validate_email,validate_name,validate_dob,validate_contact_num,validate_insurance_number,validate_appointment_date,validate_time

from db_connect import search_login_credentials,search_email_from_healthdata,write_dictionary_to_table,find_person_by_item,find_bookings,update_items

from probable_diagnoses import diagnose

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
    "gender":None,
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
name_change_active = False
gender_change_active = False
email_change_active = False
insurance_number_change_active = False
insurance_provider_change_active = False
dob_change_active = False
get_probable_diagnosis = False
def get_response(msg):
    global  get_probable_diagnosis,dob_change_active,insurance_provider_change_active,insurance_number_change_active,is_login_state,is_register_state,state_booking,password_change_active,address_change_active,contact_change_active,name_change_active,gender_change_active,email_change_active
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75 or get_probable_diagnosis or dob_change_active or insurance_provider_change_active or insurance_number_change_active or is_login_state or is_register_state or state_booking or password_change_active or address_change_active or contact_change_active or name_change_active or gender_change_active or email_change_active:
        for intent in intents['intents']:
            if (tag == "login" and prob.item()>0.75) or is_login_state == True:
                is_login_state = True
                return login(msg)
            elif (tag == "register" and prob.item()>0.75) or is_register_state == True:
                is_register_state = True
                return registration(msg)
            elif (tag == "appointment" and prob.item()>0.75) or state_booking == True:
                state_booking = True
                return do_booking(msg)
            elif (tag == "change_password" and prob.item()>0.75) or password_change_active ==True:
                password_change_active = True
                return password_update(msg)
            elif (tag == "change_address" and prob.item()>0.75) or address_change_active ==True:
                address_change_active = True
                return address_update(msg)
            elif (tag == "update_contact_number" and prob.item()>0.75) or contact_change_active == True:
                contact_change_active  = True
                return contact_update(msg)
            elif (tag == "update_name" and prob.item()>0.75) or name_change_active == True:
                name_change_active  = True
                return name_update(msg)
            elif (tag == "update_gender" and prob.item()>0.75) or gender_change_active == True:
                gender_change_active  = True
                return gender_update(msg)
            elif (tag == "update_email" and prob.item()>0.75) or email_change_active == True:
                email_change_active = True
                return email_update(msg)
            elif (tag == "update_insurance_num" and prob.item()>0.75) or insurance_number_change_active == True:
                insurance_number_change_active = True
                return insurance_number_update(msg)
            elif (tag == "update_insurance_provider" and prob.item()>0.75) or insurance_provider_change_active == True:
                insurance_provider_change_active  = True
                return insurance_provider_update(msg)
            elif (tag == "update_dob" and prob.item()>0.75) or dob_change_active == True:
                dob_change_active = True
                return dob_update(msg)
            elif (tag == "probable_diagnosis" and prob.item()>0.75) or get_probable_diagnosis == True:
                get_probable_diagnosis = True
                return for_probable_diag(msg)
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
            return "Login Successful.\n         Do you want to update Account Details,\n         If not, can you describe the reason of your visit.\n         You can get a Probable Diagnosis Based on your symptoms."
        else:
            count = 2
            login_pass.clear()
            return "Please enter correct Email: "

registration_details = {
    "name": None,
    "gender":None,
    "date_of_birth": None,
    "address": None,
    "contact_no":None,
    "Insurance_provider":None,
    "Insurance_num":None,
    "email": None,
    "pass": None,
    "MRN": None
}
count_reg = 1
def registration(msg):
    global healthdata, is_register_state,count_reg,registration_details
    if count_reg == 1:
        count_reg += 1
        return "May I know your email address for registration, please?"
    elif count_reg == 2:
        print("entered")
        if validate_email(msg) == True:
            count_reg += 1
            registration_details["email"]=msg
            return "Please enter your Password to register!"
        else:
            return "Invalid email address format. Please enter an email address in the format username@domain.com."
    elif count_reg == 3:
        count_reg += 1
        registration_details["pass"] = msg
        return "May I know your name, please?"
    elif count_reg == 4:
        if validate_name(msg) == True:
            count_reg += 1
            registration_details["name"] = msg
            return "Could you specify your Gender."
        else:
            return "Provide a Valid Name please."
    elif count_reg == 5:
        count_reg += 1
        registration_details["gender"] = msg
        return "Could you please provide your date of birth (dob) \n         in the format Date Month Year?"
    elif count_reg == 6:
        if validate_dob(msg) == True:
            count_reg += 1
            registration_details["date_of_birth"] = msg
            return "Can you also provide me with your address?"
        else:
            return "Provide a Valid Date of Birth please."
    elif count_reg == 7:
        count_reg += 1
        registration_details["address"] = msg
        return "Can you also provide me with your contact number?"
    elif count_reg == 8:
        if validate_contact_num(msg) == True:
            count_reg += 1
            registration_details["contact_no"] = msg
            return "Do you have health insurance -> yes/no?"
        else:
            return "Provide a Valid contact number please."
    elif count_reg == 9:
        if msg.lower() == "no":
            count_reg = 1
            registration_details.clear()
            is_register_state = False
            return "Sorry, for further assistance, you need to have insurance."
        else:
            count_reg += 1
            return "Great! Can you also provide me with the name \n         of your Insurance Provider?"
    elif count_reg == 10:
        if validate_name(msg) == True:
            count_reg += 1
            registration_details["Insurance_provider"] = msg
            return "Can you also provide me with your Insurance Number \n         in the format 1234-1234-1234-1234?"
        else:
            return "Provide a Valid Name for the Insurance Company please."
    elif count_reg == 11:
        if validate_insurance_number(msg) == True:
            count_reg += 1
            registration_details["Insurance_num"] = msg
            is_register_state = False
            while True:
                Medical_record_num = random.randint(1000, 10000)
                existing_mrn = find_person_by_item("health_data", "MRN", Medical_record_num)
                if existing_mrn is False:
                    registration_details["MRN"] = Medical_record_num
                    break

            write_dictionary_to_table(registration_details, "health_data")
            user_email = registration_details["email"]
            user_password = registration_details["pass"]
            write_dictionary_to_table({"email": user_email, "pass": user_password}, "username_password")
            healthdata.update((registration_details))
            registration_details.clear()
            return display_profile(personal_info=healthdata)
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
            return "Please enter your preferred time. Our \n         business hours are from 10:00 am to 6:00 pm. \n         in the format HH:MM (24-hour format)"
        else:
            return "Invalid appointment date. Please enter a \n          within 30 days from the current date."
    elif count_book == 3:
        if validate_time(msg) == True:
            count_book += 1
            var_dict.update({"appoint_time": msg})
            return "Please enter the name of the Healthcare Provider."
        else:
            return "Invalid time format. Please enter a time in the format HH:MM (24-hour format)"
    elif count_book == 4:
        if validate_name(msg) == True:
            count_book = 1
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

            current_appointments.update({current_booking_size:var_dict_new})
            state_booking = False
            return "Appointment Booking Complete."
        else:
            return "Please enter a Valid Healthcare Provider Name"

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
        return "Password successfully changed.\n         Do you want to change something else,\n         If not, can you describe the reason of your visit.\n         You can get a Probable Diagnosis Based on your symptoms."

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
        str1 = "Address successfully changed.\n         "
        str2 = str1 + display_profile(personal_info=healthdata)
        return str2

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
            str1 =  "Contact Number successfully changed.\n         "
            str2 = str1 + display_profile(personal_info=healthdata)
            return str2
        else:
            return "Provide a Valid Contact Number."

count_name_update = 1
def name_update(msg):
    global count_name_update, healthdata, name_change_active
    if count_name_update == 1:
        count_name_update += 1
        return "So you want to change your name. Please enter your new name."
    elif count_name_update == 2:
        if validate_name(msg) == True:
            count_name_update = 1
            name_change_active = False
            healthdata["name"] = msg
            mail_id = healthdata["email"]
            update_items("name", msg, mail_id)
            str1 ="Name successfully changed.\n         "
            str2 = str1 + display_profile(personal_info=healthdata)
            return str2
        else:
            return "Provide a Valid Name."

count_gender_update = 1
def gender_update(msg):
    global count_gender_update, healthdata, gender_change_active

    if count_gender_update == 1:
        count_gender_update += 1
        return "So you want to change your gender. Please enter your new gender."
    elif count_gender_update == 2:
        count_gender_update = 1
        gender_change_active = False
        mail_id = healthdata["email"]
        update_items("gender", msg, mail_id)
        healthdata["gender"] = msg
        str1 = "Gender successfully changed.\n         "
        str2 = str1 + display_profile(personal_info=healthdata)
        return str2

count_email_update = 1
def email_update(msg):
    global count_email_update, healthdata, email_change_active

    if count_email_update == 1:
        count_email_update += 1
        return "So you want to change your email. Please enter your new email."
    elif count_email_update == 2:
        if validate_email(msg)==True:
            count_email_update = 1
            email_change_active = False
            mail_id = healthdata["email"]
            healthdata["email"] = msg
            update_items("email", msg, mail_id)
            str1 = "Email successfully changed.\n         "
            str2 = str1 + display_profile(personal_info=healthdata)
            return str2
        else:
            return "Enter Valid Email."

count_insurance_number_update = 1
def insurance_number_update(msg):
    global count_insurance_number_update, healthdata, insurance_number_change_active

    if count_insurance_number_update == 1:
        count_insurance_number_update += 1
        return "So you want to change your insurance number. Please enter your new insurance number."
    elif count_insurance_number_update == 2:
        if validate_insurance_number(msg):
            count_insurance_number_update = 1
            insurance_number_change_active = False
            mail_id = healthdata["email"]
            healthdata["Insurance_num"] = msg
            update_items("Insurance_num", msg, mail_id)
            str1 ="Insurance number successfully changed.\n         "
            str2 = str1 + display_profile(personal_info=healthdata)
            return str2
        else:
            return "Invalid insurance number format. Please enter a valid 16-digit number in the format 1234-5678-1234-5678."

count_insurance_provider_update = 1
def insurance_provider_update(msg):
    global count_insurance_provider_update, healthdata, insurance_provider_change_active

    if count_insurance_provider_update == 1:
        count_insurance_provider_update += 1
        return "So you want to change your insurance provider name. Please enter the new insurance provider name."
    elif count_insurance_provider_update == 2:
        if validate_name(msg)==True:
            count_insurance_provider_update = 1
            insurance_provider_change_active = False
            mail_id = healthdata["email"]
            healthdata["Insurance_provider"] = msg
            update_items("Insurance_provider", msg, mail_id)
            str1 ="Insurance provider name successfully changed.\n         "
            str2 = str1 + display_profile(personal_info=healthdata)
            return str2
        else:
            return "Provide Valid Insurance Provider Name."

count_dob_update = 1
def dob_update(msg):
    global count_dob_update, healthdata, dob_change_active
    if count_dob_update == 1:
        count_dob_update += 1
        return "So you want to change your date of birth. Please \n         enter your new date of birth in the format Date Month Year."
    elif count_dob_update == 2:
        if validate_dob(msg)==True:
            count_dob_update = 1
            dob_change_active = False
            mail_id = healthdata["email"]
            healthdata["date_of_birth"] = msg
            update_items("date_of_birth", msg, mail_id)
            str1 = "Date of birth successfully changed.\n         "
            str2 = str1 + display_profile(personal_info=healthdata)
            return str2
        else:
            return "Invalid date of birth format. Please enter a date\n          in the format Date Month Year and make sure it is a valid date."

count_probable_diagnosis = 1
def for_probable_diag(msg):
    global count_probable_diagnosis,get_probable_diagnosis
    if count_probable_diagnosis == 1:
        count_probable_diagnosis+=1
        return "Enter your symptoms comma separated to get the probable\n          diagnosis"
    elif count_probable_diagnosis == 2:
        diagnosis_list = diagnose(msg)
        if diagnosis_list == "No matching diseases found, try consulting a professional.\n         Do you want to book an appointment.":
            return diagnosis_list
        else:
            diagnosis_string = '\n'.join(diagnosis_list)
            count_probable_diagnosis = 1
            get_probable_diagnosis = False
            return diagnosis_string
