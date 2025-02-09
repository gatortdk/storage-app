from models import Base, engine

def initialize_database():
    """Creates all tables in the database if they do not exist."""
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()
