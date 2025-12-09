import os

from dotenv import load_dotenv


class Config:
    """Configuration loader for environment variables."""

    def __init__(self) -> None:
        load_dotenv()
        self.max_projects: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
        self.max_tasks: int = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))


#load_dotenv()

# متغیرها رو از env می‌خونه
#DB_USER = os.getenv("DB_USER")
#DB_PASSWORD = os.getenv("DB_PASSWORD")
#DB_HOST = os.getenv("DB_HOST")
#DB_PORT = os.getenv("DB_PORT")
#DB_NAME = os.getenv("DB_NAME")

# ساخت connection string نهایی
#DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"