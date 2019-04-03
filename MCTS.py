import math
import numpy as np
import random
import collections
from collections import namedtuple
import matplotlib.pyplot as plt
num_rollouts=100
type_estimate='avg_value'
max_iterations=1000000
max_childs=4
import time
class UCTNode():
    def __init__(self, board, move, parent=None):
        self.board = board
        self.move=move
        self.is_expanded = False
        self.parent = parent  # Optional[UCTNode]
        self.children = {}  # Dict[move, UCTNode]
        #self.prior = prior  # float
        #self.total_value = 0  # float
        #self.number_visits = 0  # int
        self.child_priors = np.zeros([max_childs], dtype=np.float32)
        self.child_total_value = np.zeros([max_childs], dtype=np.float32)
        self.child_number_visits = np.zeros([max_childs], dtype=np.float32)

    @property
    def number_visits(self):
        return self.parent.child_number_visits[self.move]

    @number_visits.setter
    def number_visits(self, value):
        self.parent.child_number_visits[self.move] = value

    @property
    def total_value(self):
        return self.parent.child_total_value[self.move]

    @total_value.setter
    def total_value(self, value):
        self.parent.child_total_value[self.move] = value

    def child_Q(self):
        return self.child_total_value / (1 + self.child_number_visits)

    def child_U(self):
        return math.sqrt(self.number_visits) * (
            self.child_priors / (1 + self.child_number_visits))

    def best_child(self):
        #print('node',str(self)[-14:],'childs values', self.child_Q() + self.child_U())
        return np.argmin(self.child_Q() + self.child_U())
    '''
    def Q(self):  # returns float
        return self.total_value / (1 + self.number_visits)

    def U(self):  # returns float
        return (math.sqrt(self.parent.number_visits)
            * self.prior / (1 + self.number_visits))

    #During select_leaf, return the best child node of a given node.
    def best_child(self):
        return min(self.children.values(), key=lambda node: node.Q() + node.U())
    '''
    #Return which node to expand
    def select_leaf(self):
        current = self
        while current.is_expanded:
            best_move_idx = current.best_child()
            #convert idx move to move
            #print('available moves', [mov for mov in current.board.possible_moves])
            best_move=[mov for mov in current.board.possible_moves][best_move_idx]
            current=current.maybe_add_child(best_move, best_move_idx)
        return current

    #Called to expand the current node insterting child nodes
    def expand(self, child_priors):
        self.is_expanded = True
        self.child_priors=child_priors

    def maybe_add_child(self, move, best_move_idx):
        if best_move_idx not in self.children:
            self.children[best_move_idx] = UCTNode(self.board.move(move), best_move_idx, parent=self)
        return self.children[best_move_idx]

    def backup(self, value_estimate):
        current = self
        while current.parent is not None:
            current.number_visits += 1
            current.total_value += value_estimate
            current = current.parent
#required for the root node. IN order to not 
#throw an error when the leaf node is searched
#in def number_visits(self): return self.parent.child_number_visits[self.move]
class DummyNode(object):
  def __init__(self):
    self.parent = None
    self.child_total_value = collections.defaultdict(float)
    self.child_number_visits = collections.defaultdict(float)

def search(board):
    root = UCTNode(board, move=None, parent=DummyNode())
    num_nodes=0 #store the number of nodes explored
    start=time.time()
    for ite in range(max_iterations+1):#while True:
        num_nodes+=1
        print(num_nodes)
        #print('\nnodes expanded', num_nodes)
        #print('root node obj:',str(root)[-14:])
        leaf = root.select_leaf()
        '''
        the problem is that i defined the best action as the one with min value
        the actions are always 4 (even if sometimes 4 actions are not available but only 1/2/3)
        however the value of the 4th action is still in the array.
        this value is 0.
        So, it means that it is the best value possible which is wrong. It must be the worst value

        2 solutions:
            use max but I have to revert the score becvause at the moment the best score is the lower, instead should
            be the higher one.

            set the priors to 1 instead to 0 when created the array of priors.
        
        let's try to set the priors value as 1 as default.
        one is not enough. at the moment the solution is to use inf but is ugly 
        TODO:
        test if setting as infinite affects the speed of the MCTS.
        if so:
            implement the first solution
        otherwise:
            keep it
        '''
        #print('exploring leaf node', leaf)
        #print('lead node board:\n',leaf.board)

        if num_nodes==1000:
            end=time.time()
            print(end-start)
            break


        #if solved of reached limit explored nodes
        if leaf.board.solved or ite==max_iterations:
            print('number node explored', num_nodes)
            #obtain the depth of the selected node
            depth=0
            buf_leaf=leaf
            while buf_leaf.parent is not None:
                depth+=1
                buf_leaf=buf_leaf.parent
            #return the result
            Result = namedtuple('Result', 'board, depth, nodesExpanded, max_depth')
            print('<<ATTENTION>> Max depth is not the real one, it uses the solved node depth.\
                to compute the depth add an attribute to each node that get incremented when it is expanded the first time')
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
        #convert list to array and pad to match max num of childs
        #child_priors_np=np.ones(max_childs)
        child_priors_np=np.full(max_childs, np.inf) #create array of inf values so that the impossible moves are never selected
        child_priors_np[:len(child_priors)]=child_priors

        #expand the leaf node 
        leaf.expand(child_priors_np)
        #update the value of all the parent nodes
        leaf.backup(value_estimate)