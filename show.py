
def display_profile(personal_info):
    profile_string = ""
    count = 0
    for key, value in personal_info.items():
        if count == 0:
            profile_string += f"{key} : {value}\n"
        else:
            profile_string += f"         {key} : {value}\n"
        count+=1
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

