from app.cli.console import CLI
from app.core.config import Config

if __name__ == "__main__":
    config = Config()
    CLI(config).run()