import math
import numpy as np
import random
from collections import namedtuple
num_rollouts=100
max_iterations=1000000

class UCTNode():
    def __init__(self, board, depth, parent=None):
        self.board = board
        self.is_expanded = False
        self.parent = parent  # Optional[UCTNode]
        self.children = {}  # Dict[move, UCTNode]
        self.total_value = 0  # float
        self.number_visits = 0  # int
        self.depth=depth #depth of the node

    def Q(self):  # returns float
        return self.total_value / (1 + self.number_visits)

    def U(self):  # returns float
        return math.sqrt(2)*math.sqrt(math.log(self.parent.number_visits)/(1+self.number_visits))

    #During select_leaf, return the best child node of a given node.
    def best_child(self):
        return max(self.children.values(), key=lambda node: node.Q() + node.U())

    #Return which node to expand
    def select_leaf(self):
        current = self
        while current.is_expanded:
            current = current.best_child()
        return current

    #Called to expand the current node: insterting child nodes
    def expand(self, childs):
        self.is_expanded = True
        for move_idx, child in enumerate(childs):
            self.children[move_idx] = UCTNode(child, depth=self.depth+1, parent=self)

    def backup(self, value_estimate):
        current = self
        while current.parent is not None:
            current.number_visits += 1
            current.total_value += value_estimate
            current = current.parent
        #increment root node visits
        current.number_visits+=1
        
def search(board):
    root = UCTNode(board, 0)
    num_nodes=0
    max_depth=0
    for ite in range(max_iterations+1):#while True:
        num_nodes+=1
        print(num_nodes)
        leaf = root.select_leaf()

        #check if new max depth
        if leaf.depth> max_depth:
            max_depth=leaf.depth

        if leaf.board.solved or ite==max_iterations:
            print('solved!')
            #return the result
            Result = namedtuple('Result', 'board, depth, nodesExpanded, max_depth')
            return Result(leaf.board, leaf.depth, num_nodes, max_depth)

        #create the child board positions
        childs=[leaf.board.move(mov) for mov in leaf.board.possible_moves]
        
        #rollouts to compute the value of the node that has been expanded
        value_estimate=-1
        buff_board=leaf.board
        for i in range(num_rollouts):
            #pick a random action
            a=random.choice([mov for mov in buff_board.possible_moves])
            buff_board=buff_board.move(a)
            if buff_board.solved:
                value_estimate=1

        #expand the leaf node 
        leaf.expand(childs)
        #update the value of all the parent nodes
        leaf.backup(value_estimate)