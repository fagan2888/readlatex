
class Params:
    def __init__(self, penalty_height, penalty_duplication):
        self.penalty_duplication = penalty_duplication
        self.penalty_height = penalty_height

Params.default = Params(2, 3)
