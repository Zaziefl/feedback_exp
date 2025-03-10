import os
import sys
from otree.asgi import get_asgi_application

# Ensure Heroku finds the project folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('OTREE_ENV', 'production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_exp_buyer.settings')

application = get_asgi_application()
