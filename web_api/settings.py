import os


MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'better_notes')
