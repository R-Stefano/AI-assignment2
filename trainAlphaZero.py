import math
import numpy as np
import random
from collections import namedtuple
import matplotlib.pyplot as plt
from puzzle8 import Puzzle

input_seq_length=8 #use the last 8 board states as input

max_iterations=1000000
import time

root_childs={}
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
        return (math.sqrt(self.parent.number_visits)* self.prior / (1 + self.number_visits))

    #During select_leaf, return the best child node of a given node.
    def best_child(self):
        return max(self.children.values(), key=lambda node: node.Q() + node.U())

    #Return which node to expand
    def select_leaf(self):
        current = self
        board_size=int(math.sqrt(len(current.board.board)))
        seq_states=[]
        seq_states.append(current.board.board)
        while current.is_expanded:
            current = current.best_child()
            seq_states.append(current.board.board)
        seq_states=np.asarray(seq_states)
        print(seq_states.shape)
        seq_states=np.transpose(seq_states, (1,0))
        print(seq_states.shape)
        if (len(seq_states)<input_seq_length):
            seq_pads=np.zeros((board_size,board_size,input_seq_length))

        print('shape seq_states:',seq_states.shape[0])
        return current

    #Called to expand the current node: insterting child nodes
    def expand(self, child_priors, childs):
        self.is_expanded = True
        for move_idx, prior in enumerate(child_priors):
            self.children[move_idx] = UCTNode(childs[move_idx], parent=self, prior=prior)

    def backup(self, value_estimate):
        current = self
        while current.parent is not None:
            current.number_visits += 1
            current.total_value += value_estimate
            current = current.parent
        #increment root node visits
        current.number_visits+=1
        
def search(board):
    global root_childs
    root = UCTNode(board)
    num_nodes=0
    start=time.time()
    for ite in range(max_iterations+1):#while True:
        num_nodes+=1
        print('step:',num_nodes)
        leaf = root.select_leaf()

        if leaf.board.solved or ite==max_iterations:
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
        
        #feed the state sequence to the model, return priors and value of leaf node

        #HERE THE NEURAL NETWORK

        #expand the leaf node 
        leaf.expand(child_priors, childs)
        #DEBUG COUNT NUMBER TIMES CHILD ROOT NODE ARE VISITED
        if num_nodes==1:
            for c in leaf.children.values():
                root_childs[str(c)[-9:]]=[0]

        max_error=50
        #update the value of all the parent nodes
        leaf.backup((max_error-value_estimate)/max_error)

board3 = [[1,2,3],
            [4,0,6],
            [7,5,8]]

search(Puzzle(board3).shuffle())