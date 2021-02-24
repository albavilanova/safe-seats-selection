# -*- coding: utf-8 -*-

"""
Created on February 18, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

import numpy as np
import math

def block_seats(seats_map, seats_occupied, blocking_method, col_corridor):

    """ Block seats according to the blocking method, which can be blocking the middle seats
        ("Middle seats") or the seats next to the occupies ones ("Next to occupied")

        Args:
            seats_map (arr): Array with seats map data
            seats_occupied (arr): Array with coordinates of occupied seats
            blocking_method (str): Blocking method
            col_corridor (int): Position of the corridor

        Returns:
            seats_map (arr): Updated array with seats map data
    """

    # Allocate blocked seats
    if blocking_method == "Next to occupied":

        for i, j in seats_occupied:

            # Define blocked seat at the bottom of occupied seat
            if (j + 1) < seats_map.shape[0]:

                seats_map[j + 1][i] = 3

            # Define blocked seat at the top of occupied seat
            if (j - 1) >= 0:

                seats_map[j - 1][i] = 3

            # Define blocked seat to the right of occupied seat
            if ((i + 1) < seats_map.shape[1]) and ((i + 1) != col_corridor):

                seats_map[j][i + 1] = 3

            # Define blocked seat to the left of occupied seat
            if ((i - 1) >= 0) and ((i - 1) != col_corridor):

                seats_map[j][i - 1] = 3

    elif blocking_method == "Middle seat":

        if col_corridor == 3:

            col_middle = [1, 5]

            for i in col_middle:

                seats_map[:, col_middle] = 3
        
        else:

            print("ERROR: There are no middle seats to block.")

    return seats_map

def create_seats_map(columns, rows, col_corridor, seats_occupied, blocking_method):

    """ Create initial seats map (matrix with zeros)

        Args:
            columns (int): number of columns (considering the corridor)
            rows (int): number of rows
            col_corridor (int): Position of the corridor
            seats_occupied (arr): Array with coordinates of occupied seats
            blocking_method (str): Blocking method
            
        Returns:
            seats_map (arr): Updated array with seats map data
    """

    # Initialize with 0
    seats_map = np.zeros(shape = (rows, columns))

    # Allocate corridor
    seats_map[:, col_corridor] = 1

    # Allocate block seats
    seats_map = block_seats(seats_map, seats_occupied, blocking_method, col_corridor)

    # Allocate occupied seats
    for i, j in seats_occupied:
        seats_map[j, i] = 2

    return seats_map

def characterize_seats(seats_map):

    """ Characterize seats within seats map (define seats by type)

        Args:
            seats_map (arr): Array with seats map data
            
        Returns:
            seats_free (arr): Array with coordinates of free seats
            seats_available (arr): Array with coordinates of available seats
    """

    # Define free seats (with blocked)
    a = np.where(np.logical_or(seats_map == 0, seats_map == 3))
    seats_free = np.column_stack((a[1], a[0]))

    # Define available seats (without blocked)
    a = np.where(seats_map == 0)
    seats_available = np.column_stack((a[1], a[0]))

    return seats_free, seats_available

def update_seats_map(seats_map, col_corridor, seats_occupied, blocking_method):

    """ Update seats map considering the blocked seats

        Args:
            seats_map (arr): Array with seats map data
            col_corridor (int): Position of the corridor
            seats_occupied (arr): Array with coordinates of occupied seats
            blocking_method (str): Blocking method
            
        Returns:
            seats_map (arr): Updated array with seats map data
    """

    # Allocate block seats
    seats_map = block_seats(seats_map, seats_occupied, blocking_method, col_corridor)

    # Allocate occupied seats
    for i, j in seats_occupied:
        seats_map[j, i] = 2

    return seats_map

def update_seats(seats_map):

    """ Update occupied, free and available seats.

        Args:
            seats_map (arr): Array with seats map data
            
        Returns:
            seats_occupied (arr): Updated array with coordinates of occupied seats
            seats_available (arr): Updated array with coordinates of available seats
            seats_free (arr): Updated array with coordinates of free seats
    """

    # Update occupied seats
    a = np.where(np.logical_or(seats_map == 2, seats_map == 4))
    seats_occupied = np.column_stack((a[1], a[0]))

    seats_free, seats_available = characterize_seats(seats_map)

    return seats_occupied, seats_available, seats_free