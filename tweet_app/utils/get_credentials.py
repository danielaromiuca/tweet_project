"""Gets credentials from environment to connect to Twitter."""
from decouple import config

API_ACCESS_TOKEN = config("API_ACCESS_TOKEN")
API_ACCESS_TOKEN_SECRET = config("API_ACCESS_TOKEN_SECRET")
API_CONSUMER_KEY = config("API_CONSUMER_KEY")
API_CONSUMER_SECRET = config("API_CONSUMER_SECRET")
