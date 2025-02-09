from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define the SQLite database
DB_URL = "sqlite:///storage.db"
engine = create_engine(DB_URL, echo=True)  # Set echo=True for debugging SQL queries

# Base class for models
Base = declarative_base()

# Define the Storage Units table (ensuring correct table name and schema)
class StorageUnit(Base):
    __tablename__ = "storage_units"
    
    unit_id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    occupied = Column(Boolean, nullable=False, default=False)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=True)

    tenant = relationship("Tenant", back_populates="units")

# Define the Tenants table
class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    move_in_date = Column(String, nullable=True)
    lease_end_date = Column(String, nullable=True)
    payment_status = Column(String, nullable=False)

    units = relationship("StorageUnit", back_populates="tenant")

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

