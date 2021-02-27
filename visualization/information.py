# -*- coding: utf-8 -*-

"""
Created on February 27, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

def current_situation(df_passengers, seats_free, seats_occupied, seats_available, seats_free_1C, seats_occupied_1C, seats_available_1C):

    """ Show booking summary and print current situation (number of total, free, occupied and available seats)

        Args:
            df_passengers (df): Dataframe with passengers data
            seats_free (arr): Array with coordinates of free seats in economy class
            seats_occupied (arr): Array with coordinates of occupied seats in economy class
            seats_available (arr): Array with coordinates of available seats in economy class
            seats_free_1C (arr): Array with coordinates of free seats in first class
            seats_occupied_1C (arr): Array with coordinates of occupied seats in first class
            seats_available_1C (arr): Array with coordinates of available seats in first class
    """

    print("2. BOOKING SUMMARY")
    print(df_passengers)

    print("3. CURRENT SITUATION")

    print("3.1. ECONOMY CLASS")
    print(f"There are {len(seats_free) + len(seats_occupied)} seats.")
    print(f"Number of free seats: {len(seats_free)}.")
    print(f"Number of occupied seats: {len(seats_occupied)}.")
    print(f"Number of available seats: {len(seats_available)}.")

    print("3.2. FIRST CLASS")
    print(f"There are {len(seats_free_1C) + len(seats_occupied_1C)} seats.")
    print(f"Number of free seats: {len(seats_free_1C)}.")
    print(f"Number of occupied seats: {len(seats_occupied_1C)}.")
    print(f"Number of available seats: {len(seats_available_1C)}.")

def occupancy(seats_free, seats_occupied, seats_available, seats_free_1C, seats_occupied_1C, seats_available_1C):

    """ Print current level of occupancy

        Args:
            seats_free (arr): Array with coordinates of free seats in economy class
            seats_occupied (arr): Array with coordinates of occupied seats in economy class
            seats_available (arr): Array with coordinates of available seats in economy class
            seats_free_1C (arr): Array with coordinates of free seats in first class
            seats_occupied_1C (arr): Array with coordinates of occupied seats in first class
            seats_available_1C (arr): Array with coordinates of available seats in first class
    """

    occupancy = (seats_occupied.shape[0] * 100) / (seats_occupied.shape[0] + seats_free.shape[0])
    occupancy_1C = (seats_occupied_1C.shape[0] * 100) / (seats_occupied_1C.shape[0] + seats_free_1C.shape[0])

    print("4. CURRENT OCCUPANCY")
    print(f"The occupancy in economy class is: {occupancy:.2f} %.")
    print(f"The occupancy in first class is: {occupancy_1C:.2f} %.")

    return occupancy, occupancy_1C