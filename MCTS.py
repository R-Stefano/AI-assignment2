import math
import numpy as np
import random
from collections import namedtuple
import matplotlib.pyplot as plt
num_rollouts=100
type_estimate='avg_value'
class UCTNode():
    def __init__(self, board, parent=None, prior=0):
        self.board = board
        self.is_expanded = False
        self.parent = parent  # Optional[UCTNode]
        self.children = {}  # Dict[move, UCTNode]
        self.prior = prior  # float
        self.total_value = 0  # float
        self.number_visits = 0  # int

    def Q(self):  # returns float
        return self.total_value / (1 + self.number_visits)

    def U(self):  # returns float
        return (math.sqrt(self.parent.number_visits)
            * self.prior / (1 + self.number_visits))

    #During select_leaf, return the best child node of a given node.
    def best_child(self):
        return min(self.children.values(), key=lambda node: node.Q() + node.U())

    #Return which node to expand
    def select_leaf(self):
        current = self
        while current.is_expanded:
            current = current.best_child()
        return current

    #Called to expand the current node insterting child nodes
    def expand(self, child_priors, childs):
        self.is_expanded = True
        for move, prior in enumerate(child_priors):
            self.add_child(move, childs[move], prior)

    def add_child(self, move, child, prior):
        self.children[move] = UCTNode(child, parent=self, prior=prior)

    def backup(self, value_estimate):
        current = self
        while current.parent is not None:
            current.number_visits += 1
            current.total_value += value_estimate
            current = current.parent
def search(board):
    root = UCTNode(board)
    num_nodes=0
    while True:
        num_nodes+=1
        print('nodes expanded', num_nodes)
        leaf = root.select_leaf()
        if leaf.board.solved:
            #obtain the depth of the selected node
            depth=0
            buf_leaf=leaf
            while buf_leaf.parent is not None:
                depth+=1
                buf_leaf=buf_leaf.parent
            #return the result
            Result = namedtuple('Result', 'board, depth, nodesExpanded, max_depth')
            print('<<ATTENTION>> Max depth is not the real one, it uses the solved node depth')
            return Result(leaf.board, depth, num_nodes, depth)

        #compute probability to select each child node. (They are all equal probable)
        num_moves=[1 for mov in leaf.board.possible_moves]
        child_priors=[1/len(num_moves) for mov in leaf.board.possible_moves]
        #create the child board positions
        childs=[leaf.board.move(mov) for mov in leaf.board.possible_moves]
        
        #compute the value estimation of the node that has been expanded
        if type_estimate=='avg_value':            
            #the estimate is the avg value of the score of the child nodes
            value_estimate = np.mean([child.score for child in childs])
        elif type_estimate=='rollouts':
            values=[]
            buff_board=leaf.board
            for i in range(num_rollouts):
                #pick a random action
                a=random.choice([mov for mov in buff_board.possible_moves])
                buff_board=buff_board.move(a)
                values.append(buff_board.score)
            #the estimate is the avg of the score of 100 successive expansions of the node
            value_estimate=np.mean(values)
        
        #expand the leaf node 
        leaf.expand(child_priors, childs)
        #update the value of all the parent nodes
        leaf.backup(value_estimate)