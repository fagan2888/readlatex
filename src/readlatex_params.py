
class Params:
    def __init__(self, penalty_height = 1, penalty_duplication = 2, resolution_iterations = 1000, resolution_narrowing = 0.1):
        self.penalty_duplication = penalty_duplication
        self.penalty_height = penalty_height
        self.resolution_iterations = resolution_iterations
        self.resolution_narrowing = resolution_narrowing

Params.default = Params()