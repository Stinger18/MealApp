from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection string that specifies SQLite as the database engine and test.db as the database file.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 

engine = create_engine(
    # creates a SQLAlchemy engine instance for SQLite, which manages connections to the database.
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# is a base class for declarative class definitions, 
# which will be used to define ORM models for any tables (e.g., recipes) in the database.
Base = declarative_base()

# creates and yields a database session using SessionLocal.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_data_from_db(query_params):
    with engine.connect() as conn:
        # Use parameterized queries to prevent SQL injection
        result = conn.execute(text("SELECT * FROM recipes WHERE ingredient = :ingredient"), {"ingredient": query_params})
        return result.fetchall()