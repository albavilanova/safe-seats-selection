# -*- coding: utf-8 -*-

"""
Created on February 20, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

import uuid
from PyInquirer import prompt
from examples import custom_style_1

def input_user_details(c):
    
    """ Input user details and create booking reference

        Args:
            c: Cursor

        Returns:
            data_passengers (list): List with passengers data and booking reference
            number_of_passengers (int): Number of passengers per booking
    """
    
    data_passengers = []

    booking_reference = str(uuid.uuid4())[:8]
    print(f"NEW BOOKING: {booking_reference}")

    questions = [
                {
                    "type": "rawlist",
                    "name": "number_of_passengers", 
                    "message": "Enter total number of passengers:",
                    "choices": ["1", "2"] 
                },
                {
                    "type": "rawlist",
                    "name": "selection_preference", 
                    "message": "Enter selection preference:",
                    "choices": ["Automatic", "Manual"]
                },
                {
                    "type": "rawlist",
                    "name": "class_type", 
                    "message": "Enter class preference:",
                    "choices": ["Economy", "First class"]
                }
    ]

    answers = prompt(questions, style = custom_style_1)
    number_of_passengers = int(answers["number_of_passengers"])
    selection_preference = answers["selection_preference"]
    class_type = answers["class_type"]

    passenger_ID_list = c.execute("""SELECT Passenger_ID FROM Passengers""").fetchall()

    for i in range(number_of_passengers):

        print("New passenger:")

        passenger_name = input("Enter full name: ")

        while not passenger_name:

            print("ERROR: The passenger name is mandatory.")
            passenger_name = input("Enter full name: ")

        passenger_ID = input("Enter ID number: ")

        while not passenger_ID:

            print("ERROR: The passenger ID is mandatory.")
            passenger_ID = input("Enter ID number: ")
        
        while passenger_ID in [i[0] for i in passenger_ID_list]:
            
            print("ERROR: The passenger ID has already been used to book this trip.")
            passenger_ID = input("Enter ID number: ")

        passenger_ID_list.append((passenger_ID,))

        seat = []
        data_passengers.append({"Booking_Reference": booking_reference, "Passenger_Name": passenger_name, "Passenger_ID": passenger_ID, "Selection_Preference": selection_preference, "Class": class_type, "Seat": seat})

    return data_passengers, number_of_passengers