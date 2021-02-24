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
            db_file (str): directory of the database
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
            c: cursor
    """

    # Create table for Passengers
    c.execute("""CREATE TABLE Passengers (
           Booking_Reference VARCHAR(30),
           Passenger_Name text NOT NULL,
           Passenger_ID VARCHAR(10) PRIMARY KEY NOT NULL,
           Selection_Preference text,
           Seat VARCHAR(10),
           CONSTRAINT fk_Seating
               FOREIGN KEY (Seat)
               REFERENCES Seating(Seat)
      )""")

    # Create table for Planes
    c.execute("""CREATE TABLE Planes (
           Plane_ID VARCHAR(10) PRIMARY KEY,
           Number_Corridors int,
           Number_Columns int,
           Number_Rows int
       )""")

    # Create table for Seating
    c.execute("""CREATE TABLE Seating (
            Plane_ID VARCHAR(10),
            Seat VARCHAR(10) PRIMARY KEY,
            X int,
            Y int,
            Occupied BOOLEAN,
            CONSTRAINT fk_Planes
                FOREIGN KEY (Plane_ID)
                REFERENCES Planes(Plane_ID)
    )""")

def delete_tables(c):

    """ Drop the tables Passengers, Planes and Seatings

        Args:
            c: cursor
    """

    c.execute("""DROP TABLE Passengers""")
    c.execute("""DROP TABLE Planes""")
    c.execute("""DROP TABLE Seating""")

def delete_data(c):

    """ Delete all records from the tables Passengers, Planes and Seatings

        Args:
            c: cursor
    """

    c.execute("""DELETE FROM Passengers""")
    c.execute("""DELETE FROM Planes""")
    c.execute("""DELETE FROM Seating""")

def create_plane(c, conn):

    """ Insert data about the plane in the table Planes

        Args:
            c: cursor
            conn: connection
    """

    # Plane structure (1 corridor, 6 columns (without considering the corridor) and 15 rows)
    c.execute("""INSERT INTO Planes VALUES ("AFM2020", "1", "6", "15")""")
    conn.commit()

def create_seats(c, conn, columns, rows):

    """ Insert data about the seating structure (equivalences between 
        seats coordinates (x, y) and reference)

        Args:
            c: cursor
            conn: connection
            columns (int): number of columns (considering the corridor)
            rows (int): number of rows

        Returns:
            data_seating (list): list with seats references and corresponding coordinates for the plane
    """

    col_name = "ABCDEF"
    data_seating = []

    for i in (col_name):

        for j in range (1, rows + 1):

            seat_ref = i + str(j)
            x, y = t.transform_ref_to_xy(seat_ref, 3)
            occupied = False
            plane_ID = "AFM2020"

            data_seating.append({"Plane_ID": plane_ID, "Seat": seat_ref, "X": x, "Y": y, "Occupied": occupied})
    
    return data_seating

def change_seat_status(c, conn, seat_ref, second_seat_ref, number_of_passengers):

    """ Change status from False to True for occupied seats in database

        Args:
            c: cursor
            conn: connection
            seat_ref (str): seat reference for first passenger
            second_seat_ref (str): seat reference for second passenger
            number_of_passenger (int): number of passengers per booking
    """

    c.execute("""UPDATE Seating
    SET Occupied = ? 
    WHERE Seat = ? """,(True, seat_ref))

    if number_of_passengers == 2:

        c.execute("""UPDATE Seating
        SET Occupied = ? 
        WHERE Seat = ? """,(True, second_seat_ref))

    conn.commit()

def delete_booking(c, conn):

    """ Delete booking by passenger ID or booking reference

        Args:
            c: cursor
            conn: connection
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

    elif delete_type == "By passenger ID":

        passenger_ID = input("Enter passenger ID: ")
        passenger_ID_list = [i[0] for i in c.execute("""SELECT Passenger_ID FROM Passengers""").fetchall()]
    
        while passenger_ID not in passenger_ID_list:
            
            print("ERROR: The booking reference does not exist.")
            passenger_ID = input("Enter passenger ID: ")

        query = 'DELETE FROM Passengers WHERE Passenger_ID = "%s"' % passenger_ID.strip()

    print("The booking was removed successfully.")
    c.execute(query)

    conn.commit()