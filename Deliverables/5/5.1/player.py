from rule_checker import RuleChecker
from board import Board

class Player(object):
    def __init__(self, name, stone):
        self.name = name
        self.stone = stone
        self.rule_checker = RuleChecker()

    """
        takes in:
            * boards: a list of game boards
        returns:
            * A string representing a point of the first valid play
            * "pass", if no plays are possible
    """
    def make_a_move(self, boards):
        # check valid history
        boards = [Board(x) for x in boards]
        if not self.rule_checker.is_valid_game_history(self.stone, boards):
            return "This history makes no sense!"
        
        curr_empties = boards[0].get_empty_spots()

        for empty in curr_empties:
            if self.rule_checker.verify_play(self.stone, empty, boards):
                return self._create_point(empty[0], empty[1])
        return "pass"
    
    """
        returns the Point object for the coordinate integers point_x and point_y
    """
    def _create_point(self, point_x, point_y):
        return str(point_x + 1) + '-' + str(point_y + 1) 

    """
        returns name of player
    """
    def get_name(self):
        return self.name