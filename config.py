import os

class Config:
    """Basic configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change_me')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
