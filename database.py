
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "sqlite:///./storage.db"

# Database Connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Tenant Model
class Tenant(Base):
    __tablename__ = "tenants"
    tenant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    move_in_date = Column(String, nullable=True)
    lease_end_date = Column(String, nullable=True)
    payment_status = Column(String, nullable=False)

# Storage Unit Model
class StorageUnit(Base):
    __tablename__ = "storage_units"
    unit_id = Column(Integer, primary_key=True, index=True)
    size = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    occupied = Column(Boolean, nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=True)
    tenant = relationship("Tenant", back_populates="units")

Tenant.units = relationship("StorageUnit", back_populates="tenant")

# Create Tables
Base.metadata.create_all(bind=engine)
