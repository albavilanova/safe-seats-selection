# -*- coding: utf-8 -*-

"""
Created on February 22, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

import algorithm.optimization as o
import algorithm.transformation as t
import algorithm.design as d
import algorithm.allocation as a
import db.db_functions as dbf
import db.user_details as ud
import plot.visualization as v
import pandas as pd
import numpy as np
import math

# Connect to DB
#db_file = Write path that points to Project\\db\\sqlite\\db\\pythonsqlite.db in your computer
c, conn = dbf.create_connection(db_file)

# Drop tables in DB
#dbf.delete_tables(c)

# Create tables in DB
#dbf.create_tables(c)
#dbf.create_plane(c, conn)

# Read number of columns, rows and position of corridor from DB
columns = c.execute("""SELECT Number_Columns FROM Planes""").fetchone()[0] + 1
rows = c.execute("""SELECT Number_Rows FROM Planes""").fetchone()[0]
col_corridor = math.floor(columns / 2)

# Write equivalences between seat coordinates and references (e.g. A1 = (0,0)) in DB
#data_seating = dbf.create_seats(c, conn, columns, rows)
#df_seating = pd.DataFrame(data_seating)
#df_seating.to_sql('Seating', conn, if_exists='append', index = False)

# Read occupied seats from DB
seats_occupied_ref = [i[0] for i in c.execute("""SELECT Seat FROM Passengers""").fetchall()]
seats_occupied = t.transform_ref_to_xy_in_array(seats_occupied_ref, col_corridor)

# Define blocking method (Options: "Next to occupied" and "Middle seat")
blocking_method = "Next to occupied"

# Create seats map
seats_map = d.create_seats_map(columns, rows, col_corridor, seats_occupied, blocking_method)

# Define available and free seats
seats_free, seats_available = d.characterize_seats(seats_map)

# Print initial occupancy
print("EVALUATION OF INITIAL OCCUPANCY")
occupancy = v.occupancy(seats_free, seats_occupied, seats_available)

stop = False

while not stop:

    # Ask for input data in terminal and create passengers dataframe
    data_passengers, number_of_passengers = ud.input_user_details()
    df_passengers = pd.DataFrame(data_passengers)

    # Do this while there are free seats (green or orange)
    if seats_free.size != 0:

        if df_passengers["Selection_Preference"][0] == "Automatic":
            
            seats_free, seats_occupied, seats_available, seats_map, seat_ref, second_seat_ref = a.automatic_selection(seats_free, seats_occupied, 
            seats_occupied_ref, seats_available, seats_map, col_corridor, number_of_passengers, blocking_method)

        elif df_passengers["Selection_Preference"][0] == "Manual":

            seats_free, seats_occupied, seats_available, seats_map, seat_ref, second_seat_ref = a.manual_selection(seats_free, seats_occupied, 
            seats_occupied_ref, seats_available, seats_map, col_corridor, number_of_passengers, blocking_method)

        # Input (first) seat reference into the passengers dataframe
        df_passengers.iloc[0, 4] = seat_ref

        if number_of_passengers == 2:
            
            #Input second seat reference into the passengers dataframe
            df_passengers.iloc[1, 4] = second_seat_ref

        # Print booking summary
        print("2. BOOKING SUMMARY")
        print(df_passengers)

        # Print current situation
        v.current_situation(seats_free, seats_occupied, seats_available)

        # Print occupancy
        print("4. CURRENT OCCUPANCY")
        occupancy = v.occupancy(seats_free, seats_occupied, seats_available)
        
        # Input passengers dataframe into the DB
        df_passengers.to_sql('Passengers', conn, if_exists='append', index = False)

        # Change the seats status (from False to True) if they are occupied in table Seating
        dbf.change_seat_status(c, conn, seat_ref, second_seat_ref, number_of_passengers)

    # If there are no free seats
    elif seats_free.size == 0:

        print("ERROR: It is not possible to generate more bookings. The plane is full.") 

        break

    # Ask user if they want to generate a new booking
    answer = input("Do you want to create a new booking? True or False: ")

    while answer != "True" and answer != "False":

        print("ERROR: The answer has to be True or False.")
        answer = input("Do you want to create a new booking? True or False: ")

    if answer == "True":

        stop = False

    elif answer == "False":

        stop = True

# Delete passenger from DB by booking reference or passenger ID
# dbf.delete_booking(c, conn)

# Close the connection
# conn.close()

