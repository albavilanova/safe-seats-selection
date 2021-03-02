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
import pandas as pd
import random
import math

# Settings
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.options.mode.chained_assignment = None

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
    data_mat = []

    for j in range(0, diff.shape[1]): # 0 to number of available seats
        
        mat[j, 0] = seats_available[j, 0]
        mat[j, 1] = seats_available[j, 1]
        
        for i in range(0, diff.shape[0]): # 0 to number of occupied seats
            
            mat[j, i + 2] = abs(diff[i][j][0]) + abs(diff[i][j][1])
            mat[j, diff.shape[0] + 2] += mat[j, i + 2]
            array = np.append(array, mat[j, i + 2])

        # Calculate standard deviation
        mat[j, diff.shape[0] + 3] = np.std(array)

        # Substract standard deviation from the sum of distances
        mat[j, diff.shape[0] + 4] = mat[j, diff.shape[0] + 2] - mat[j, diff.shape[0] + 3]

        # Restart array
        array = []

        data_mat.append({"X": int(mat[j, 0]), "Y": int(mat[j, 1]), "Sum": int(mat[j, diff.shape[0] + 2]), "Std": mat[j, diff.shape[0] + 3]})

    df_mat = pd.DataFrame(data_mat)
    df_mat_sorted = df_mat.sort_values(["Sum", "Std"], ascending = [True, False])
    df_mat_sorted.reset_index(drop=True, inplace=True)
    
    if blocking_method == "Next to occupied":
            
        # Start with False (without space to any of the sides)
        df_mat_sorted["Next"] = False

        if status == 0:

            # Set True if there is an available space (green) next to any of the sides
            for j in range(0, df_mat_sorted.shape[0]):
                
                # 313: For columns B, C, D and E
                if (df_mat_sorted["X"][df_mat_sorted.index[j]] > 0) and (df_mat_sorted["X"][df_mat_sorted.index[j]] < (seats_map.shape[1] - 1)):

                    if (seats_map[df_mat_sorted["Y"][df_mat_sorted.index[j]], df_mat_sorted["X"][df_mat_sorted.index[j]] - 1] == 0 or 
                        seats_map[df_mat_sorted["Y"][df_mat_sorted.index[j]], df_mat_sorted["X"][df_mat_sorted.index[j]] + 1] == 0):

                        df_mat_sorted["Next"][df_mat_sorted.index[j]] = True

                # 313: For column A
                elif df_mat_sorted["X"][df_mat_sorted.index[j]] == 0:
                    
                    if seats_map[df_mat_sorted["Y"][df_mat_sorted.index[j]], df_mat_sorted["X"][df_mat_sorted.index[j]] + 1] == 0:
                        
                        df_mat_sorted["Next"][df_mat_sorted.index[j]] = True

                # 313: For column F
                elif df_mat_sorted["X"][df_mat_sorted.index[j]] == (seats_map.shape[1] - 1):
        
                    if (seats_map[df_mat_sorted["Y"][df_mat_sorted.index[j]], df_mat_sorted["X"][df_mat_sorted.index[j]] - 1] == 0):
                        
                        df_mat_sorted["Next"][df_mat_sorted.index[j]] = True

        elif status == 1:
            
            # Set True if there is a free space (orange) next to any of the sides
            for j in range(0, df_mat_sorted.shape[0]):

                # 313: For columns B, C, D and E
                if df_mat_sorted["X"][df_mat_sorted.index[j]] > 0 and df_mat_sorted["X"][df_mat_sorted.index[j]] < (seats_map.shape[1] - 1):

                    if (seats_map[df_mat_sorted["Y"][df_mat_sorted.index[j]], df_mat_sorted["X"][df_mat_sorted.index[j]] - 1] == 3 or 
                        seats_map[df_mat_sorted["Y"][df_mat_sorted.index[j]], df_mat_sorted["X"][df_mat_sorted.index[j]] + 1] == 3):
                        
                        df_mat_sorted["Next"][df_mat_sorted.index[j]] = True

                # 313: For column A
                elif df_mat_sorted["X"][df_mat_sorted.index[j]] == 0:
                    
                    if seats_map[df_mat_sorted["Y"][df_mat_sorted.index[j]], df_mat_sorted["X"][df_mat_sorted.index[j]] + 1] == 3:
                        
                        df_mat_sorted["Next"][df_mat_sorted.index[j]] = True

                # 313: For column F
                elif df_mat_sorted["X"][df_mat_sorted.index[j]] == (seats_map.shape[1] - 1):
        
                    if (seats_map[df_mat_sorted["Y"][df_mat_sorted.index[j]], df_mat_sorted["X"][df_mat_sorted.index[j]] - 1] == 3):

                        df_mat_sorted["Next"][df_mat_sorted.index[j]] = True
        
    occupancy = seats_occupied.shape[0] * 100 / ((seats_map.shape[1] - 1) * seats_map.shape[0])
    
    if occupancy < 25:

        threshold_value = np.mean(df_mat_sorted["Std"])

    else:
        
        threshold_value = max(df_mat_sorted["Std"])

        df_mat_sorted = df_mat_sorted[df_mat_sorted["Std"] <= threshold_value]
        df_mat_sorted.reset_index(drop=True, inplace=True)
        
    if seats_available.shape[0] == 1:
        
        X = df_mat_sorted["X"][df_mat_sorted.index[0]]
        Y = df_mat_sorted["Y"][df_mat_sorted.index[0]]

    else:

        X = df_mat_sorted["X"][df_mat_sorted.index[-1]]
        Y = df_mat_sorted["Y"][df_mat_sorted.index[-1]]

        if number_of_passengers == 2:

            for j in range(-1, -df_mat_sorted.shape[0], -1):
                
                if df_mat_sorted["Next"][df_mat_sorted.index[j]] == False:
                    
                    X = df_mat_sorted["X"][df_mat_sorted.index[j - 1]]
                    Y = df_mat_sorted["Y"][df_mat_sorted.index[j - 1]]
                    
                else:

                    break

    seat = [X, Y]

    return seat

def find_second_seat(seat, seats_map, seats_available, col_corridor, status):

    """ Find the second seat

        Args:
            seat: Coordinates of selected (first) seat
            seats_map (arr): Array with seats map data
            seats_available (arr): Array with coordinates of available seats
            status (int):
                status = 0 means there are available seats
                status = 1 means there are no more available seats

        Returns:
            second_seat (arr): Coordinates of selected second seat
    """

    second_seat = np.array([])
  
    if col_corridor == 3:
    
        # For all rows, except first and last
        if seat[1] > 0 and seat[1] < (seats_map.shape[0] - 1):

            # 313: For columns A and D
            if seat[0] == 0 or seat[0] == 4: 

                if status == 0:

                    if (seats_map[seat[1] - 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1] + 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 2] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])   

                elif status == 1:    

                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns B and E
            elif seat[0] == 1 or seat[0] == 5: 
                
                if status == 0:

                    if (seats_map[seat[1] - 1, seat[0] - 1] != 2 and
                        seats_map[seat[1] + 1, seat[0] - 1] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0 and 
                        seats_map[seat[1] - 1, seat[0] + 1] != 2 and
                        seats_map[seat[1] + 1, seat[0] + 1] != 2 and
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        if seat[0] == 1:

                            second_seat = np.array([seat[0] - 1, seat[1]])

                        elif seat[0] == 5:
                            
                            second_seat = np.array([seat[0] + 1, seat[1]])

                    # Add to the left
                    elif (seats_map[seat[1] - 1, seat[0] - 1] != 2 and
                        seats_map[seat[1] + 1, seat[0] - 1] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):

                        second_seat = np.array([seat[0] - 1, seat[1]])
                        
                    # Or add to the right
                    elif (seats_map[seat[1] - 1, seat[0] + 1] != 2 and
                        seats_map[seat[1] + 1, seat[0] + 1] != 2 and
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif status == 1:
                    
                    # Add to the left
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])
                        
                    # Or add to the right
                    elif seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313 - For columns C and F
            elif seat[0] == 2 or seat[0] == 6: 

                if status == 0:
                    
                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1] - 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1], seat[0] - 2] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])
                
                elif status == 1:
                  
                    if seats_map[seat[1], seat[0] - 1] == 3:
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])  
            
        # For first row
        elif seat[1] == 0:

            # 313: For columns A and D
            if seat[0] == 0 or seat[0] == 4: 

                if status == 0:

                    if (seats_map[seat[1] + 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 2] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif status == 1:

                    if seats_map[seat[1], seat[0] + 1] == 3:

                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns B and E
            if seat[0] == 1 or seat[0] == 5: 
                
                if status == 0:
                        
                    # Add to the left
                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):

                        second_seat = np.array([seat[0] - 1, seat[1]])

                    # Or add to the right
                    elif (seats_map[seat[1] + 1, seat[0] + 1] != 2 and
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif status == 1:
                    
                    if seats_map[seat[1], seat[0] - 1] == 3 and seats_map[seat[1], seat[0] + 1] == 3:
                        
                        if seat[0] == 1:

                            second_seat = np.array([seat[0] - 1, seat[1]])

                        elif seat[0] == 5:
                            
                            second_seat = np.array([seat[0] + 1, seat[1]])

                    # Add to the left
                    elif seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

                    # Or add to the right
                    elif seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns C and F
            if seat[0] == 2 or seat[0] == 6: 

                if status == 0:

                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and  
                        seats_map[seat[1], seat[0] - 2] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])

                elif status == 1:
                    
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

        # For last row
        elif seat[1] == (seats_map.shape[0] - 1):
            
            # 313: For columns A and D
            if seat[0] == 0 or seat[0] == 4: 

                if status == 0:

                    if (seats_map[seat[1] - 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 2] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif status == 1:

                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns B and E
            if seat[0] == 1 or seat[0] == 5: 

                if status == 0:

                    # Add to the left
                    if (seats_map[seat[1] - 1, seat[0] - 1] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):

                        second_seat = np.array([seat[0] - 1, seat[1]])

                    # Or add to the left
                    elif (seats_map[seat[1] - 1, seat[0] + 1] != 2 and
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif status == 1:
                    
                    if seats_map[seat[1], seat[0] - 1] == 3 and seats_map[seat[1], seat[0] + 1] == 3:
                        
                        if seat[0] == 1:

                            second_seat = np.array([seat[0] - 1, seat[1]])

                        elif seat[0] == 5:

                            second_seat = np.array([seat[0] + 1, seat[1]])

                    # Add to the left
                    elif seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

                    # Or add to the left
                    elif seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 313: For columns C and F
            if seat[0] == 2 or seat[0] == 6: 
                
                if status == 0:

                    if (seats_map[seat[1] - 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1], seat[0] - 2] != 2 and
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])
                
                elif status == 1:
                    
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

    elif col_corridor == 2:

        # For all rows, except first and last
        if seat[1] > 0 and seat[1] < (seats_map.shape[0] - 1):

            # 212: For columns A and C
            if seat[0] == 0 or seat[0] == 3: 

                if status == 0:

                    if (seats_map[seat[1] - 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1] + 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])   

                elif status == 1:    

                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 212 - For columns B and D
            if seat[0] == 1 or seat[0] == 4: 

                if status == 0:
                        
                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1] - 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])
                
                elif status == 1:

                    if seats_map[seat[1], seat[0] - 1] == 3:
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])  
            
        # For first row
        elif seat[1] == 0:
            
            # 212: For columns A and C
            if seat[0] == 0 or seat[0] == 3: 
               
                if status == 0:
                    
                    if (seats_map[seat[1] + 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif status == 1:
                   
                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 212: For columns B and D
            if seat[0] == 1 or seat[0] == 4: 
                
                if status == 0:

                    if (seats_map[seat[1] + 1, seat[0] - 1] != 2 and  
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])

                elif status == 1:
                   
                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

        # For last row
        elif seat[1] == (seats_map.shape[0] - 1):

            # 212 For columns A and C
            if seat[0] == 0 or seat[0] == 3: 

                if status == 0:

                    if (seats_map[seat[1] - 1, seat[0] + 1] != 2 and 
                        seats_map[seat[1], seat[0] + 1] == 0):
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

                elif status == 1:

                    if seats_map[seat[1], seat[0] + 1] == 3:
                        
                        second_seat = np.array([seat[0] + 1, seat[1]])

            # 212: For columns B and D
            if seat[0] == 1 or seat[0] == 4: 

                if status == 0:

                    if (seats_map[seat[1] - 1, seat[0] - 1] != 2 and 
                        seats_map[seat[1], seat[0] - 1] == 0):
                        
                        second_seat = np.array([seat[0] - 1, seat[1]])
                
                elif status == 1:

                    if seats_map[seat[1], seat[0] - 1] == 3:

                        second_seat = np.array([seat[0] - 1, seat[1]])

    return second_seat

def find_random_seat_all(seats_map):

    """ Find random seat when there are no occupied seats

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

    """ Find random seat when there are occupied seats

        Args:
            seats_free (arr): Array with coordinates of free seats

        Returns:
            second_seat (arr): Coordinates of selected second seat
    """

    second_seat = seats_free[np.random.choice(len(seats_free), 1)]

    return second_seat[0]