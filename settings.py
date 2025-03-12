from os import environ

SESSION_CONFIGS = [
    dict(name='SVO',
         app_sequence=['svo'],
         num_demo_participants=6,
        ),
dict(name='buyers',
         app_sequence=['buyers'],
         num_demo_participants=6,
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
    {
        'name': 'experiment_room',
        'display_name': 'Experiment Room',
    },
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

SECRET_KEY = '8439487796573'

INSTALLED_APPS = ['otree']