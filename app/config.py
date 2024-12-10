import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'your-fallback-api-key-if-needed')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///users.db')
