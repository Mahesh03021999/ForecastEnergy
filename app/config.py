import os
class Config:
    SECRET_KEY = 'your_secret_key'
    DATABASE_URL = os.getenv('DATABASE_URL')
