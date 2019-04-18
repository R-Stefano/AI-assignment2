import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np


def displayResults(results):
    x=[i for i in range(len(results['BFS']['depths']))]#1,2,3=3x3,4x4,5x5
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
    plt.savefig('result.png')
    plt.show()

    #plt.style.use('seaborn-deep')

    yaxis=[]
    for key in results:
        algo=[]
        for prob in results[key]['isSolved']:
            algo.append(prob.count(True))
        yaxis.append(algo)

    xaxis=[1,2,3]
    #Calculate optimal width
    width = np.min(np.diff(xaxis))/(len(yaxis)+1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(xaxis-width,yaxis[0],width,color='b',label='bfs')
    ax.bar(xaxis,yaxis[1],width,color='c',label='astar')
    ax.bar(xaxis+width,yaxis[2],width,color='g',label='mcts')
    ax.legend(loc=0)
    ax.set_xticks([1,2, 3])
    ax.set_xticklabels(x_ticks)
    plt.savefig('isSolvedBars.png')
    plt.show()
