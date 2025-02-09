from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define the SQLite database
DB_URL = "sqlite:///storage.db"
engine = create_engine(DB_URL, echo=True)  # Set echo=True for debugging SQL queries

# Base class for models
Base = declarative_base()

# Define the Units table
class Unit(Base):
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    unit_number = Column(String, unique=True, nullable=False)
    status = Column(Enum("available", "occupied", "reserved", name="unit_status"), default="available", nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)

    tenant = relationship("Tenant", back_populates="units")

# Define the Tenants table
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)

    units = relationship("Unit", back_populates="tenant")

# Create a session factory
SessionLocal = sessionmaker(bind=engine)
