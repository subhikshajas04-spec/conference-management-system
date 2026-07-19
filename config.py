import os

class Config:
    SECRET_KEY = 'conference-management-system-secret-key-2026'
    
    # Absolute path for database - This solves the error
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/instance/conference.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads/papers')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB