import random
import math


class SamplingMatrix:
    def __init__(self, matrix_id, number_items, players):
        self.matrix_id = matrix_id
        self.players = players
        good_items = random.sample(range(0, number_items), 6)  # Set number of good items
        self.values = 0
        for i in good_items:
            self.values += pow(2, i)
        for i in range(number_items):
            exec('self.pr%s = 0' % i)
            exec('self.neur%s = 0' % i)
            exec('self.nr%s = 0' % i)
        del i


class MatrixManager:
    def __init__(self, number_players, round_switch, number_items, subgroup_size):
        self.round_switch = round_switch
        self.number_players = number_players
        self.subgroup_size = subgroup_size
        self.matrix_long = []
        self.matrix_short = []
        for i in range(int(number_players / subgroup_size)):
            self.matrix_long.append(SamplingMatrix(i, number_items, 10))
            self.matrix_short.append(SamplingMatrix(i, number_items, 6))

    def sample_matrix(self, number_player, number_round):
        short = number_round >= self.round_switch
        if short:
            number_round = number_round - self.round_switch
        matrix_id = int(
            (math.ceil(number_player / self.subgroup_size) + number_round) % (self.number_players / self.subgroup_size))
        print('Matrix ' + str(matrix_id) + 'given to player ' + str(number_player))
        if short:
            return self.matrix_short[matrix_id]
        else:
            return self.matrix_long[matrix_id]

    def return_matrix(self, matrix_id, number_round, item, rating, publish):
        short = number_round >= self.round_switch
        if short:
            matrix = self.matrix_short[matrix_id]
        else:
            matrix = self.matrix_long[matrix_id]
        matrix.players -= 1
        if publish:
            if rating == 1:
                exec("matrix.pr%s += %d" % (item, 1))
                print('Positive rating added to Matrix ' + str(matrix_id) + ': ' + str(self.matrix_long[matrix_id].pr0))
            else:
                if rating == 0:
                    exec("matrix.neur%s += %d" % (item, 1))
                else:
                    exec("matrix.nr%s += %d" % (item, 1))
                    print('Negative rating added to Matrix ' + str(matrix_id) + ': ' + str(
                        self.matrix_long[matrix_id].nr0))

    def calculate_owner_payoff(self):
        return 0.5

    pass


# global mm_c1
# global mm_c2
# global mm_c3
# global mm_c4
#
# def get_matrix_manager(condition, number_players, round_switch, number_items, subgroup_size):
#     global mm_c1
#     if mm_c1 is None:
#         mm_c1 = MatrixManager(number_players, round_switch, number_items, subgroup_size)
#     return mm_c1
