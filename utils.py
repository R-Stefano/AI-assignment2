import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np


def displayResults(results):
    x=[i for i in range(len(results['BFS']['depths']))]#1,2,3=3x3,4x4,5x5
    print(x)
    colors=['red', 'green', 'blue']
    f, axs = plt.subplots(2, 2, figsize=(15,15))
    #set the titles of subplots
    axs[0,0].set_title('Depth')
    axs[0,1].set_title('Nodes expanded')
    axs[1,0].set_title('Max Depth')
    axs[1,1].set_title('Time')

    #set the x-axis values
    axs[0,0].set_xticks(x)
    axs[0,1].set_xticks(x)
    axs[1,0].set_xticks(x)
    axs[1,1].set_xticks(x)

    #set the x-axis label
    x_ticks=['3x3', '4x4', '5x5']
    axs[0,0].set_xticklabels(x_ticks)
    axs[0,1].set_xticklabels(x_ticks)
    axs[1,0].set_xticklabels(x_ticks)
    axs[1,1].set_xticklabels(x_ticks)

    for key,col in zip(results, colors):
        axs[0,0].plot(x, results[key]['depths'], color=col, label=key)
        axs[0,1].plot(x, results[key]['nodesExpanded'], color=col, label=key)
        axs[1,0].plot(x, results[key]['max_depth'], color=col, label=key)
        axs[1,1].plot(x, results[key]['time'], color=col, label=key)

    #add legend to each subplot
    axs[0,0].legend(loc=0)
    axs[0,1].legend(loc=0)
    axs[1,0].legend(loc=0)
    axs[1,1].legend(loc=0)

    plt.subplots_adjust(hspace=0.4)
    plt.show()
