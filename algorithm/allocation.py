# -*- coding: utf-8 -*-

"""
Created on February 15, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

import algorithm.optimization as o
import algorithm.transformation as t
import algorithm.design as d
import numpy as np
import random

def automatic_selection(seats_free, seats_occupied, seats_occupied_ref, seats_available, 
                        seats_map, col_corridor, number_of_passengers, blocking_method):

    """ Does the automatic selection of the seats

        Args:
            seats_free (arr): Array with coordinates of free seats
            seats_occupied (arr): Array with coordinates of occupied seats
            seats_occupied_ref (list): List with references of occupied seats
            seats_available (arr): Array with coordinates of available seats
            seats_map (arr): Array with seats map data
            col_corridor (int): Position of the corridor
            number_of_passengers (int): Number of passengers per booking
            blocking_method (str): Blocking method

        Returns:
            seats_free (arr): Updated array with coordinates of free seats
            seats_occupied (arr): Updated array with coordinates of occupied seats
            seats_available (arr): Updated array with coordinates of available seats
            seats_map (arr): Updated array with seats map data
            seat_ref (str): Reference of selected (first) seat
            second_seat_ref (str): Reference of selected second seat
    """

    # Initialize seats reference
    seat_ref = []
    second_seat_ref = []

    print("1. AUTOMATIC SELECTION")

    # Do this while there are available seats (green)
    if seats_available.size != 0:

        status = 0
        
        # ALLOCATE FIRST PASSENGER (WHEN THERE ARE AVAILABLE SEATS)

        # If there are no occupied seats (all green), find a random seat
        if seats_occupied.size == 0:
            
            seat = o.find_random_seat_all(seats_map)
            print("ALERT: There are no occupied seats.")
            print("The (first) seat will be chosen randomly.")

        else:
            
            # Find the furthest seat from all occupied seats
            seat = o.furthest_seat_all(seats_occupied, seats_available, status, number_of_passengers, seats_map, blocking_method)

        # Get reference from (first) seat
        seat_ref = t.transform_xy_to_ref(int(seat[0]), int(seat[1]), col_corridor)
        print(f"The seat of the (first) passenger is {seat_ref}.")

        # Allocate (first) seat
        seats_map[seat[1], seat[0]] = 4

        # Update seats
        seats_occupied, seats_available, seats_free = d.update_seats(seats_map)
        seats_occupied_ref = np.append(seats_occupied_ref, seat_ref)

        # ALLOCATE SECOND PASSENGER (WHEN THERE ARE AVAILABLE SEATS)

        if number_of_passengers == 2:

            # Try to find second seat next to first seat
            second_seat = o.find_second_seat(seat, seats_map, seats_available, col_corridor, status)

            if second_seat.size == 0:

                # If there are available seats (green), find second seat randomly
                if seats_available.size != 0:

                    print("ALERT: There are no more available seats in pairs.")
                    print("The second seat will be randomly allocated in an available space.")
                    second_seat = o.find_random_seat_blocked(seats_available)

                # If there are no available seats (no green), find second seat randomly
                else:
                    
                    print("ALERT: There are no more available seats.")
                    print("The second seat will be randomly allocated in a blocked space.")
                    second_seat = o.find_random_seat_blocked(seats_free)
                    
            # Get reference from second seat
            second_seat_ref = t.transform_xy_to_ref(int(second_seat[0]), int(second_seat[1]), col_corridor)
            print(f"The seat of the second passenger is {second_seat_ref}.")

            # Allocate second seat
            seats_map[second_seat[1], second_seat[0]] = 4

        # Update seats
        seats_occupied, seats_available, seats_free = d.update_seats(seats_map)
        seats_occupied_ref = np.append(seats_occupied_ref, seat_ref)

    elif seats_available.size == 0:
        
        status = 1

        # ALLOCATE FIRST PASSENGER (WHEN THERE ARE NO AVAILABLE SEATS)

        # Find the furthest seat from all occupied seats
        print("ALERT: There are no more available seats to ensure social distancing. However, the booking will be made.")
        seat = o.furthest_seat_all(seats_occupied, seats_free, status, number_of_passengers, seats_map, blocking_method)
        
        # Get reference from (first) seat
        seat_ref = t.transform_xy_to_ref(seat[0], seat[1], col_corridor)
        print(f"The seat of the (first) passenger is {seat_ref}.")

        # Allocate (first) seat
        seats_map[seat[1], seat[0]] = 4

        # Update seats
        seats_occupied, seats_available, seats_free = d.update_seats(seats_map)
        seats_occupied_ref = np.append(seats_occupied_ref, seat_ref)
        
        # ALLOCATE SECOND PASSENGER (WHEN THERE ARE NO AVAILABLE SEATS)

        if number_of_passengers == 2:

            # If there are no free seats after adding the first seat (all red), remove first seat. 
            if seats_free.size == 0:

                print("ALERT: There are no more free seats. The data of the both passengers will be removed.")
                seats_map[seat[1], seat[0]] = 3

            else:
                
                # Try to find second seat next to first seat
                second_seat = o.find_second_seat(seat, seats_map, seats_free, col_corridor, status)

                if second_seat.size == 0:
                   
                    # If there are free seats (orange), find second seat randomly
                    print("ALERT: There are no more free seats in pairs.")
                    print("The second seat will be randomly allocated in a free space.")
                    second_seat = o.find_random_seat_blocked(seats_free)
                        
                # Get reference from second seat
                second_seat_ref = t.transform_xy_to_ref(int(second_seat[0]), int(second_seat[1]), col_corridor)
                print(f"The seat of the second passenger is {second_seat_ref}.")

                # Allocate second seat
                seats_map[second_seat[1], second_seat[0]] = 4  

            # Update seats
            seats_occupied, seats_available, seats_free = d.update_seats(seats_map)
            seats_occupied_ref = np.append(seats_occupied_ref, seat_ref)     
    
    # Update seats map
    seats_map = d.update_seats_map(seats_map, col_corridor, seats_occupied, blocking_method)
    
    return seats_free, seats_occupied, seats_available, seats_map, seat_ref, second_seat_ref

def manual_selection(seats_free, seats_occupied, seats_occupied_ref, seats_available, 
                     seats_map, col_corridor, number_of_passengers, blocking_method):

    """ Does the manual selection of the seats

        Args:
            seats_free (arr): Array with coordinates of free seats
            seats_occupied (arr): Array with coordinates of occupied seats
            seats_occupied_ref (list): List with references of occupied seats
            seats_available (arr): Array with coordinates of available seats
            seats_map (arr): Array with seats map data
            col_corridor (int): Position of the corridor
            number_of_passengers (int): Number of passengers per booking
            blocking_method (str): Blocking method

        Returns:
            seats_free (arr): Updated array with coordinates of free seats
            seats_occupied (arr): Updated array with coordinates of occupied seats
            seats_available (arr): Updated array with coordinates of available seats
            seats_map (arr): Updated array with seats map data
            seat_ref (str): Reference of selected (first) seat
            second_seat_ref (str): Reference of selected second seat
    """

    # Initialize seats reference
    seat_ref = []
    second_seat_ref = []

    print("1. MANUAL SELECTION")
    
    # Input first seat and throw error if it doesn't exist or it isn't free (it is green or orange)
    seat_ref = input("Enter your seat: ")
    seats_free_ref = t.transform_xy_to_ref_in_array(seats_free, col_corridor)
    
    while seat_ref not in seats_free_ref:
        
        print("ERROR: The seat reference should be a letter, followed by a number, and the seat should be free.")
        print("The free seats are:")
        print(seats_free_ref)
        seat_ref = input("Enter your seat: ")

    # Get coordinates from (first) seat
    x, y = t.transform_ref_to_xy(seat_ref, col_corridor)

    # Allocate (first) seat
    seats_map[y, x] = 4

    # Update seats
    seats_occupied, seats_available, seats_free = d.update_seats(seats_map)
    seats_occupied_ref = np.append(seats_occupied_ref, seat_ref)

    if number_of_passengers == 2:
        
        # Input second seat and throw error if it doesn't exist or it isn't free (it can be green or orange)
        second_seat_ref = input("Enter the second seat: ")

        # Get coordinates from all free seats
        seats_free_ref = t.transform_xy_to_ref_in_array(seats_free, col_corridor)

        while second_seat_ref not in seats_free_ref:
            
            print("ERROR: The seat reference should be a letter, followed by a number, and the seat should be free.")
            print("The free seats are:")
            print(seats_free_ref)
            second_seat_ref = input("Enter the second seat: ")

        # Get coordinates from second seat
        x, y = t.transform_ref_to_xy(second_seat_ref, col_corridor)

        # Allocate second seat
        seats_map[y, x] = 4

        # Update seats
        seats_occupied, seats_available, seats_free = d.update_seats(seats_map)
        seats_occupied_ref = np.append(seats_occupied_ref, second_seat_ref)

    # Update seats map
    seats_map = d.update_seats_map(seats_map, col_corridor, seats_occupied, blocking_method)

    return seats_free, seats_occupied, seats_available, seats_map, seat_ref, second_seat_ref