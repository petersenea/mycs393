from rule_checker import RuleChecker
from board import Board
import copy

class Player(object):
    def __init__(self, name, stone):
        self.name = name
        self.stone = stone
        self.n = 1
        self.opp_stone = self._get_opponent_stone(stone)

    """
        move: [Point, Boards]
    """
    def make_a_move(self, boards):
        # check valid history
        boards = [Board(x) for x in boards]
        rule_checker = RuleChecker()
        if not rule_checker.is_valid_game_history(self.stone, boards):
            return "This history makes no sense!"

        curr_empties = boards[0].get_empty_spots()

        #find first move that allows capture within n moves
        for empty in curr_empties:
            if self.choose_move(copy.deepcopy(boards), self.n, empty):
                return self._create_point(empty[0], empty[1])
        #if there is no move which allows a capture, pick first available valid spot
        for empty in curr_empties:
            if rule_checker.verify_play(self.stone, empty, boards):
                return self._create_point(empty[0], empty[1])
        #if no valid moves, return "pass"
        return "pass"
    
    """
        returns the Point object for the coordinate integers point_x and point_y
    """
    def _create_point(self, point_x, point_y):
        return str(point_x + 1) + '-' + str(point_y + 1) 
    
    def choose_move(self, boards, n, empty):
        if n > 0:
            rule_checker = RuleChecker()
            if rule_checker.verify_play(self.stone, empty, boards):
                new_board = rule_checker.play_move(self.stone, empty, copy.deepcopy(boards[0]))
                if self.check_if_capture(new_board, boards[0]) == True: return True
                else:
                    boards = self.update_history(new_board, boards)
                    curr_empties = new_board.get_empty_spots()
                    for empty in curr_empties:
                        if self.choose_move(boards, n-1, empty): return True
        return False

    def update_history(self, new_board, boards):
        boards.insert(0, new_board)
        if len(boards)>4: 
            boards.pop()
        return boards

    def check_if_capture(self, new_board, old_board):
        opp_stone_count_before = len(old_board.get_points(self.opp_stone))
        opp_stone_count_after = len(new_board.get_points(self.opp_stone))
        return opp_stone_count_after < opp_stone_count_before

    def get_name(self):
        return self.name
    
    def _get_opponent_stone(self, stone):
        if stone == "W":
            return "B"
        else:
            return "W"