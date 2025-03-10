import random

class SamplingMatrix:
    def __init__(self, number_items, players):
        self.players = players
        good_items = random.sample(range(0, number_items), 5)  # Set number of good items
        self.values = 0
        for i in good_items:
            self.values += pow(2, i)
        for i in range(number_items):
            exec('self.pr%s = 0' % i)
            exec('self.text%s = ""' % i)
            exec('self.nr%s = 0' % i)
        del i


def get_pos_rating(group, item):
    if item == 0:
        return group.pr0
    if item == 1:
        return group.pr1
    if item == 2:
        return group.pr2
    if item == 3:
        return group.pr3
    if item == 4:
        return group.pr4
    if item == 5:
        return group.pr5
    if item == 6:
        return group.pr6
    if item == 7:
        return group.pr7
    if item == 8:
        return group.pr8
    if item == 9:
        return group.pr9
    if item == 10:
        return group.pr10
    if item == 11:
        return group.pr11
    if item == 12:
        return group.pr12
    if item == 13:
        return group.pr13
    if item == 14:
        return group.pr14
    if item == 15:
        return group.pr15


def get_neg_rating(group, item):
    if item == 0:
        return group.nr0
    if item == 1:
        return group.nr1
    if item == 2:
        return group.nr2
    if item == 3:
        return group.nr3
    if item == 4:
        return group.nr4
    if item == 5:
        return group.nr5
    if item == 6:
        return group.nr6
    if item == 7:
        return group.nr7
    if item == 8:
        return group.nr8
    if item == 9:
        return group.nr9
    if item == 10:
        return group.nr10
    if item == 11:
        return group.nr11
    if item == 12:
        return group.nr12
    if item == 13:
        return group.nr13
    if item == 14:
        return group.nr14
    if item == 15:
        return group.nr15


def get_rating_text(group, item):
    if item == 0:
        return group.text0
    if item == 1:
        return group.text1
    if item == 2:
        return group.text2
    if item == 3:
        return group.text3
    if item == 4:
        return group.text4
    if item == 5:
        return group.text5
    if item == 6:
        return group.text6
    if item == 7:
        return group.text7
    if item == 8:
        return group.text8
    if item == 9:
        return group.text9
    if item == 10:
        return group.text10
    if item == 11:
        return group.text11
    if item == 12:
        return group.text12
    if item == 13:
        return group.text13
    if item == 14:
        return group.text14
    if item == 15:
        return group.text15


def get_new_matrix(player, players_per_group, number_items):
    number_players = players_per_group * player.session.config['rounds_per_matrix'][
        player.session.config['rounds_new_matrix'].index(player.round_number)]
    sm = SamplingMatrix(number_items, number_players)
    positive_ratings = []
    negative_ratings = []
    texts = []
    for i in range(number_items):
        exec('positive_ratings.append(sm.pr%s)' % i)
        exec('negative_ratings.append(sm.nr%s)' % i)
        exec('texts.append(sm.text%s)' % i)
    return [sm.values, sm.players, positive_ratings, negative_ratings, texts]


def get_matrix_from_previous_group(current_group, number_items):
    group_list = current_group.subsession.get_groups()
    groups_number = len(group_list)
    group_number = group_list.index(current_group)
    prev_group = current_group.subsession.get_groups()[(group_number + 1) % groups_number].in_round(current_group.round_number - 1)
    positive_ratings = []
    negative_ratings = []
    texts = []
    for i in range(number_items):
        exec('positive_ratings.append(prev_group.pr%s)' % i)
        exec('negative_ratings.append(prev_group.nr%s)' % i)
        exec('texts.append(prev_group.text%s)' % i)
    return [prev_group.values, prev_group.players, positive_ratings, negative_ratings, texts]


def publish_rating(player, rating):
    if rating == 1:
        exec("player.group.pr%s += 1" % player.chose_field)
    else:
        exec("player.group.nr%s += 1" % player.chose_field)
    pos_selected_texts = [player.field_maybe_none('pos_rating_text_1'), player.field_maybe_none('pos_rating_text_2'), player.field_maybe_none('pos_rating_text_3'),
                          player.field_maybe_none('pos_rating_text_4'), player.field_maybe_none('pos_rating_text_5'), player.field_maybe_none('pos_rating_text_6')]
    neg_selected_texts = [player.field_maybe_none('neg_rating_text_1'), player.field_maybe_none('neg_rating_text_2'), player.field_maybe_none('neg_rating_text_3'),
                          player.field_maybe_none('neg_rating_text_4'), player.field_maybe_none('neg_rating_text_5'), player.field_maybe_none('neg_rating_text_6')]
    text = ' '
    if rating == 1:
        text += "2"
        for i in range(6):
            if pos_selected_texts[i]:
                text += str(i + 1)
    else:
        text += "1"
        for i in range(6):
            if neg_selected_texts[i]:
                text += str(i + 1)
        text += ' '
    exec("player.group.text%s += text" % player.chose_field)


def calculate_owner_payoff(player, number_items):
    i = 0
    while player.round_number > player.session.config['rounds_new_matrix'][i] and len(player.session.config['rounds_new_matrix']) > i:
        print(str(player.round_number) + ' larger than' + str(player.session.config['rounds_new_matrix'][i]))
        i += 1
    steps_back = player.round_number - player.session.config['rounds_new_matrix'][i]
    groups_number = len(player.subsession.get_groups())
    group_list = player.subsession.get_groups()
    index_own_group = group_list.index(player.group)
    owner_01 = (index_own_group - 1 - steps_back) % groups_number
    owner_23 = (index_own_group - 2 - steps_back) % groups_number
    owner_45 = (index_own_group - 3 - steps_back) % groups_number
    owner_67 = (index_own_group - 4 - steps_back) % groups_number
    ownership_groups = [owner_01, owner_23, owner_45, owner_67]
    items_chosen = 0
    for i in range(4):
        for p in group_list[ownership_groups[i]].get_players():
            print('Player ' + str(p.id_in_group) + ' chose item ' + str(p.chose_field))
            if p.chose_field == i+4*(player.id_in_group-1):
                items_chosen += 1
    print(str(items_chosen) + ' items of player ' + str(player.id_in_group) + ' chosen.')
    return items_chosen*player.session.config['owner_payoff']


