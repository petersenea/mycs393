from copy import deepcopy as copy
from board import Board


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
        
