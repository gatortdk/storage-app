from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define the SQLite database
DB_URL = "sqlite:///storage.db"
engine = create_engine(DB_URL, echo=False)  # Disabled echo, use logging instead

# Base class for models
Base = declarative_base()

# Define the Storage Units table (ensuring correct table name and schema)
class StorageUnit(Base):
    __tablename__ = "storage_units"
    
    unit_id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(String(100), nullable=False)  # Added length constraint
    price = Column(Float, nullable=False)
    occupied = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, default=False)  # Soft delete flag
    
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id", ondelete="SET NULL"), nullable=True)
    tenant = relationship("Tenant", back_populates="units")

# Define the Tenants table
class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  # Added length constraint
    contact = Column(String(255), nullable=False)  # Added length constraint
    move_in_date = Column(String, nullable=True)
    lease_end_date = Column(String, nullable=True)
    payment_status = Column(String(50), nullable=False)  # Added length constraint

    units = relationship("StorageUnit", back_populates="tenant")

# Create a session factory
SessionLocal = sessionmaker(bind=engine)
