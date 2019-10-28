from game import Game

#["register"]
#["receive-stone", Stone]
#[["make-a-move"], Boards]


"""
    wrapper class that enforces contracts for the board class
"""
class InterfaceWrapper(object):
    BOARD_SIZE = 19
    STONES = ['B', 'W']
    MAYBE_STONES = STONES + [" "]
    """
        input_array takes the format of a giant json obj array
    """
    def __init__(self, input_):
        self._verify_input_(input_)
        self.ret_value = Game(input_).ret()

    def ret(self):
        return self.ret_value
        
    """
        input_ takes the format [["register"], ["receive-stones", Stone], ["make-a-move", Boards], ...]
        verifies the input_:
            (1) is a list
            (2) first element is a ["register"]
            (3) second element is a ["receive-stones", Stone]
            (4) third element on is a ["make-a-move", Boards]
    """
    def _verify_input_(self, input_):
        if type(input_) != list: 
                raise BaseException("input_ is not of type list.")
        
        for i in range(len(input_)):
            if i == 0:
                if len(input_[i]) == 1:
                    if input_[i][0] != "register":
                        raise BaseException("input_[0] is of length 1, but is not 'register'.")
                else:
                    raise BaseException("input_[0] is not of length 1.")
            elif i == 1:
                if len(input_[i]) == 2:
                    if input_[i][0] == "receive-stones":
                        self._check_stone(input_[i][1])
                    else:
                        raise BaseException("input_[1] is not a valid 'receive-stones'")
                else:
                    BaseException("input_ is of length 2, but is otherwise invalid.")
            else:
                if len(input_[i]) == 2:            
                    if input_[i][0] == "make-a-move":
                        self._check_boards(input_[i][1])
                    else:
                        raise BaseException("input_[1] is not a valid 'make-a-move'")
                
                else:
                    BaseException("input_ is of length 2, but is otherwise invalid.")

                         
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
        verifies that 
            (1) the boards array is the proper length
            (2) every board is a valid board in boards array
    """
    def _check_boards(self, boards_arr):
        if 1 <= len(boards_arr) <= 3:
            [self._verify_board(x) for x in boards_arr]
        else:
            raise BaseException("Boards array is not valid length.")
