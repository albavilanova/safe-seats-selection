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
import visualization.information as i
import visualization.plot as p
import pandas as pd
import numpy as np
import math

# Connect to DB (Recommendation: Install SQLiteStudio)
db_file = "D:\\Arxius\\3_Academic\\9_IMS_Lisboa\\Courses\\Seminar with Python\\Project\\db\\sqlite\\db\\pythonsqlite.db"
c, conn = dbf.create_connection(db_file)

# Drop tables in DB
#dbf.delete_tables(c)

# Create tables and define structure of plane in DB
#dbf.create_tables(c)
#dbf.create_plane(c, conn)

# Define blocking method (Options: "Next to occupied" and "Middle seat")
blocking_method = "Middle seat"

# Read number of columns, rows and position of corridor from DB
columns = c.execute("""SELECT Number_Columns FROM Planes""").fetchone()[0] + 1
rows = c.execute("""SELECT Number_Rows FROM Planes""").fetchone()[0]
col_corridor = math.floor(columns / 2)

# Read number of columns, rows and position of corridor from DB (FIRST CLASS)
columns_1C = c.execute("""SELECT Number_Columns_1C FROM Planes""").fetchone()[0] + 1
rows_1C = c.execute("""SELECT Number_Rows_1C FROM Planes""").fetchone()[0]
col_corridor_1C = math.floor(columns_1C / 2)

# Write equivalences between seat coordinates and references (e.g. A1 = (0,0)) in DB
#data_seating = dbf.create_seats(c, conn, rows, rows_1C, col_corridor, col_corridor_1C)
#df_seating = pd.DataFrame(data_seating)
#df_seating.to_sql('Seating', conn, if_exists='append', index = False)

# Read occupied seats from DB
query = 'SELECT Seat FROM Passengers WHERE Class = "%s"' % "Economy".strip()
seats_occupied_ref = [i[0] for i in c.execute(query).fetchall()]
seats_occupied = t.transform_ref_to_xy_in_array(seats_occupied_ref, col_corridor)

# Read occupied seats from DB (FIRST CLASS)
query = 'SELECT Seat FROM Passengers WHERE Class = "%s"' % "First class".strip()
seats_occupied_ref_1C = [i[0] for i in c.execute(query).fetchall()]
seats_occupied_1C = t.transform_ref_to_xy_in_array(seats_occupied_ref_1C, col_corridor_1C)

# Create seats map
seats_map = d.create_seats_map(columns, rows, col_corridor, seats_occupied, blocking_method)

# Create seats map (FIRST CLASS)
seats_map_1C = d.create_seats_map(columns_1C, rows_1C, col_corridor_1C, seats_occupied_1C, blocking_method)

# Define available and free seats
seats_free, seats_available = d.characterize_seats(seats_map)

# Define available and free seats (FIRST CLASS)
seats_free_1C, seats_available_1C = d.characterize_seats(seats_map_1C)

stop = False

while not stop:

    # Ask for input data in terminal and create passengers dataframe
    data_passengers, number_of_passengers = ud.input_user_details(c)
    df_passengers = pd.DataFrame(data_passengers)

    if df_passengers["Class"][0] == "Economy":
    
        if seats_free.size != 0:

            # See initial seat map
            p.make_plot(seats_map, seats_map_1C)

            if df_passengers["Selection_Preference"][0] == "Automatic":

                seats_free, seats_occupied, seats_available, seats_map, seat_ref, second_seat_ref = a.automatic_selection(seats_free, seats_occupied, 
                seats_occupied_ref, seats_available, seats_map, col_corridor, number_of_passengers, blocking_method)

            elif df_passengers["Selection_Preference"][0] == "Manual":

                seats_free, seats_occupied, seats_available, seats_map, seat_ref, second_seat_ref = a.manual_selection(seats_free, seats_occupied, 
                seats_occupied_ref, seats_available, seats_map, col_corridor, number_of_passengers, blocking_method)

            # Update passengers dataframe and save to DB
            dbf.create_passengers(c, conn, seat_ref, second_seat_ref, df_passengers, number_of_passengers)

            # See final seat map
            p.make_plot(seats_map, seats_map_1C)
            
        elif seats_free.size == 0:

            print("ALERT: It is not possible to book more seats in economy class.") 

            if seats_free_1C.size != 0:

                print("If you are still interested in flying with us, we inform you that there are available seats in first class. Retry again.") 

            break

    elif df_passengers["Class"][0] == "First class":

        if seats_free_1C.size != 0:

            # See initial seat map
            p.make_plot(seats_map, seats_map_1C)

            if df_passengers["Selection_Preference"][0] == "Automatic":
                
                seats_free_1C, seats_occupied_1C, seats_available_1C, seats_map_1C, seat_ref, second_seat_ref = a.automatic_selection(seats_free_1C, 
                seats_occupied_1C, seats_occupied_ref_1C, seats_available_1C, seats_map_1C, col_corridor_1C, number_of_passengers, blocking_method)

            elif df_passengers["Selection_Preference"][0] == "Manual":

                seats_free_1C, seats_occupied_1C, seats_available_1C, seats_map_1C, seat_ref, second_seat_ref = a.manual_selection(seats_free_1C, 
                seats_occupied_1C, seats_occupied_ref_1C, seats_available_1C, seats_map_1C, col_corridor_1C, number_of_passengers, blocking_method)

            # Update passengers dataframe and save to DB
            dbf.create_passengers(c, conn, seat_ref, second_seat_ref, df_passengers, number_of_passengers)

            # See final seat map
            p.make_plot(seats_map, seats_map_1C)

        elif seats_free_1C.size == 0:

            print("ALERT: It is not possible to book more seats in first class.") 

            if seats_free.size != 0:

                print("If you are still interested in flying with us, we inform you that there are available seats in economy class.") 

            break
        
    # Print current situation and level of occupancy
    i.current_situation(df_passengers, seats_free, seats_occupied, seats_available, seats_free_1C, seats_occupied_1C, seats_available_1C)
    i.occupancy(seats_free, seats_occupied, seats_available, seats_free_1C, seats_occupied_1C, seats_available_1C)

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