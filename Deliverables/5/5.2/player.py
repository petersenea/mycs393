from rule_checker import RuleChecker
from board import Board
from copy import deepcopy as copy

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
        if not rule_checker.is_valid_game_history(self.stone, boards):
            return "This history makes no sense!"

        move = self.choose_move(boards, self.n)
        return self._create_point(move[0], move[1])
        '''

        curr_board = Board(boards[0])
        curr_empties = curr_board.get_points(" ")

        for empty in curr_empties:
            if rule_checker.verify_play(self.stone, empty, boards):
                return self._create_point(empty[0], empty[1])
        '''
        return "pass"
    
    """
        returns the Point object for the coordinate integers point_x and point_y
    """
    def _create_point(self, point_x, point_y):
        return str(point_x + 1) + '-' + str(point_y + 1) 
    
    def choose_move(self, boards, n):
        empties = Board(boards[0]).get_points(" ")
        rule_checker = RuleChecker()
        for empty in empties:
            print(empty)
            if rule_checker.verify_play(self.stone, empty, boards):
                new_board = rule_checker.play_move(self.stone, empty, copy(Board(copy(boards[0]))))
                opp_stone_count_before = len(Board(boards[0]).get_points(self._get_opponent_stone(self.stone)))
                opp_stone_count_after = len(new_board.get_points(self._get_opponent_stone(self.stone)))
                print("oppstonecount",opp_stone_count_before, opp_stone_count_after)
                if opp_stone_count_after < opp_stone_count_before:
                    print("hi", empty)
                    print('board1 /n', boards[0])
                    print('board2 /n', new_board.board_array)
                    return empty
                boards.insert(0, new_board.board_array)
                if len(boards)>4:
                    boards.pop()
                if self.choose_move_rec(boards, n-1) == True: 
                    print('??')
                    return empty
        print("hell")
        return "pass"

    def choose_move_rec(self, boards, n):
        # print("here")
        if n > 0:
            # print("here2")
            empties = Board(boards[0]).get_points(" ")

            rule_checker = RuleChecker()
            for empty in empties:
                if rule_checker.verify_play(self.stone, empty, boards):
                    new_board = rule_checker.play_move(self.stone, empty, copy(Board(boards[0])))

                    opp_stone_count_before = len(Board(boards[0]).get_points(self._get_opponent_stone(self.stone)))
                    opp_stone_count_after = len(new_board.get_points(self._get_opponent_stone(self.stone)))


                    if opp_stone_count_after < opp_stone_count_before:
                        return True
                    boards.insert(0, new_board.board_array)
                    if len(boards)>4:
                        boards.pop()
                    if self.choose_move_rec(boards, n-1) == True: return True
        return False


    def get_name(self):
        return self.name
    
    def _get_opponent_stone(self, stone):
        if stone == "W":
            return "B"
        else:
            return "W"