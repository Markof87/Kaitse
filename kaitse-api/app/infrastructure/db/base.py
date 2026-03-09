from sqlalchemy.orm import DeclarativeBase

# Base class for SQLAlchemy models
# This class can be extended to include common attributes or methods for all models
# SQLAlchemy's DeclarativeBase is used to define the base class for all ORM models, 
# allowing us to create tables and manage database interactions more easily.
class Base(DeclarativeBase):
    pass