import numpy as np   
from operator import itemgetter

class Board(object):
    EMPTY_STONE = " "
    BOARD_SIZE = 19  

    def __init__(self, board_array):

        self.board_array = np.array(board_array)
    
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
        CHANGED: returns a list of [x,y] lists (sorted by column first, then row)
    """
    def get_points(self, maybe_stone):

        points = np.where(self.board_array == maybe_stone)

        points_coords = [[points[1][i], points[0][i]] for i in range(len(points[0]))]

        points_coords = sorted(points_coords, key=itemgetter(0))


        return points_coords
   
    """
        ############ Added since assignment 3 ############
    """

    """
        returns the MaybeStone at the given point
    """
    def get_maybe_stone(self, point):
        return self.board_array[point[1]][point[0]]
    
    """
        sets a given point to a MaybeStone
    """
    def set_maybe_stone(self, point, maybe_stone):
        self.board_array[point[1]][point[0]] = maybe_stone

    """
        returns a list of Points that are linked together (aka a chain of stones)
    """
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

    """
        returns true if the entire board is empty, otherwise returns false 
    """
    def _is_board_empty(self):
        return len(self.get_points(self.EMPTY_STONE)) == self.BOARD_SIZE**2

    """
        returns list of empty intersections ordered by increasing column first, then row
    """
    def get_empty_spots(self):
        return self.get_points(self.EMPTY_STONE)
        

