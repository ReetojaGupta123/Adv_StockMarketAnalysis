import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/stockdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
