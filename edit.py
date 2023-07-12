
from validations import validate_contact_num
from db_connect import update_items

bot_name = "Sam"
def edit_options(healthdata):
    print(f"{bot_name}: What do you want to Update? (Type 'done' to exit Update Window)")
    response = input("You: ")

    while response != "done" and response != "quit":
        if response.lower() == "password":
            response = edit_pass(healthdata=healthdata)
            if response.lower() != "done" and response.lower() != "quit":
                break
        elif response.lower() == "address":
            response = edit_address(healthdata=healthdata)
            if response.lower() != "done" and response.lower() != "quit":
                break
        elif response.lower() == "contact number":
            response = edit_contact(healthdata=healthdata)
            if response.lower() != "done" and response.lower() != "quit":
                break
        else:
            print(f"{bot_name} Provide Valid Update Item")
    return response

def edit_pass(healthdata):
    mail = healthdata["email"]
    print(f"{bot_name}: Enter your New Password")
    response = input("You: ")
    if response.lower() != "done" and response.lower() != "quit":
        healthdata["pass"] = response
        update_items("pass",response,mail)
        print(f"{bot_name}: Password successfully changed.")
    return response

def edit_address(healthdata):
    mail = healthdata["email"]
    print(f"{bot_name}: Enter your New Address")
    response = input("You: ")
    if response.lower() != "done" and response.lower() != "quit":
        healthdata["address"] = response
        update_items("address",response,mail)
        print(f"{bot_name}: Address successfully Updated.")
    return response

def edit_contact(healthdata):
    mail = healthdata["email"]
    print(f"{bot_name}: Enter your New Contact Number")
    response = input("You: ")
    if response.lower() != "done" and response.lower() != "quit":
        response = validate_contact_num(response)
        healthdata["contact_no"] = response
        update_items("contact_no",response,mail)
        print(f"{bot_name}: Contact Number successfully Updated.")
    return response