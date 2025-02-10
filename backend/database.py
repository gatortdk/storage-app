import os
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Database URL from environment variables (default to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./storage.db")

# Database Connection
try:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database connection established successfully.")
except Exception as e:
    logger.error(f"Database connection failed: {e}")

# Tenant Model
class Tenant(Base):
    __tablename__ = "tenants"
    tenant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Added length constraint
    contact = Column(String(255), nullable=False)  # Added length constraint
    move_in_date = Column(String, nullable=True)  # Can be converted to Date if needed
    lease_end_date = Column(String, nullable=True)  # Can be converted to Date if needed
    payment_status = Column(String(50), nullable=False)  # Added length constraint

# Storage Unit Model
class StorageUnit(Base):
    __tablename__ = "storage_units"
    unit_id = Column(Integer, primary_key=True, index=True)
    size = Column(String(100), nullable=False)  # Added length constraint
    price = Column(Float, nullable=False)
    occupied = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, default=False)  # Soft delete flag
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id", ondelete="SET NULL"), nullable=True)
    tenant = relationship("Tenant", back_populates="units")

Tenant.units = relationship("StorageUnit", back_populates="tenant")

# Create Tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"Table creation failed: {e}")

