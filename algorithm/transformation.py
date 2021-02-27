# -*- coding: utf-8 -*-

"""
Created on February 18, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

import re
import math
import numpy as np

def transform_ref_to_xy(seat_ref, col_corridor):

    """ Transform seat reference into coordinates

        Args:
            seat_ref (arr): Reference of seat
            col_corridor (int): Position of the corridor

        Returns:
            x (int): Coordinate in axis X of the matrix seats map
            y (int): Coordinate in axis Y of the matrix seats map
    """

    r = re.compile("([A-F]+)([0-9]+)")
    m = r.match(seat_ref)
    first_element = m.group(1)
    second_element = int(m.group(2))
    
    if col_corridor == 3:
        
        if first_element == "A" or first_element == "B" or first_element == "C":
            
            x = ord(first_element)%32 - 1
        
        else:

            x = ord(first_element)%32
    
    elif col_corridor == 2:
        
        if first_element == "A" or first_element == "B":

            x = ord(first_element)%32 - 1 
        
        else:

            x = ord(first_element)%32
    
    y = second_element - 1
    
    return x, y

def transform_xy_to_ref(x, y, col_corridor):

    """ Transform seat coordinates into reference

        Args:
            x (int): Coordinate in axis X of the matrix seats map
            y (int): Coordinate in axis Y of the matrix seats map
            col_corridor (int): Position of the corridor

        Returns:
            seat_ref (arr): Reference of seat
    """

    if x == 0:

        first_element = "A"

    elif x < col_corridor and x != 0:

        first_element = chr(ord('@') + (x + 1))
    
    elif x > col_corridor:

        first_element = chr(ord('@') + (x))
    
    second_element = str(y + 1)

    seat_ref = first_element + second_element

    return seat_ref

def transform_ref_to_xy_in_array(seats_ref_arr, col_corridor):

    """ Transform seat reference into coordinates in array

        Args:
            seats_ref_arr (arr): Array with references of seats
            col_corridor (int): Position of the corridor

        Returns:
            seat_ref (arr):  Array with coordinates of seats
    """

    seats_arr = np.array([], int)

    for i in range(0, len(seats_ref_arr)):

        x, y = transform_ref_to_xy(seats_ref_arr[i], col_corridor)
        arr_xy = np.array([x, y])
        seats_arr = np.append(seats_arr, arr_xy)

    seats_arr = seats_arr.reshape([len(seats_ref_arr), 2])

    return seats_arr

def transform_xy_to_ref_in_array(seats_arr, col_corridor):

    """ Transform seat coordinates into reference in array

        Args:
            seats_arr (arr): Array with coordinates of seats
            col_corridor (int): Position of the corridor

        Returns:
            seats_ref_arr (arr):  Array with references of seats
    """

    seats_ref_arr = np.array([], str)

    for i in range(0, len(seats_arr)):

        seat_ref = transform_xy_to_ref(seats_arr[i][0], seats_arr[i][1], col_corridor)
        seats_ref_arr = np.append(seats_ref_arr, seat_ref)

    return seats_ref_arr