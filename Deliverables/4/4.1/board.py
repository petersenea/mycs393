from abc import ABC, abstractmethod
import numpy as np
from copy import deepcopy as copy

"""
    wrapper class that enforces contracts for the board class
"""
class InterfaceWrapper(object):
    BOARD_SIZE = 19
    STONES = ['B', 'W']
    MAYBE_STONES = STONES + [" "]
    """
        input_array takes the format [board, statement]
    """
    def __init__(self, input_):
        self._verify_input_(input_)
        self.ret_value = RuleChecker(input_).ret()

    def ret(self):
        return self.ret_value
        
    """
        input_ takes the format [Stone, Move] or Board
        verifies the input_:
            (1) is a list
            (2) is either of length 2 or a Board
            (3) The Board is a valid Board
            (4) The Stone is a valid Stone
            (5) The Move is a valid Move
    """
    def _verify_input_(self, input_):

        if type(input_) != list: 
            raise BaseException("input_ is not of type list.")

        if len(input_) == 2:
            # check if valid Stone:
            self._check_stone(input_[0])
            # check if valid Move:
            self._check_move(input_[1])

        else:
            self._verify_board(input_)
            
    """
        verifies the board_array:
            (1) is the correct size
            (2) contains only MaybeStones
    """
    def _verify_board(self, board_array):
        if len(board_array) != self.BOARD_SIZE or len(board_array[0]) != self.BOARD_SIZE:
            raise BaseException("board_array is not valid size.")
        else:
            for row in board_array:
                if not all(x in self.MAYBE_STONES for x in row):
                    raise BaseException("board_array does not have valid contents.")
            
   
    """
        verifies that a given Point is valid
    """
    def _check_point(self, point):
        point = point.split("-")
        if len(point) != 2:
            raise BaseException("Point should have 2 indexes.")
        try:
            point = [int(i) for i in point]
        except:
            raise BaseException("Point indexes should be numbers.")
        if 1 > point[0] > self.BOARD_SIZE or 1 > point[1] > self.BOARD_SIZE:
            raise BaseException('Points are not on board')


    """
        verifies that a given Stone is a valid Stone
    """
    def _check_stone(self, stone):
        if stone not in self.STONES:
            raise BaseException("not a valid Stone.")


    """
        verifies that a given MaybeStone is a valid MaybeStone
    """
    def _check_maybe_stone(self, stone):
        if stone not in self.MAYBE_STONES:
            raise BaseException("not a valid MaybeStone.")


    def _check_move(self, move):
        if len(move) == 2:
            # check [Point, Boards]
            self._check_point(move[0])
            self._check_boards(move[1])
        elif move != "pass":
            raise BaseException("Move is not valid.")

    
    def _check_boards(self, boards_arr):
        if 1 <= len(boards_arr) <= 3:
            [self._verify_board(x) for x in boards_arr]
        else:
            raise BaseException("Boards array is not valid length.")

    

class RuleChecker(object):
    """
        input_ is either [Stone, Move] or Board
    """
    
    def __init__(self, input_):
        if len(input_) == 2:
            if input_[1] == "pass":
                self.ret_value = True
            else:
                self.ret_value = self._verify_play(input_)
        else:
            # calculate score of input_
            self.ret_value = self._calc_score(Board(input_))

    def ret(self):
        return self.ret_value

    def _calc_score(self, board):
        b_points = len(board.get_points('B'))
        w_points = len(board.get_points('W'))
        empty_spaces = board.get_points(' ')

        #for every empty space not already checked, check to see if it and its neighbor chain is reachable by either opponent     
        while len(empty_spaces) > 0:
            space = empty_spaces.pop(0)

            #find list of all the points with the same MaybeStone that the point is connected to, as they will all be reachable
            #by the same MaybeStones
            neighbor_chain = board.neighbor_chain(board.get_maybe_stone(space), [space], [space])
            if board.is_reachable(space, 'B'):
                if not board.is_reachable(space,'W'):
                    b_points += len(neighbor_chain)
            elif board.is_reachable(space,'W'):
                w_points += len(neighbor_chain)

            # do not need to check if each one of a chain is reachable, as they are already accounted for
            # remove empty spaces that have already been checked
            # can't do set manipulation because they are lists of lists
            empty_spaces = [i for i in empty_spaces if i not in neighbor_chain]

        return {"B": b_points, "W": w_points}

    def _create_point(self, point):
        return [int(i) - 1 for i in point.split('-')]
    
    def _verify_play(self, input_):
        stone = input_[0]
        play = input_[1]
        point = self._create_point(play[0])
        boards = [Board(board) for board in play[1]]

        next_board = self._play_move(stone, point, copy(boards[0]))

        if next_board:
            if len(boards) > 1 and self._ko_rule_violated(next_board, boards[1]): return False
            else: return self._is_valid_game_history(stone, self._get_opponent_stone(stone), boards)
        else: return False

    
    def _ko_rule_violated(self, board1, board2):
        return board1.board_array == board2.board_array

    def _is_valid_game_history(self, stone, opp_stone, boards):
        # boards = [Board(board) for board in boards]
        # check that every board has proper liberties first
        
        for board in boards:
            if not self._check_board_liberities(board): return False

        if len(boards) == 1:
            if stone == "B" and boards[0]._is_board_empty(): return True
            else: return False
        elif len(boards) == 2:
            if stone == "W" and boards[1]._is_board_empty():
                if len(boards[0].get_points("W")) == 0 and 0 <= len(boards[0].get_points("B")) <= 1: return True
            return False
    
        else:
            if self._ko_rule_violated(boards[0], boards[2]): return False
            if boards[1]._is_board_empty() and stone != "B": 
                return False

            pass_count = 0
            valid1, pass_count = self._validate_turn(boards[0], boards[1], opp_stone, pass_count)
            valid2, pass_count = self._validate_turn(boards[1], boards[2], stone, pass_count)
            if valid1 and valid2 and pass_count < 2: return True
            else: return False



    def _validate_turn(self, curr_board, prev_board, stone, pass_count):
        curr_stones = curr_board.get_points(stone)
        prev_stones = prev_board.get_points(stone)
        player_point = [i for i in curr_stones if i not in prev_stones]
        if len(player_point) == 1:
            simulation_board = self._play_move(stone, player_point[0], copy(prev_board))
            if simulation_board and simulation_board.board_array == curr_board.board_array: return True, pass_count
            else: return False, pass_count
        elif curr_board.board_array == prev_board.board_array:
            return True, pass_count + 1
        else: return False, pass_count


    def _check_board_liberities(self, board):
        taken_intersections = board.get_points('B') + board.get_points('W')

        #for every empty space not already checked, check to see if it and its neighbor chain is reachable by either opponent     
        while len(taken_intersections) > 0:
            intersection = taken_intersections.pop(0)

            if not self._has_liberty(board, intersection): return False

            #find list of all the points with the same MaybeStone that the point is connected to, as if one has a liberty all do
            neighbor_chain = board.neighbor_chain(board.get_maybe_stone(intersection), [intersection], [intersection])          
            
            taken_intersections = [i for i in taken_intersections if i not in neighbor_chain]

        return True      
            
    def _get_opponent_stone(self, stone):
        if stone == "W":
            return "B"
        else:
            return "W"

    
    """
        takes in:
            * stone: the Stone that will be removed
            * point: the Point where the opposing stone has just been placed
            * board: the game Board
        returns:
            * True, if remove is successful
            * False, otherwise
    """
    def _remove_stones(self, stone, point, board):
        # gets the direct neighbors of point
        neighbors = board._valid_neighbors(point)

        # check that each neighbor has a liberty, if not remove the whole neighbor_chain
        for neighbor in neighbors:
            if board.get_maybe_stone(neighbor) == stone:
                if not self._has_liberty(board, neighbor):
                    neighbor_chain = board.neighbor_chain(stone, [neighbor], [neighbor])
                    for point in neighbor_chain:
                        is_remove_successful = board.remove(stone, point)
                        if not is_remove_successful: return False
        return True

    """
        takes in:
            * board:
            * point:
        returns:
            * False
            * True
    """
    def _has_liberty(self, board, point):
        return board.is_reachable(point, ' ')


    # actually implemented elsewhere in _verify_play and _is_valid_game_history
    def _play_move(self, stone, point, simulation_board):
        is_place_successful = simulation_board.place(stone, point)
        if is_place_successful:
            opp_stone = self._get_opponent_stone(stone)
            self._remove_stones(opp_stone, point, simulation_board)

            #if the stone placed has a liberty return true, else return false due to suicide rule
            if self._has_liberty(simulation_board, point): return simulation_board
        return False
        


class Board(object):
    EMPTY_STONE = " "
    BOARD_SIZE = 19  

    def __init__(self, board_array):
        self.board_array = board_array
    
    """
        returns:
            * True if there is a Stone at the given Point on the board
            * False otherwise
    """
    def is_occupied(self, point):
        if self.board_array[point[1]][point[0]] != self.EMPTY_STONE:
            return True
        else: return False

    """
        returns:
            * True if the given Stone is at the given Point on the board
            * False otherwise
    """
    def does_occupy(self, stone, point):
        if self.board_array[point[1]][point[0]] == stone:
            return True
        else: return False

    """
        returns:
            * True if there exists a path from the given Point to the given MaybeStone
            * False otherwise
    """
    def is_reachable(self, point, maybe_stone):
        curr_stone = self.get_maybe_stone(point)
        if curr_stone == maybe_stone:
            return True
        else:
            return self._breadth_first(curr_stone, maybe_stone, [point], [])

    """
        performs a breadth first search on the board
        returns:
            * True if the desired MaybeStone is located in the search
            * False otherwise
    """
    def _breadth_first(self, curr_stone, maybe_stone, queue, visited):
        point = queue.pop(0)
        neighbors = self._valid_neighbors(point)
        for neighbor in neighbors:
            if self.get_maybe_stone(neighbor) == maybe_stone:
                return True
            if neighbor not in visited and self.get_maybe_stone(neighbor) == curr_stone:
                queue.append(neighbor)
                visited.append(neighbor)
        if len(queue) == 0:
            return False
        else:
            return self._breadth_first(curr_stone, maybe_stone, queue, visited)
    
    """
        returns a list of Points on the board that contain valid neighbors to the MaybeStone at point_x, point_y 
    """
    def _valid_neighbors(self, point):
        valid_lst = []
        point_x = point[0]
        point_y = point[1]
        if (point_x + 1) < self.BOARD_SIZE:
            valid_lst.append([point_x +1, point_y])
        if (point_y + 1) < self.BOARD_SIZE:
            valid_lst.append([point_x, point_y + 1])
        if (point_x - 1) >= 0:
            valid_lst.append([point_x - 1, point_y])
        if (point_y - 1) >= 0:
            valid_lst.append([point_x, point_y - 1])
        return valid_lst


    """ CHANGED 
        mutates self.board_array with the new Stone at Point, if that Point was previously empty
        returns:
            * True, if mutation occurs
            * False, if that Point was previously filled with a Stone
    """
    def place(self, stone, point):
        if self.get_maybe_stone(point) == self.EMPTY_STONE:
            self.set_maybe_stone(point, stone)
            return True
        else: 
            return False

    """ CHANGED
        mutates self.board_array with an Empty at Point, if that Point was previously occupied by the given Stone
        returns:
            * True, if mutation occurs
            * False, if that Point was previously not occupied by the given Stone
    """
    def remove(self, stone, point):
        if self.get_maybe_stone(point) == stone:
            self.set_maybe_stone(point, self.EMPTY_STONE)
            return True
        else: return False

    """
        CHANGED: returns a list of [x,y] lists (unordered)
    """
    def get_points(self, maybe_stone):
        np_array = np.array(self.board_array)

        points = np.where(np_array == maybe_stone)

        points_coords = [[points[1][i], points[0][i]] for i in range(len(points[0]))]

        return points_coords
   
    """
        ############ Added since assignment 3 ############
    """
    def get_maybe_stone(self, point):
        return self.board_array[point[1]][point[0]]
    
    def set_maybe_stone(self, point, maybe_stone):
        self.board_array[point[1]][point[0]] = maybe_stone

    def neighbor_chain(self, curr_stone, queue, visited):
        point = queue.pop(0)
        neighbors = self._valid_neighbors(point)
        for neighbor in neighbors:
            if neighbor not in visited and self.get_maybe_stone(neighbor) == curr_stone:
                queue.append(neighbor)
                visited.append(neighbor)
        if len(queue) == 0:
            return visited
        else:
            return self.neighbor_chain(curr_stone, queue, visited)

    def _is_board_empty(self):
        return len(self.get_points(" ")) == self.BOARD_SIZE**2

        

