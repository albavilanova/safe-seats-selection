# -*- coding: utf-8 -*-

"""
Created on February 20, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

import algorithm.transformation as t
import sqlite3
from sqlite3 import Error
import re
import pandas as pd
from PyInquirer import prompt
from examples import custom_style_1

def create_connection(db_file):

    """ Create connection to the database

        Args:
            db_file (str): Directory of the database
    """

    conn = None 

    try:

        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

    except Exception as err:

        print(err)

    c = conn.cursor() 

    return c, conn

def create_tables(c):

    """ Create the tables Passengers, Planes and Seatings

        Args:
            c: Cursor
    """

    # Create table for Planes
    c.execute("""CREATE TABLE Planes (
           Plane_ID VARCHAR(10) NOT NULL PRIMARY KEY,
           Number_Corridors int NOT NULL,
           Number_Columns int NOT NULL,
           Number_Rows int NOT NULL,
           Number_Corridors_1C int NOT NULL,
           Number_Columns_1C int NOT NULL,
           Number_Rows_1C int NOT NULL
       )""")

    # Create table for Passengers
    c.execute("""CREATE TABLE Passengers (
           Booking_Reference VARCHAR(30) NOT NULL,
           Passenger_Name text NOT NULL,
           Passenger_ID VARCHAR(10) PRIMARY KEY NOT NULL,
           Selection_Preference text NOT NULL,
           Class text NOT NULL,
           Seat VARCHAR(10) NOT NULL
      )""")

    # Create table for Seating
    c.execute("""CREATE TABLE Seating (
            Plane_ID VARCHAR(10) NOT NULL,
            Class text NOT NULL,
            Seat VARCHAR(10) NOT NULL,
            X int NOT NULL,
            Y int NOT NULL,
            Occupied BOOLEAN NOT NULL,
            CONSTRAINT fk_Planes
                FOREIGN KEY (Plane_ID)
                REFERENCES Planes(Plane_ID)
    )""")

def delete_tables(c):

    """ Drop the tables Passengers, Planes and Seatings

        Args:
            c: Cursor
    """

    c.execute("""DROP TABLE Planes""")
    c.execute("""DROP TABLE Passengers""")
    c.execute("""DROP TABLE Seating""")

def delete_data(c):

    """ Delete all records from the tables Passengers, Planes and Seatings

        Args:
            c: Cursor
    """

    c.execute("""DELETE FROM Planes""")
    c.execute("""DELETE FROM Passengers""")
    c.execute("""DELETE FROM Seating""")

def create_plane(c, conn):

    """ Insert data about the plane in the table Planes

        Args:
            c: Cursor
            conn: Connection
    """

    # Plane structure (A320 - 214 (4R-ABM/N/O) Configuration)
    # In economy: 1 corridor, 6 columns (without considering the corridor) and 20 rows
    # In first class: 1 corridor, 4 columns (without considering the corridor) and 4 rows
    c.execute("""INSERT INTO Planes VALUES ("A320 - 214", "1", "6", "20", "1", "4", "4")""")
    conn.commit()

def create_seats(c, conn, rows, rows_1C, col_corridor, col_corridor_1C):

    """ Insert data about the seating structure (equivalences between 
        seats coordinates (x, y) and reference)

        Args:
            c: Cursor
            conn: Connection
            rows (int): Number of rows
            rows_1C (int): Number of rows in first class
            col_corridor (int): Position of the corridor
            col_corridor_1C (int): Position of the corridor in first class

        Returns:
            data_seating (list): list with seats references and corresponding coordinates for the plane
    """

    col_name = "ABCDEF"
    data_seating = []

    for i in (col_name):

        for j in range (1, rows + 1):

            seat_ref = i + str(j)
            x, y = t.transform_ref_to_xy(seat_ref, col_corridor)
            occupied = False
            plane_ID = "A320 - 214"

            data_seating.append({"Plane_ID": plane_ID, "Class": "Economy", "Seat": seat_ref, "X": x, "Y": y, "Occupied": occupied})

    col_name = "ABCD"

    for i in (col_name):

        for j in range (1, rows_1C + 1):

            seat_ref = i + str(j)
            x, y = t.transform_ref_to_xy(seat_ref, col_corridor_1C)
            occupied = False
            plane_ID = "A320 - 214"

            data_seating.append({"Plane_ID": plane_ID, "Class": "First class", "Seat": seat_ref, "X": x, "Y": y, "Occupied": occupied})

    return data_seating

def change_seat_status(c, conn, seat_ref, second_seat_ref, number_of_passengers, class_type):

    """ Change status from False to True for occupied seats in database

        Args:
            c: Cursor
            conn: Connection
            seat_ref (str): Seat reference for first passenger
            second_seat_ref (str): Seat reference for second passenger
            number_of_passenger (int): Number of passengers per booking
    """

    c.execute("""UPDATE Seating
    SET Occupied = ? 
    WHERE Seat = ? 
    AND Class = ?""", (True, seat_ref, class_type))

    if number_of_passengers == 2:

        c.execute("""UPDATE Seating
        SET Occupied = ? 
        WHERE Seat = ? 
        AND Class = ?""", (True, second_seat_ref, class_type))

    conn.commit()

def delete_booking(c, conn):

    """ Delete booking by passenger ID or booking reference

        Args:
            c: Cursor
            conn: Connection
    """

    print("BOOKING REMOVAL:")

    question = [{
                "type": "rawlist",
                "name": "delete_type", 
                "message": "How do you want to delete the booking?",
                "choices": ["By booking reference", "By passenger ID"]
                }
    ]
    
    answers = prompt(question, style = custom_style_1)
    delete_type = answers["delete_type"]

    if delete_type == "By booking reference":

        booking_reference = input("Enter booking reference: ")
        booking_reference_list = [i[0] for i in c.execute("""SELECT Booking_Reference FROM Passengers""").fetchall()]
    
        while booking_reference not in booking_reference_list:
            
            print("ERROR: The booking reference does not exist.")
            booking_reference = input("Enter booking reference: ")

        query = 'DELETE FROM Passengers WHERE Booking_Reference = "%s"' % booking_reference.strip()
        query_seat_ref = 'SELECT Seat FROM Passengers WHERE Booking_Reference = "%s"' % booking_reference.strip()
        query_class_type = 'SELECT Class FROM Passengers WHERE Booking_Reference = "%s"' % booking_reference.strip()

    elif delete_type == "By passenger ID":

        passenger_ID = input("Enter passenger ID: ")
        passenger_ID_list = [i[0] for i in c.execute("""SELECT Passenger_ID FROM Passengers""").fetchall()]
    
        while passenger_ID not in passenger_ID_list:
            
            print("ERROR: The booking reference does not exist.")
            passenger_ID = input("Enter passenger ID: ")

        query = 'DELETE FROM Passengers WHERE Passenger_ID = "%s"' % passenger_ID.strip()
        query_seat_ref = 'SELECT Seat FROM Passengers WHERE Passenger_ID = "%s"' % passenger_ID.strip()
        query_class_type = 'SELECT Class FROM Passengers WHERE Passenger_ID = "%s"' % passenger_ID.strip()

    # Delete booking
    c.execute(query)
    
    # Change seat status to unoccupied (False)
    seat_ref = c.execute(query_seat_ref).fetchall()
    class_type = c.execute(query_class_type).fetchall()

    c.execute("""UPDATE Seating 
    SET Occupied = ? 
    WHERE Seat = ? 
    AND Class = ?""", (False, seat_ref[0][0], class_type[0][0]))

    if len(seat_ref) == 2:

        c.execute("""UPDATE Seating
        SET Occupied = ? 
        WHERE Seat = ? 
        AND Class = ?""", (False, seat_ref[1][0], class_type[1][0]))

    print("The booking was removed successfully.")

    conn.commit()

def create_passengers(c, conn, seat_ref, second_seat_ref, df_passengers, number_of_passengers):

    """ Update passengers dataframe by adding the seat references and upload to database. Also,
        change status from False to True for the new occupied seats.

        Args:
            c: Cursor
            conn: Connection
            df_passengers (df): Dataframe with passengers data
            seat_ref (str): Seat reference for first passenger
            second_seat_ref (str): Seat reference for second passenger
            number_of_passenger (int): Number of passengers per booking
    """

    # Input (first) seat reference into the passengers dataframe
    df_passengers.iloc[0, 5] = seat_ref

    if number_of_passengers == 2:
        
        #Input second seat reference into the passengers dataframe
        df_passengers.iloc[1, 5] = second_seat_ref

    # Input passengers dataframe into the DB
    df_passengers.to_sql('Passengers', conn, if_exists='append', index = False)

    # Change the seats status (from False to True) if they are occupied in table Seating
    change_seat_status(c, conn, seat_ref, second_seat_ref, number_of_passengers, df_passengers["Class"][0])