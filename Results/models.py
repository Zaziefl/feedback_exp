from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'results'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    open_text = models.LongStringField(label='Let me know what you think:');
    pass
