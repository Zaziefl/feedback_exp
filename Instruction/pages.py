from otree.api import *


class ResultsWaitPage(WaitPage):
    pass


class Instruction(Page):
    form_model = 'player'
    form_fields = ['consent']
    pass


class Payment(Page):
    pass


page_sequence = [Instruction, Payment]