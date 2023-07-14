
def display_profile(personal_info):
    profile_string = "Review the Details you have filled : \n         "
    count = 0
    data = {}
    for key,value in personal_info.items():
        if key == "name":
            data["Name"] = value
        elif key == "date_of_birth":
            data["Date of Birth"] = value
        elif key == "gender":
            data["Gender"] = value
        elif key == "contact_no":
            data["Contact Number"] = value
        elif key == "Insurance_provider":
            data["Insurance Provider"] = value
        elif key == "Insurance_num":
            data["Insurance Number"] = value
        elif key == "email":
            data["Email"] = value
        elif key == "address":
            data["Address"] = value
        elif key == "MRN":
            data["MRN"] = value

    for key, value in data.items():
        if count == 0:
            profile_string += f"{key} : {value}\n"
        else:
            profile_string += f"         {key} : {value}\n"
        count+=1
    profile_string += "\n         Specify anything that you would like to change.\n         If not, can you describe the reason of your visit."
    return profile_string


def display_appointments(current_appointments):
    appointments_string = ""
    count = 0
    for key, values in current_appointments.items():
        appointments_string += f"\n{key}:\n"
        for title, value in values.items():
            appointments_string += f"    {title}: {value}\n"
        count += 1

    if len(appointments_string) == 0:
        appointments_string = "You have no appointments scheduled."
    return appointments_string

