from itertools import chain
from random import choice
import random

class Puzzle:
    HOLE = 0

    """
    A class representing an '8-puzzle'.
    - 'board' should be a square list of lists with integer entries 0...width^2 - 1
       e.g. [[1,2,3],[4,0,6],[7,5,8]]
    """
    '''
    possible values:
        placed
        orderedPlaced
        manhattan
    '''
    def __init__(self, board, hole_location=None, width=None):
        # Use a flattened representation of the board (if it isn't already)
        self.board = list(chain.from_iterable(board)) if hasattr(board[0], '__iter__') else board
        self.hole = hole_location if hole_location is not None else self.board.index(Puzzle.HOLE)
        self.width =width if width is not None else len(board)
        self.num_values=self.width*self.width
        self.scoretype='placed'

    @property
    def solved(self):
        """
        The puzzle is solved if the flattened board's numbers are in
        increasing order from left to right and the '0' tile is in the
        last position on the board
        """
        return self.board == list(range(1, self.width * self.width)) + [Puzzle.HOLE]

    @property 
    def possible_moves(self):
        """
        A generator for the possible moves for the hole, where the
        board is linearized in row-major order.  Possibilities are
        -1 (left), +1 (right), -width (up), or +width (down).

        Return:
            dest: a generator which contains the idxs of the list where the 
                    the hole(0) could go
        """
        # Up, down
        for dest in (self.hole - self.width, self.hole + self.width):
            if 0 <= dest < len(self.board):
                yield dest
        # Left, right
        for dest in (self.hole - 1, self.hole + 1):
            if dest // self.width == self.hole // self.width:
                yield dest

    def move(self, destination):
        """
        Move the hole to the specified index.
        Args:
            destination: the idx where to move the 0 (the possible idxs are retrieved using possible_moves)
        
        Return:
            Puzzle(obj): A new puzzle object with the new board configuration
        """
        board = self.board[:]
        board[self.hole], board[destination] = board[destination], board[self.hole]
        return Puzzle(board, destination, self.width)

    @property 
    def score(self):
        #Higher number means more far away from the goal
        if self.scoretype=='orderedPlaced':
            pairs=[i==j for i, j in zip(range(1, (self.num_values+1)), self.board)]
            for i, value in enumerate(pairs):
                if not(value):
                    return ((self.num_values-1)-i)
        elif self.scoretype=='placed':
            return ((self.num_values-1)-[i==j for i, j in zip(range(1, self.num_values+1), self.board)].count(True))
        elif self.scoretype=='manhattan':
            #goal = [1, 2, 3, 8, 0, 4, 7, 6, 5]
            goal = [i for i in range(1, self.num_values)]
            goal.append(0)
            return sum(abs(b%3 - g%3) + abs(b//3 - g//3) for b, g in ((self.board.index(i), goal.index(i)) for i in range(1, self.num_values)))


    def shuffle(self, moves=1000):
        """
        When the program starts, shuffle the default configuration.
        Return a new puzzle that has been shuffled with random moves
        """
        p = self
        for _ in range(moves):
            p = p.move(choice(list(p.possible_moves)))
        return p

    @staticmethod
    def direction(a, b):
        """
        The direction of the movement of the hole (L, R, U, or D) from a to b.
        """
        if a is None:
            return None
        return {
                -a.width: 'U',
                -1: 'L',    
                0: None,    
                +1: 'R',
                +a.width: 'D'
        }[b.hole - a.hole]

    def __str__(self):
        return "\n".join(str(self.board[start : start + self.width])
                         for start in range(0, len(self.board), self.width))

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        h = 0
        for value, i in enumerate(self.board):
            h ^= value << i
        return h
    #required when in priority queue priority has same value
    #priorityqueue compare the objects and this func is called
    #randomly say if bigger or lesser than the other one
    def __lt__(self, other):
        return bool(random.getrandbits(1))