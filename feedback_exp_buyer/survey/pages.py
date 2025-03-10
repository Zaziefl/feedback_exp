from otree.api import *

class End(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return dict(
            first=self.round_number == 1
        )


class ResultsWaitPage(WaitPage):
    pass

class Survey(Page):
    form_model = 'player'
    form_fields = ['trust', 'age', 'gender', 'major']
    pass

class Payment_Details(Page):
    form_model = 'player'
    form_fields = ['first_name', 'last_name', 'street', 'house_number', 'post_code', 'city', 'iban', ]
    pass


page_sequence = [End, Survey, Payment_Details]