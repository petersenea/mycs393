from board import Board
import numpy as np


class ScoreCalculator(object):
    def __init__(self, board):
        self.board = Board(board)

    """
        Calculates the score of a given board for each player
        takes in:
            * board: the game Board
        returns:
            * A dictionary containing the score
    """ 
    def calculate_score(self):
        b_points = len(self.board.get_points('B'))
        w_points = len(self.board.get_points('W'))
        empty_spaces = self.board.get_points(' ')

        #for every empty space not already checked, check to see if it and its neighbor chain is reachable by either opponent     
        while len(empty_spaces) > 0:
            space = empty_spaces.pop(0)

            #find list of all the points with the same MaybeStone that the point is connected to, as they will all be reachable
            #by the same MaybeStones
            neighbor_chain = self.board.neighbor_chain(self.board.get_maybe_stone(space), [space], [space])
            if self.board.is_reachable(space, 'B'):
                if not self.board.is_reachable(space,'W'):
                    b_points += len(neighbor_chain)
            elif self.board.is_reachable(space,'W'):
                w_points += len(neighbor_chain)

            # do not need to check if each one of a chain is reachable, as they are already accounted for
            # remove empty spaces that have already been checked
            # can't do set manipulation because they are lists of lists
            empty_spaces = [i for i in empty_spaces if i not in neighbor_chain]

        return {"B": b_points, "W": w_points}