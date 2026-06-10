# config.py
from config import Config

app.config.from_object(Config)

class Config:
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "password"
    DB_NAME = "smoothie_db"
