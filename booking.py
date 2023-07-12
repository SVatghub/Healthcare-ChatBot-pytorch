
from validations import validate_appointment_date,validate_time,validate_name

from db_connect import write_dictionary_to_table

def do_booking(bot_name,healthdata):
    var_dict = {}
    mrn_number = healthdata["MRN"]
    var_dict.update({"MRN":mrn_number})

    print(f"{bot_name}: Please enter your preferred date")
    appoint_date  = input('You: ')
    appoint_date = validate_appointment_date(appoint_date)
    var_dict.update({"appoint_date":appoint_date})

    print(f"{bot_name}: Please enter your preferred time. Our business hours are from 10:00 am to 6:00 pm.")
    appoint_time  = input('You: ') 
    appoint_time  = validate_time(appoint_time) 
    var_dict.update({"appoint_time":appoint_time})

    print(f"{bot_name}: Please enter the name of the Healthcare Provider.")
    provider  = input('You: ') 
    provider  = validate_name(provider) 
    var_dict.update({"provider":provider})

    
    write_dictionary_to_table(var_dict,"bookings")

    var_dict.pop("MRN")

    return var_dict