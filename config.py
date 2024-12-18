import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://avnadmin:AVNS_u8qvjn4F2_gwng59mfR@pg-1ab4f1eb-moviedatabase1.f.aivencloud.com:18022/defaultdb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 