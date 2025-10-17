import os

from dotenv import load_dotenv


class Config:
    """Configuration loader for environment variables."""

    def __init__(self) -> None:
        load_dotenv()
        self.max_projects: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
        self.max_tasks: int = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))