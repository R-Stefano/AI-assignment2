from collections import deque, namedtuple

max_iterations=1000000
def search(board):
    """ 
    Performs breadth-first search starting with the 'start' as the beginning
    node. Returns a namedtuple 'Success' which contains namedtuple 'position'
    (includes: node, cost, depth, prev), 'max_depth' and 'nodes_expanded'
    if a node that passes the goal test has been found.

    """

    #It returns a class named Node which contains 4 elements: node, cost, depth, prev
    nodeClass = namedtuple('Node', 'board, cost, depth, prev')

    #instantiate object from class created with the start board position
    node = nodeClass(board, 0, 0, None)
    # frontier contains unexpanded positions
    frontier = deque([node])
    #used to check if the node is already in the frontier obj
    frontier_set = {node}
    #contains the board states already explored, useless add them to the frontier again
    explored_state = set()
    for ite in range(max_iterations+1):#while True:
        # current position is the first position in the frontier
        node = frontier.popleft()

        #get the puzzle board from the object
        board = node.board

        # goal test: return success if True
        if board.solved or ite==max_iterations:
            Result = namedtuple('Result', 'board, depth, nodesExpanded, max_depth')
            return Result(board, node.depth, len(frontier_set), max(no.depth for no in frontier_set))

        # expanded nodes are added to explored_state set
        explored_state.add(board)

        # All reachable positions from current postion are added to frontier
        for mov in board.possible_moves:
            new_board=board.move(mov)
            new_node = nodeClass(new_board, node.cost + 1,
                                    node.depth + 1, node)

            if ((new_board not in explored_state) and (new_node not in frontier_set)):
                frontier.append(new_node)
                frontier_set.add(new_node)
        