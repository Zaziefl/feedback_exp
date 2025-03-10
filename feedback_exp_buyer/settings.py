from os import environ
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default="postgres://ud3if1lg3n1dk1:pbb701783c442cb07bb8f7fe876dbeeef903ebaa82a4b9ca9757a620df3178a2b@c724r43q8jp5nk.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d6btc0o51dni39")
}



SESSION_CONFIGS = [
    dict(name='SVO',
         app_sequence=['svo'],
         num_demo_participants=4,
         condition_pos_default=0,
         rounds_new_matrix=[1, 4, 9, 12, 17],
         rounds_per_matrix=[3, 5, 3, 5],
         owner_first=0
        ),
dict(name='buyers',
         app_sequence=['buyers'],
         num_demo_participants=8,
         condition_pos_default=0,
         rounds_new_matrix=[1, 4, 9, 12, 17],
         rounds_per_matrix=[3, 5, 3, 5],
         owner_first=0
        ),
dict(name='Full',
         app_sequence=['Instruction', 'svo', 'buyers', 'survey', 'Results'],
         num_demo_participants=6,
        ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point= 1 / 50,
    participation_fee=0.00,
    doc="",
    matching='RING',
    select_items='PRIMARY',
    items_in_random_order=True,
    scale=1,
    slider_init='LEFT',
    random_payoff='RAND',
    precision='INTEGERS',
    language='en',
)

PARTICIPANT_FIELDS = ['dictator_payoff', 'recipient_payoff', 'owner_payoff']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = False

ROOMS = [
    dict(
        name='exp_session',
        display_name='Chosing Items Session',
        participant_label_file='_rooms/tr.txt',
    )]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

SECRET_KEY = '8439487796573'

INSTALLED_APPS = ['otree']