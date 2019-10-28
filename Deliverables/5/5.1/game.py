
from player import Player

class Game(object):
    #temporary, currently just creates a player with the give stone
    #then calls player.make_a_move on each make_a_move imputed
    #returns a list of the results
    def __init__(self, _input):
        register = _input[0]
        receive_stones = _input[1]
        make_a_moves = _input[2:]
        
        self.ret_list = []

        self.player_1 = Player("no name", receive_stones[1])
        self.ret_list.append(self.player_1.get_name())

        for move in make_a_moves:
            self.ret_list.append(self.player_1.make_a_move(move[1]))

    def ret(self):
        return self.ret_list

        
