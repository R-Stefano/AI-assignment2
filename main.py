from puzzle8 import Puzzle
import BFS as bfs
import AStar as astar
import MCTS as mcts
import utils

import time
import numpy as np
import copy

from random import sample 
num_iter=5

dataStruc={
            'depths':[],
            'nodesExpanded': [],
            'max_depth': [],
            'time':[]
          }
if __name__ == '__main__':    
    board3 = [[1,2,3],
             [4,0,6],
             [7,5,8]]
    
    board4 = [[1,2,3,4],
             [5,6,0,7],
             [8,9,10,11],
             [12,13,14,15]]

    board5 = [[1,2,3,4,5],
              [6,7,8,9,10],
              [11,12,0,13,14],
              [15,16,17,18,19],
              [20,21,22,23,24]]

    boards=[board3, board4, board5]

    inputBoards=[]
    for b in boards:
        board_shuffles=[]
        for i in range(num_iter):
            board_shuffles.append(Puzzle(b).shuffle())
        inputBoards.append(board_shuffles)

    algos={'BFS':bfs, 'AStar':astar, 'MCTS': mcts}
    results={'BFS':copy.deepcopy(dataStruc), 'AStar':copy.deepcopy(dataStruc), 'MCTS':copy.deepcopy(dataStruc)}

    for algo in algos:
        print(algo)
        for i,board in enumerate(boards):
            print('Board: {}x{}'.format(i+3,i+3))
            algo_epoch=copy.deepcopy(dataStruc)
            for j in range(num_iter):
                print('Test:',j)
                print(inputBoards[i][j])
                start = time.time()
                res=algos[algo].search(inputBoards[i][j])
                end= time.time()
                algo_epoch['depths'].append(res.depth)
                algo_epoch['nodesExpanded'].append(res.nodesExpanded)
                algo_epoch['max_depth'].append(res.max_depth)
                algo_epoch['time'].append((end - start))

            results[algo]['depths'].append(np.mean(algo_epoch['depths']))
            results[algo]['nodesExpanded'].append(np.mean(algo_epoch['nodesExpanded']))
            results[algo]['max_depth'].append(np.mean(algo_epoch['max_depth']))
            results[algo]['time'].append(np.mean(algo_epoch['time']))
    
    utils.displayResults(results)
