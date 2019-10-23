from rule_checker import RuleChecker


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

    """
        verifies that a Move is a valid Move
    """
    def _check_move(self, move):
        if len(move) == 2:
            # check [Point, Boards]
            self._check_point(move[0])
            self._check_boards(move[1])
        elif move != "pass":
            raise BaseException("Move is not valid.")

    """
        verifies that 
            (1) the boards array is the proper length
            (2) every board is a valid board in boards array
    """
    def _check_boards(self, boards_arr):
        if 1 <= len(boards_arr) <= 3:
            [self._verify_board(x) for x in boards_arr]
        else:
            raise BaseException("Boards array is not valid length.")
