from abc import ABC, abstractmethod
import numpy as np

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

    """
        returns a list of ints representing a given Point from a string
    """
    def _create_point(self, point):
        return [int(i) - 1 for i in point.split('-')]


    

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
            board = Board(input_)
            self.ret_value = self._calc_score(board)

    def ret(self):
        return self.ret_value

    def _calc_score(self, board):
        b_points = len(board.get_points('B'))
        w_points = len(board.get_points('W'))
        empty_spaces = [self._create_point(space) for space in board.get_points(' ')]   

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
        opp_stone = self._get_opponent_stone(stone)
        play = input_[1]
        point = self._create_point(play[0])
        boards = play[1]

        current_board = Board(boards[0])

        # check if the boards array history is valid
        if self._is_valid_game_history(stone, opp_stone, boards):
            
            next_board_arr = current_board.place(stone, point)
            
            if next_board_arr == "This seat is taken!":
                return False
            else:

                # remove opponents liberty-less pieces
                next_board_arr = self._remove_stones(opp_stone, point, next_board_arr)
                next_board = Board(next_board_arr)
                
                # verify that there are liberties
                """ STILL NEED TO IMPLEMENT """

                # check for suicide
                print(point)
                if next_board.is_reachable(point, " "):
                    return True
                else:
                    return False


        else:
            return False
    
    def _is_valid_game_history(self, stone, opp_stone, boards):
        if len(boards) == 1:
            if stone == "B" and self._is_board_empty(boards[0]): return True
            else: return False
        elif len(boards) == 2:
            if stone == "W":
                if self._is_board_empty(boards[1]):
                    curr_board = Board(boards[0])
                    if len(curr_board.get_points("W")) == 0 and 0 <= len(curr_board.get_points("B")) <= 1:
                        return True
            return False
    
        else:
            curr_board = Board(boards[0])
            prev_board = Board(boards[1])
            last_board = Board(boards[2])


            # last turn was the opponent's
            # since no suicide, they should have increased their stone count by 1 on the board
            curr_opp_stones = curr_board.get_points(opp_stone)
            prev_opp_stones = prev_board.get_points(opp_stone)
            if len(curr_opp_stones) - len(prev_opp_stones) == 1:
                # find point of added stone
                opp_point = self._create_point(list(set(curr_opp_stones) - set(prev_opp_stones))[0])
                
                # add stone
                new_arr = prev_board.place(opp_stone, opp_point)
                if new_arr == "This seat is taken!":
                    return False

                # remove opps
                new_arr = self._remove_stones(stone, opp_point, new_arr)

                # compare boards
                if boards[0] != new_arr:
                    return False
                
                # turn before last was the current player's
                # since no suicide, they should have increased their stone count by 1 on the board 
                prev_player_stones = prev_board.get_points(stone)
                last_player_stones = last_board.get_points(stone)
                if len(prev_player_stones) - len(last_player_stones) == 1:
                    # find point of added stone
                    player_point = self._create_point(list(set(prev_player_stones) - set(last_player_stones))[0])

                    # add stone
                    new_arr = prev_board.place(stone, player_point)
                    if new_arr == "This seat is taken!": return False

                    # remove opps
                    new_arr = self._remove_stones(opp_stone, player_point, new_arr)

                    # compare boards
                    if boards[1] != new_arr:
                        return False
                    else:
                        return True

                else:
                    return False
            
            else:
                return False
            
            
    def _get_opponent_stone(self, stone):
        if stone == "W":
            return "B"
        else:
            return "W"

    def _is_board_empty(self, board_array):
        board = Board(board_array)
        return len(board.get_points(" ")) == board.BOARD_SIZE**2

    def _remove_stones(self, stone, point, board_array):
        # assume the stone has already been placed for the turn
        # stone is the type you are removing
        board = Board(board_array)
        neighbors = board._valid_neighbors(point)
        for neighbor in neighbors:
            if board.get_maybe_stone(neighbor) == stone:
                neighbor_chain = board.neighbor_chain(stone, [neighbor], [neighbor])
                if not self._has_liberty(board, neighbor):
                    for point in neighbor_chain:
                        board.remove(stone, point)
        return board.board_array

    def _has_liberty(self, board, point):
        return board.is_reachable(point, ' ')


    # actually implemented elsewhere in _verify_play and _is_valid_game_history
    def _play_move(self, stone, point, board_array):
        # place stone
        # remove opponents stones using _remove_stones
        # verify that there are liberties
        pass

    

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


    """
        returns:
            * a board array with the new Stone at Point, if that Point was previously empty
            * "This seat is taken!", if that Point was previously filled with a Stone
    """
    def place(self, stone, point):
        if self.get_maybe_stone(point) == self.EMPTY_STONE:
            self.set_maybe_stone(point, stone)
            return self.board_array
        else: 
            return "This seat is taken!"

    """
        returns:
            * a board array with an Empty at Point, if that Point was previously occupied by the given Stone
            * "I am just a board! I cannot remove what is not there!", if that Point was previously not occupied by the given Stone
    """
    def remove(self, stone, point):
        if self.get_maybe_stone(point) == stone:
            self.set_maybe_stone(point, self.EMPTY_STONE)
            return self.board_array
        else: return "I am just a board! I cannot remove what is not there!"

    """
        returns a list of lexigraphically ordered Points where the given MaybeStone exists on the board
    """
    def get_points(self, maybe_stone):
        np_array = np.array(self.board_array)

        points = np.where(np_array == maybe_stone)
             
        points_coords = [self._create_point(points[1][i], points[0][i]) for i in range(len(points[0]))]

        points_coords.sort()

        return points_coords

    """
        returns the Point object for the coordinate integers point_x and point_y
    """
    def _create_point(self, point_x, point_y):
        return str(point_x + 1) + '-' + str(point_y + 1)
    
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

        

