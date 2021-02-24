# -*- coding: utf-8 -*-

"""
Created on February 6, 2021

@author: 
    Alba Vilanova Cortezón - m20201124
    Fábio Miguel Domingues da Silva - r2016669
    Matheus Lopes do Nascimento - g20200024
"""

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import math

def make_plot(seats_map):

    """ Make plot to show the matrix seats map

        Args:
            seats_map (arr): Array with seats map data
    """

    rows = seats_map.shape[0]
    columns = seats_map.shape[1]
    col_corridor = math.floor(columns / 2)

    x = np.arange(columns)
    y = np.arange(rows)
    y_labels = np.arange(rows) + 1

    if col_corridor == 3:

        x_labels = ["A", "B", "C", "", "D", "E", "F"]

    elif col_corridor == 2:

        x_labels = ["A", "B", "", "C", "D"]

    plt.figure()
    ax = plt.gca()
    
    # Set colors
    cmap = ListedColormap(["green", "white", "red", "orange", "blue"])
    ax.imshow(seats_map , cmap = cmap, vmin = 0, vmax = 4)

    # Set major ticks
    ax.set_xticks(x)
    ax.set_yticks(y)

    # Set labels
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)
    ax.xaxis.tick_top()

    # Set minor ticks
    ax.set_xticks(np.arange(-.5, columns, 1), minor=True)
    ax.set_yticks(np.arange(-.5, rows, 1), minor=True)

    # Add white grid to see squares
    ax.grid(which = "minor", color = "white", linestyle = "-", linewidth = 2)

    plt.show()

def occupancy(seats_free, seats_occupied, seats_available):

    """ Print current level of occupancy

        Args:
            seats_free (arr): Array with coordinates of free seats
            seats_occupied (arr): Array with coordinates of occupied seats
            seats_available (arr): Array with coordinates of available seats
    """

    occupancy = (seats_occupied.shape[0] * 100) / (seats_occupied.shape[0] + seats_free.shape[0])
    print(f"The occupancy is: {occupancy:.2f} %.")

    return occupancy

def current_situation(seats_free, seats_occupied, seats_available):

    """ Printu current situation (number of total, free, occupied and available seats)

        Args:
            seats_free (arr): Array with coordinates of free seats
            seats_occupied (arr): Array with coordinates of occupied seats
            seats_available (arr): Array with coordinates of available seats
    """

    print("3. CURRENT SITUATION")
    print(f"There are {len(seats_free) + len(seats_occupied)} seats.")
    print(f"Number of free seats: {len(seats_free)}.")
    print(f"Number of occupied seats: {len(seats_occupied)}.")
    print(f"Number of available seats: {len(seats_available)}.")

