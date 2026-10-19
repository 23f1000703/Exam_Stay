import os
class Config:
    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = "sqlite:///examstay.db"
    SQLALCHEMY_TRACK_MODIFICATION = False

    JWT_SECRET_KEY = ""

    REDIS_URL ="redis://localhost:6379/0"

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    OTP_LENGTH = 6
    OTP_EXPIRY_SECONDS = 300
    OTP_MAX_ATTEMPTS = 5