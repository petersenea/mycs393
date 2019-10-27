from rule_checker import RuleChecker

class Player(object):
    def __init__(name, stone):
        self.name = name
        self.stone = stone

    """
        move: [Point, Boards]
    """
    def make_a_move(self, move):
        # check valid history
        rule_checker = RuleChecker([self.stone, move])


    def get_name(self):
        return self.name