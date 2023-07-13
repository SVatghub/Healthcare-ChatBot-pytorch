import random
import json

import torch

from model import NeuralNet

from nltk_utils import bag_of_words, tokenize

from intro import startconv

from booking import do_booking

from show import display_profile,display_appointments

from edit import edit_options

from db_connect import find_bookings

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
# Data values
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

# for getting some vital information
commands = ["Book an Appointment","Show Profile","Show my Schedules Appointments","Ask Questions Related to your Symtoms","Edit Account Details"]
editing_tags = ["change_password","change_address","update_contact_number"]

flag = True
def getresponse(msg):
    intro_greet()
    flag = True
    flag = startconv(healthdata=healthdata, flag=flag)

def intro_greet():
    return "Hi there! You need to Login/Register. \n Type login or register accordingly"

if flag == True:
    mrn_num = healthdata["MRN"]
    current_appointments = find_bookings("bookings","MRN",mrn_num)
    # if current_appointments is None:
    #     current_appointments = {}

    count = 1
    while True:
        # sentence = "do you use credit cards?"
        if count==1:
            print(f"{bot_name}: I can do the following : ")
            for i in range(len(commands)):
                print(f'{i+1}). {commands[i]}')

        count+=1
        sentence = input("You: ")
        if sentence == "quit":
            break

        sentence = tokenize(sentence)
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
                if tag == intent["tag"]:
                    if tag == "appointment":
                        current_booking_size = len(current_appointments)+1
                        new_booking = do_booking(bot_name=bot_name,healthdata=healthdata)
                        current_appointments.update({current_booking_size:new_booking})
                        print(f"{bot_name}: Appointment Booking Complete.")
                    elif tag == "profile":
                        display_profile(personal_info=healthdata)
                    elif tag == "scheduled_appointments":
                        current_appointments = find_bookings("bookings","MRN",mrn_num)
                        display_appointments(current_appointments=current_appointments)
                    elif tag in editing_tags:
                        flag = edit_options(healthdata)
                        if flag == "quit":
                            break
                    else:
                        print(f"{bot_name}: {random.choice(intent['responses'])}")                    
        else:
            print(f"{bot_name}: I do not understand...")