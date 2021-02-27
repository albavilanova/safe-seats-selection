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
import matplotlib.gridspec as gridspec
import numpy as np
import math

def make_plot(seats_map, seats_map_1C):

    """ Make plot to show the matrix seats map

        Args:
            seats_map (arr): Array with seats map data in economy class
            seats_map_1C (arr): Array with seats map data in first class
    """

    # Create figure
    fig = plt.figure(constrained_layout = True)

    # Define rows, columns and col_corridor
    rows = seats_map.shape[0]
    columns = seats_map.shape[1]
    col_corridor = math.floor(columns / 2)

    # Define rows, columns and col_corridor (FIRST CLASS)
    rows_1C = seats_map_1C.shape[0]
    columns_1C = seats_map_1C.shape[1]
    col_corridor_1C = math.floor(columns_1C / 2)

    # Define x and y
    x = np.arange(columns)
    y = np.arange(rows)
    y_labels = np.arange(rows) + 1

    if col_corridor == 3:

        x_labels = ["A", "B", "C", "", "D", "E", "F"]

    elif col_corridor == 2:

        x_labels = ["A", "B", "", "C", "D"]

    # Define x and y (FIRST CLASS)
    x_1C = np.arange(columns_1C)
    y_1C = np.arange(rows_1C)
    y_labels_1C = np.arange(rows_1C) + 1

    if col_corridor_1C == 3:

        x_labels_1C = ["A", "B", "C", "", "D", "E", "F"]
        gs = gridspec.GridSpec(2, 1, figure = fig)

    elif col_corridor_1C == 2:

        x_labels_1C = ["A", "B", "", "C", "D"]
        gs = gridspec.GridSpec(2, 1, figure = fig, height_ratios = [1, 3])

    # Set subplots
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    
    # Set colors
    cmap = ListedColormap(["green", "white", "red", "orange", "blue"])
    ax1.imshow(seats_map_1C, cmap = cmap, vmin = 0, vmax = 4)
    ax2.imshow(seats_map, cmap = cmap, vmin = 0, vmax = 4)

    # Set titles
    ax1.title.set_text("First class")
    ax2.title.set_text("Economy class")

    # Set major ticks
    ax1.tick_params(color='grey', which="both")
    ax2.tick_params(color='grey', which="both")
    ax1.set_xticks(x_1C)
    ax1.set_yticks(y_1C)
    ax2.set_xticks(x)
    ax2.set_yticks(y)

    # Set labels
    ax1.set_xticklabels(x_labels_1C, color="grey")
    ax1.set_yticklabels(y_labels_1C, color="grey")
    ax1.xaxis.tick_top()
    ax2.set_xticklabels(x_labels, color="grey")
    ax2.set_yticklabels(y_labels, color="grey")
    ax2.xaxis.tick_top()

    # Set minor ticks
    ax1.set_xticks(np.arange(-.5, columns_1C, 1), minor=True)
    ax1.set_yticks(np.arange(-.5, rows_1C, 1), minor=True)
    ax2.set_xticks(np.arange(-.5, columns, 1), minor=True)
    ax2.set_yticks(np.arange(-.5, rows, 1), minor=True)

    # Add white grid to see squares
    ax1.grid(which = "minor", color = "white", linestyle = "-", linewidth = 2)
    ax2.grid(which = "minor", color = "white", linestyle = "-", linewidth = 2)

    # Change color of spines
    spines_list = ["bottom", "top", "right", "left"]
    
    for i in spines_list:

        ax1.spines[i].set_color("grey")
        ax2.spines[i].set_color("grey")

    plt.show()