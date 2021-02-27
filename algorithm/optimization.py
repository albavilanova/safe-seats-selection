# -*- coding: utf-8 -*-

"""
Created on February 10, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

import algorithm.transformation as t
import numpy as np
import random
import math

def furthest_seat_one(seats_occupied, seats_available, col_corridor):

    """ Get the furthest seat from each occupied seat by finding the maximum difference 
        in x and y between each occupied seat and each available seat 

        Args:
            seats_occupied (arr): Array with coordinates of occupied seats
            seats_available (arr): Array with coordinates of available seats
            col_corridor (int): Position of the corridor
    """

    diff = seats_available[None, :] - seats_occupied[:, None]

    for i in range(0, diff.shape[0]):
        
        max_diff_x = diff[i][0][0]
        max_diff_y = diff[i][0][1]

        temp_var = abs(max_diff_x) + abs(max_diff_y)

        for j in range(0, diff.shape[1]):

            sum_x_y = abs(diff[i][j][0]) + abs(diff[i][j][1])
        
            if sum_x_y > temp_var:
                
                max_diff_x = diff[i][j][0]
                max_diff_y = diff[i][j][1]

                temp_var = sum_x_y
    
        diff_x_y = np.array([max_diff_x, max_diff_y])
        seat_occupied_ref = t.transform_xy_to_ref(int(seats_occupied[i][0]), int(seats_occupied[i][1]), col_corridor)
        seat_xy = diff_x_y + seats_occupied[i]
        seat_ref = t.transform_xy_to_ref(int(seat_xy[0]), int(seat_xy[1]), col_corridor)
        #print(f"The furthest available seat from {seat_occupied_ref} is {seat_ref}.")   

def sumabsdiff(array):

    """ Get the sum of the absolute differences among all values in an array. For instance,
        if we have an array such as [1, 5, 7], the result will be coming from:
        |(1 - 5)| + |(1 - 7)| + |(5 - 7)| = 12

        Args:
            array (arr): Any one dimensional array

        Returns:
            int(sum(diffs) / 2): Sum of the absolute distances among all values in the array
    """

    diffs = []

    for i, x in enumerate(array):
      
        for j, y in enumerate(array):
         
            if i != j:
            
                diffs.append(abs(x - y))
   
    return int(sum(diffs) / 2)

def furthest_seat_all(seats_occupied, seats_available, status, number_of_passengers, seats_map, blocking_method):

    """ Get the furthest seat from all occupied seats

        Args:
            seats_occupied (arr): Array with coordinates of occupied seats
            seats_available (arr): Array with coordinates of available seats
            status (int): 
                status = 0 means there are available seats
                status = 1 means there are no more available seats
            number_of_passengers (int): number of passengers per booking
            seats_map (arr): Array with seats map data
            blocking_method (str): Blocking method

        Returns:
            seat (arr): Coordinates of selected (first) seat
    """

    diff = seats_available[None, :] - seats_occupied[:, None]
    mat = np.zeros(shape = (len(seats_available), len(seats_occupied) + 6))
    array = []

    for j in range(0, diff.shape[1]): # 0 to number of available seats
        
        mat[j, 0] = seats_available[j, 0]
        mat[j, 1] = seats_available[j, 1]
        
        for i in range(0, diff.shape[0]): # 0 to number of occupied seats
            
            mat[j, i + 2] = abs(diff[i][j][0]) + abs(diff[i][j][1])
            mat[j, diff.shape[0] + 2] += mat[j, i + 2]
            array = np.append(array, mat[j, i + 2])

        # Calculate sum of the absolute differences among all values in array
        # where these values are the distances from each occupied seat to one available seat
        mat[j, diff.shape[0] + 3] = sumabsdiff(array)

        # Substract sum of the absolute differences from the sum of distances
        mat[j, diff.shape[0] + 4] = mat[j, diff.shape[0] + 2] - mat[j, diff.shape[0] + 3]

        array = []

    mat_sorted = mat[np.argsort(mat[:, diff.shape[0] + 4])]

    seat = [int(mat_sorted[-1, 0]), int(mat_sorted[-1, 1])]

    if blocking_method == "Next to occupied":

        if number_of_passengers == 2:

            if status == 0:
                
                for j in range(0, diff.shape[1]):
                    
                    # False for seats that have no space to one of their sides
                    mat_sorted[j, diff.shape[0] + 5] = False

                    # 313: For columns B, C, D and E
                    if mat_sorted[j, 0] > 0 and mat_sorted[j, 0]  < (seats_map.shape[1] - 1):
                    
                        if (seats_map[int(mat_sorted[j, 1]), int(mat_sorted[j, 0]) - 1] == 0 or 
                            seats_map[int(mat_sorted[j, 1]), int(mat_sorted[j, 0]) + 1] == 0):
                                
                            mat_sorted[j, diff.shape[0] + 5] = True

                    # 313: For column A
                    elif mat_sorted[j, 0] == 0:
                        
                        if seats_map[int(mat_sorted[j, 1]), int(mat_sorted[j, 0]) + 1] == 0:
                            
                            mat_sorted[j, diff.shape[0] + 5] = True

                    # 313: For column F
                    elif mat_sorted[j, 0] == (seats_map.shape[1] - 1):
            
                        if (seats_map[int(mat_sorted[j, 1]), int(mat_sorted[j, 0]) - 1] == 0):

                            mat_sorted[j, diff.shape[0] + 5] = True

                for j in range(-1, -mat_sorted.shape[0], -1):
                    
                    # If the seat has no free seat next to it, go to next
                    if mat_sorted[j, diff.shape[0] + 5] == False:

                        seat = [int(mat_sorted[j - 1, 0]), int(mat_sorted[j - 1, 1])]
                    
                    # If the seat has a free seat next to it, break for loop
                    else:
                        break

            elif status == 1:
                
                for j in range(0, diff.shape[1]):
                    
                    # False for seats that have no space to one of their sides
                    mat_sorted[j, diff.shape[0] + 5] = False

                    # 313: For columns B, C, D and E
                    if mat_sorted[j, 0] > 0 and mat_sorted[j, 0]  < (seats_map.shape[1] - 1):

                        if (seats_map[int(mat_sorted[j, 1]), int(mat_sorted[j, 0]) - 1] == 3 or 
                            seats_map[int(mat_sorted[j, 1]), int(mat_sorted[j, 0]) + 1] == 3):
                            
                            mat_sorted[j, diff.shape[0] + 5] = True

                    # 313: For column A
                    elif mat_sorted[j, 0] == 0:
                        
                        if seats_map[int(mat_sorted[j, 1]), int(mat_sorted[j, 0]) + 1] == 3:
                            
                            mat_sorted[j, diff.shape[0] + 5] = True

                    # 313: For column F
                    elif mat_sorted[j, 0] == (seats_map.shape[1] - 1):
            
                        if (seats_map[int(mat_sorted[j, 1]), int(mat_sorted[j, 0]) - 1] == 3):

                            mat_sorted[j, diff.shape[0] + 5] = True

                for j in range(-1, -mat_sorted.shape[0], -1):
                    
                    # If the seat has no free seat next to it, go to next
                    if mat_sorted[j, diff.shape[0] + 5] == False:

                        seat = [int(mat_sorted[j - 1, 0]), int(mat_sorted[j - 1, 1])]
                    
                    # If the seat has a free seat next to it, break for loop
                    else:
                        break

    return seat

def find_second_seat(seat, seats_map, seats_available, col_corridor):

    """ Find the second seat

        Args:
            seat: Coordinates of selected (first) seat
            seats_map (arr): Array with seats map data
            seats_available (arr): Array with coordinates of available seats

        Returns:
            second_seat (arr): Coordinates of selected second seat
    """

    second_seat = np.array([])

    if col_corridor == 3:
    
        # For all rows, except first and last
        if seat[1] > 0 and seat[1] < (seats_map.shape[0] - 1):

            # 313: For columns A and D
            if seat[0] == 0 or seat[0] == 4: 

                if seats_available.size != 0:

                    if (seats_map[seat[1] - 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1] + 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 2] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])   

                elif seats_available.size == 0:    

                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns B and E
            if seat[0] == 1 or seat[0] == 5: 
                
                if seats_available.size != 0:

                    # Add to the left
                    if (seats_map[seat[1] - 1, seat[0] - 1] != 2 and
                        seats_map[seat[1] + 1, seat[0] - 1] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):

                        second_seat = np.array([seat[0] - 1, seat[1]])
                        
                    # Or add to the right
                    elif (seats_map[seat[1] - 1, seat[0] + 1] != 2 and
                        seats_map[seat[1] + 1, seat[0] + 1] != 2 and
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif seats_available.size == 0:
                    
                    # Add to the left
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])
                        
                    # Or add to the right
                    elif seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313 - For columns C and F
            if seat[0] == 2 or seat[0] == 6: 

                if seats_available.size != 0:
                        
                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1] - 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1], seat[0] - 2] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])
                
                elif seats_available.size == 0:

                    if seats_map[seat[1], seat[0] - 1] == 3:
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])  
            
        # For first row
        elif seat[1] == 0:

            # 313: For columns A and D
            if seat[0] == 0 or seat[0] == 4: 

                if seats_available.size != 0:

                    if (seats_map[seat[1] + 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 2] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif seats_available.size == 0:

                    if seats_map[seat[1], seat[0] + 1] == 3:

                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns B and E
            if seat[0] == 1 or seat[0] == 5: 
                
                if seats_available.size != 0:
                        
                    # Add to the left
                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):

                        second_seat = np.array([seat[0] - 1, seat[1]])

                    # Or add to the right
                    elif (seats_map[seat[1] + 1, seat[0] + 1] != 2 and
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif seats_available.size == 0:
                        
                    # Add to the left
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

                    # Or add to the right
                    elif seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns C and F
            if seat[0] == 2 or seat[0] == 6: 

                if seats_available.size != 0:

                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and  
                        seats_map[seat[1], seat[0] - 2] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])

                elif seats_available.size == 0:
                    
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

        # For last row
        elif seat[1] == (seats_map.shape[0] - 1):

            # 313: For columns A and D
            if seat[0] == 0 or seat[0] == 4: 

                if seats_available.size != 0:

                    if (seats_map[seat[1] - 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 2] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif seats_available.size == 0:

                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns B and E
            if seat[0] == 1 or seat[0] == 5: 

                if seats_available.size != 0:

                    # Add to the left
                    if (seats_map[seat[1] - 1, seat[0] - 1] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):

                        second_seat = np.array([seat[0] - 1, seat[1]])

                    # Or add to the left
                    elif (seats_map[seat[1] - 1, seat[0] + 1] != 2 and
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif seats_available.size == 0:

                    # Add to the left
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

                    # Or add to the left
                    elif seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns C and F
            if seat[0] == 2 or seat[0] == 6: 

                if seats_available.size != 0:

                    if (seats_map[seat[1] - 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1], seat[0] - 2] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])
                
                elif seats_available.size == 0:

                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

    elif col_corridor == 2:

        # For all rows, except first and last
        if seat[1] > 0 and seat[1] < (seats_map.shape[0] - 1):

            # 212: For columns A and C
            if seat[0] == 0 or seat[0] == 3: 

                if seats_available.size != 0:

                    if (seats_map[seat[1] - 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1] + 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])   

                elif seats_available.size == 0:    

                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 212 - For columns B and D
            if seat[0] == 1 or seat[0] == 4: 

                if seats_available.size != 0:
                        
                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1] - 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])
                
                elif seats_available.size == 0:

                    if seats_map[seat[1], seat[0] - 1] == 3:
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])  
            
        # For first row
        elif seat[1] == 0:
            
            # 212: For columns A and C
            if seat[0] == 0 or seat[0] == 3: 
               
                if seats_available.size != 0:
                    
                    if (seats_map[seat[1] + 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif seats_available.size == 0:
                   
                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 212: For columns B and D
            if seat[0] == 1 or seat[0] == 4: 
                
                if seats_available.size != 0:

                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and  
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])

                elif seats_available.size == 0:
                   
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

        # For last row
        elif seat[1] == (seats_map.shape[0] - 1):

            # 212 For columns A and C
            if seat[0] == 0 or seat[0] == 3: 

                if seats_available.size != 0:

                    if (seats_map[seat[1] - 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif seats_available.size == 0:

                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 212: For columns B and D
            if seat[0] == 1 or seat[0] == 4: 

                if seats_available.size != 0:

                    if (seats_map[seat[1] - 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])
                
                elif seats_available.size == 0:

                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

    return second_seat

def find_random_seat_all(seats_map):

    """ Find random seat when there are no seats occupied

        Args:
            seats_map (arr): Array with seats map data

        Returns:
            seat (arr): Coordinates of selected (first) seat
    """

    col_corridor = math.floor(seats_map.shape[1] / 2)

    x = random.choice([*range(0, col_corridor), *range(col_corridor + 1, seats_map.shape[1])])
    y = random.randint(0, seats_map.shape[0] - 1)
    seat = [x, y]

    return seat

def find_random_seat_blocked(seats_free):

    """ Find random seat when there are only blocked and occupied seats

        Args:
            seats_free (arr): Array with coordinates of free seats

        Returns:
            second_seat (arr): Coordinates of selected second seat
    """

    second_seat = seats_free[np.random.choice(len(seats_free), 1)]

    return second_seat[0]