import random

from validations import validate_name, validate_dob,validate_contact_num,validate_insurance_number,validate_email
from db_connect import write_dictionary_to_table,find_person_by_item,search_login_credentials,search_email_from_healthdata
bot_name = "Sam"
def startconv(healthdata,flag):
    login_register_prompt = input("You: ")
    if(login_register_prompt.lower() == "login"):
        row = login(flag=flag)
        if row != False:
            user_mail = row["email"]
            healthdata.update(find_person_by_item("health_data","email",user_mail))
        else:
            return False
    else:
        register(healthdata=healthdata,flag=flag)
    return flag


def register(healthdata,flag):
    # 1) Asking for email address!
    print(f"{bot_name}: May I know your email address, please?")
    user_email = input("You: ")
    flag = endconv(user_email,flag=flag)
    if flag != False:
        # 2) Asking for email address password!
        user_email = validate_email(user_email)
        user_found = search_email_from_healthdata(user_email)
        if user_found is None:
            healthdata["email"] = user_email
            print(f"{bot_name}: Please enter your password:")
            user_password = input("You: ")
            flag = endconv(user_password,flag=flag)
            if flag != False:
                healthdata["pass"] = user_password

                # 3) adding username and password to table named username_password
                write_dictionary_to_table({"email" : user_email,"pass" : user_password},"username_password")

                print(f"{bot_name}: May I know your name, please?")
                user_name = input("You: ")
                user_name = validate_name(user_name)
                flag = endconv(user_name,flag=flag)
                if flag != False:
                    healthdata["name"] = user_name

                    # Asking for date of birth!
                    print(f"{bot_name}: Nice to meet you, {user_name}!")
                    print(f"{bot_name}: Could you please provide your date of birth (dob)?")
                    user_dob = input("You: ")
                    flag = endconv(user_dob,flag=flag)
                    if flag != False:
                        user_dob = validate_dob(user_dob)
                        healthdata["date_of_birth"] = user_dob

                        # Asking for address!
                        print(f"{bot_name}: Can you also provide me with your address?")
                        user_address = input("You: ")
                        flag = endconv(user_address,flag=flag)
                        if flag != False:
                            healthdata["address"] = user_address

                            # Asking for contact number!
                            print(f"{bot_name}: Can you also provide me with your contact number?")
                            user_contact_num = input("You: ")
                            flag = endconv(user_contact_num,flag=flag)
                            if flag != False:
                                user_contact_num = validate_contact_num(user_contact_num)
                                healthdata["contact_no"] = user_contact_num
                                # Asking for insurance details
                                print(f"{bot_name}: Do you have health insurance -> yes/no?")
                                user_bool_input = input("You: ")
                                flag = endconv(user_bool_input,flag=flag)
                                if flag != False:
                                    if user_bool_input.lower() == "yes":
                                        print(f"{bot_name}: Great! Can you also provide me with the name of your Insurance Provider?")
                                        user_insurance_prov = input("You: ")
                                        user_insurance_prov = validate_name(user_insurance_prov)
                                        flag = endconv(user_insurance_prov,flag=flag)
                                        if flag != False:
                                            healthdata["Insurance_provider"] = user_insurance_prov

                                            print(f"{bot_name}: Can you also provide me with your Insurance Number?")
                                            user_insurance_num = input("You: ")
                                            flag = endconv(user_insurance_num,flag=flag)
                                            if flag != False:
                                                user_insurance_num = validate_insurance_number(user_insurance_num)
                                                healthdata["Insurance_num"] = user_insurance_num
                                    else:
                                        flag = False
                                        print(f"{bot_name}: Sorry, for further assistance, you need to have insurance.")

    if flag == True and user_found is None:
        # to make sure that mrn stays unique
        while True:
            Medical_record_num = random.randint(1000,10000)
            existing_mrn = find_person_by_item("health_data","MRN",Medical_record_num)
            if existing_mrn is None:
                healthdata["MRN"] = Medical_record_num
                break

        write_dictionary_to_table(healthdata,"health_data")
        print(f"{bot_name}: Perfect! I have all the information I need.")
    elif flag==True and user_found is not None:
        print(f"{bot_name}: This Email Already Exists, use another or login.")
        flag = startconv(healthdata=healthdata,flag=flag)
    else:
        print(f"{bot_name}: Thank you! Have a nice day.")
    return flag

def login(flag):
    while True:
        print(f"{bot_name}: Please enter your email address:")
        email = input("You: ")
        flag = endconv(email,flag=flag)
        if flag != False:
            print(f"{bot_name}: Please enter your password:")
            password = input("You: ")
            flag = endconv(password,flag=flag)
            if flag != False:
                row = search_login_credentials(email=email, password=password)
                if row is not None:
                    print("Login successful!")
                    break
                else:
                    print("Invalid username or password. Please try again.")
        if flag == False:
            return False
    return row

def endconv(input_text,flag):
    exit_text  = "quit"
    if input_text.lower() == exit_text:
        flag = False
    return flag