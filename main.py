from dotenv import load_dotenv
import os

def main():
    """Entry point for the ToDoList application."""
    load_dotenv()
    max_tasks = int(os.getenv("MAX_TASKS", 100))
    print(f"ToDoList App started. Max tasks: {max_tasks}")

if __name__ == "__main__":
    main()