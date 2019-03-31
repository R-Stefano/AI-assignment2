import queue as q
from collections import namedtuple
max_iterations=1000000
def search(start):
    """ 
    Performs A* search starting with the initialized puzzle board. 
    Returns a namedtuple 'Success' which contains namedtuple 'position'
    (includes: node, cost, depth, prev), 'max_depth' and 'nodes_expanded'
    if a node that passes the goal test has been found.

    """

    '''
    Create a class named nodeClass which contains 4 elements: 
        state: The puzzle object containing the puzzle board at the node 
        misplaced: num of misplaced tiles
        depth: depth of the node in the tree 
        prev: parent node
    '''
    nodeClass = namedtuple('nodeClass', 'state, misplaced, depth, prev')

    #instantiate object from class creating the root node
    node = nodeClass(start, 0, 0, None)

    #stores the nodes that are going to be explored. 
    #the node with lower f-score is explored first
    frontier = q.PriorityQueue()
    frontier.put((0,node))

    # frontier_set keep track of the nodes in the frontier queue
    frontier_set = {node}
    #contains the board states already explored
    explored_states = set()
    for ite in range(max_iterations+1):#while True:
        #Retrieve the node in the frontier with lowest value
        node = frontier.get()[1]

        #get the puzzle board obj from the node object
        state = node.state

        #Check if the game has ben solved
        if state.solved or ite==max_iterations:
            Result = namedtuple('Result', 'board, depth, nodesExpanded, max_depth')
            return Result(state, node.depth, len(frontier_set), max(no.depth for no in frontier_set))

        # expanded nodes are added to explored set
        explored_states.add(state)

        #EXPANDING
        for mov in state.possible_moves:
            new_state=state.move(mov)
            new_node = nodeClass(new_state, new_state.score,
                                    node.depth + 1, node)

            #compute f-score of the node
            f_score=new_state.score + new_node.depth

            if new_state not in explored_states and new_node not in frontier_set:
                frontier.put((f_score,new_node))
                frontier_set.add(new_node)
        
        '''
        if a new_state is already explored, it means that there could be a better situation 
        or this new one is the best. In order to know, I have to check the nodes.

        What I have to check in the nodes? I have to check for the depth.

        Lesser depth node, better it is. So, I have to keep the less depth one.

        In order to find the less deph, I have to retrieve the node with the same state
        However, I have to be sure to not come back to that node.
        '''