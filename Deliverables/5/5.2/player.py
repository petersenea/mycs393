from rule_checker import RuleChecker
from board import Board
import copy

class Player(object):
    def __init__(self, name, stone):
        self.name = name
        self.stone = stone
        self.n = 1

    """
        move: [Point, Boards]
    """
    def make_a_move(self, boards):
        # check valid history
        rule_checker = RuleChecker()
        if not rule_checker.is_valid_game_history(self.stone, [Board(x) for x in boards]):
            return "This history makes no sense!"
        curr_board = Board(boards[0])
        curr_empties = curr_board.get_points(" ")

        for empty in curr_empties:
            if self.choose_move(boards, self.n, empty):
                return self._create_point(empty[0], empty[1])
        
        return "pass"
    
    """
        returns the Point object for the coordinate integers point_x and point_y
    """
    def _create_point(self, point_x, point_y):
        return str(point_x + 1) + '-' + str(point_y + 1) 
    
    def choose_move(self, boards, n, empty):
        if n > 0:
            boards = [Board(x) for x in boards]
            rule_checker = RuleChecker()
            if rule_checker.verify_play(self.stone, empty, copy.deepcopy(boards)):
                new_board = rule_checker.play_move(self.stone, empty, copy.deepcopy(boards[0]))
                opp_stone_count_before = len(boards[0].get_points(self._get_opponent_stone(self.stone)))
                opp_stone_count_after = len(new_board.get_points(self._get_opponent_stone(self.stone)))
                if opp_stone_count_after < opp_stone_count_before:
                    return True
                boards.insert(0, new_board)
                if len(boards)>4: boards.pop()
                curr_board = Board(boards[0])
                curr_empties = curr_board.get_points(" ")

                for empty in curr_empties:
                    if self.choose_move(boards, n-1, empty): return True
        return False




    def get_name(self):
        return self.name
    
    def _get_opponent_stone(self, stone):
        if stone == "W":
            return "B"
        else:
            return "W"