import os
from otree.asgi import get_asgi_application

os.environ.setdefault('OTREE_ENV', 'production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_exp_buyer.settings')

application = get_asgi_application()
