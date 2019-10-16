from abc import ABC, abstractmethod
import numpy as np

"""
    wrapper class that enforces contracts for the board class
"""
class WrapperBoard(object):
    BOARD_SIZE = 19
    STONES = ['B', 'W']
    MAYBE_STONES = STONES + [" "]
    """
        input_array takes the format [board, statement]
    """
    def __init__(self, input_array):
        self._verify_input_arr(input_array)

        board = Board(input_array[0])
        
        self.ret_value = self._play_move(board, input_array[1])

    """
        returns the contents of self.ret_value
    """
    def ret(self):
        return self.ret_value

    """
        input_array takes the format [board, statement]
        verifies the input_array:
            (1) is a list
            (2) is of length 2
            (3) board is a valid size and has valid markers for each point
            (4) the statment is a valid statement and has the correct number and type of arguments
    """
    def _verify_input_arr(self, input_array):

        if type(input_array) != list: 
            raise BaseException("input_array is not of type list.")

        if len(input_array) != 2:
            raise BaseException("input_array is not of length 2.")

        self._verify_board(input_array[0])
        self._verify_statement(input_array[1])


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
        verifies the statement:
            (1) has a valid method
            (2) has the correct number and type of arguments for that method
    """
    def _verify_statement(self, statement):
        method = statement[0]
        args = statement[1:]

        if method == "occupied?":
            self._check_arg_len(args, method)
            self._check_point(args[0])
        elif method == "occupies?":
            self._check_arg_len(args, method)
            self._check_stone(args[0])
            self._check_point(args[1])
        elif method == "reachable?":
            self._check_arg_len(args, method)
            self._check_point(args[0])
            self._check_maybe_stone(args[1])
        elif method == "place":
            self._check_arg_len(args, method)
            self._check_stone(args[0])
            self._check_point(args[1])
        elif method == "remove":
            self._check_arg_len(args, method)
            self._check_stone(args[0])
            self._check_point(args[1])
        elif method == "get-points":
            self._check_arg_len(args, method)
            self._check_maybe_stone(args[0])
        else:
            raise BaseException("statement method is not a valid method.")
    

    """
        verifies that the number of given arguments is the correct 
        number for the given method
    """
    def _check_arg_len(self, args, method):
        statement_arg_length = {"occupied?": 1, "occupies?" : 2, "reachable?": 2, "place": 2, "remove":2, "get-points": 1}
        if len(args) != statement_arg_length[method]:
            raise BaseException("wrong number of arguments for the method.")
    

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
        #if point[0] > self.BOARD_SIZE or point[1] > self.BOARD_SIZE:
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


    """
        returns a list of ints representing a given Point from a string
    """
    def _create_point(self, point):
        return [int(i) - 1 for i in point.split('-')]


    """
        calls the given method with the appropriate arguments on an instance
        of the Board class and returns the output
    """
    def _play_move(self, board, statement):
        method = statement[0]
        args = statement[1:]

        if method == "occupied?":
            return board.is_occupied(self._create_point(args[0]))
        elif method == "occupies?":
            return board.does_occupy(args[0], self._create_point(args[1]))
        elif method == "reachable?":
            return board.is_reachable(self._create_point(args[0]), args[1])
        elif method == "place":
            return board.place(args[0], self._create_point(args[1]))
        elif method == "remove":
            return board.remove(args[0], self._create_point(args[1]))
        elif method == "get-points":
            return board.get_points(args[0])

    

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
        curr_stone = self.board_array[point[1]][point[0]]
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
        neighbors = self._valid_neighbors(point[0], point[1])
        for neighbor in neighbors:
            if self.board_array[neighbor[1]][neighbor[0]] == maybe_stone:
                return True
            if neighbor not in visited and self.board_array[neighbor[1]][neighbor[0]] == curr_stone:
                queue.append(neighbor)
                visited.append(neighbor)
        if len(queue) == 0:
            return False
        else:
            return self._breadth_first(curr_stone, maybe_stone, queue, visited)
    
    """
        returns a list of Points on the board that contain valid neighbors to the MaybeStone at point_x, point_y 
    """
    def _valid_neighbors(self, point_x, point_y):
        valid_lst = []
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
        if self.board_array[point[1]][point[0]] == self.EMPTY_STONE:
            self.board_array[point[1]][point[0]] = stone
            return self.board_array
        else: 
            return "This seat is taken!"

    """
        returns:
            * a board array with an Empty at Point, if that Point was previously occupied by the given Stone
            * "I am just a board! I cannot remove what is not there!", if that Point was previously not occupied by the given Stone
    """
    def remove(self, stone, point):
        if self.board_array[point[1]][point[0]] == stone:
            self.board_array[point[1]][point[0]] = self.EMPTY_STONE
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

        

