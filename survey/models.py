from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='Question 4. What is your age?', min=15, max=120)

    gender = models.IntegerField(choices=[[0, 'Female'], [1, 'Male'], [2, 'Prefer not to say or other']],
        label='Question 5. What is your gender?',
        widget=widgets.RadioSelectHorizontal
    )

    major = models.StringField(label='Question 6. What is your major?')

    first_name = models.StringField(label='Please enter your first name')
    last_name = models.StringField(label='Please enter your last name')
    iban = models.StringField(label='Please enter your IBAN')
    iban = models.StringField(label='Please enter your IBAN')
    street = models.StringField(label='Please enter your street')
    house_number = models.StringField(label='Please enter your house number')
    post_code = models.StringField(label='Please enter your postal code')
    city = models.StringField(label='Please enter your city')
    trust = models.IntegerField(
        label='Question 3. Generally speaking, would you say that most people can be trusted, or that you can’t be too careful in dealing with people?',
        choices=[[0, '0 (You can’t be too careful)'], [1, '1'], [2, '2'], [3, '3'], [4, '4'], [5, '5'],
                 [6, '6'], [7, '7'], [8, '8'], [9, '9'], [10, '10 (Most people can be trusted)']],
        widget=widgets.RadioSelect,
    )
    pass