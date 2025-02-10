from sqlalchemy.orm import Session
from backend.models import StorageUnit, Tenant

# CREATE Operations
def create_unit(db: Session, size: str, price: float, occupied: bool = False, tenant_id: int = None):
    """Adds a new storage unit."""
    new_unit = StorageUnit(size=size, price=price, occupied=occupied, tenant_id=tenant_id)
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

def create_tenant(db: Session, name: str, contact: str, move_in_date: str = None, lease_end_date: str = None, payment_status: str = "Pending"):
    """Adds a new tenant."""
    new_tenant = Tenant(name=name, contact=contact, move_in_date=move_in_date, lease_end_date=lease_end_date, payment_status=payment_status)
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return new_tenant

# READ Operations
def get_units(db: Session):
    """Retrieves all storage units excluding soft-deleted ones."""
    return db.query(StorageUnit).filter(StorageUnit.is_deleted == False).all()

def get_tenants(db: Session):
    """Retrieves all tenants."""
    return db.query(Tenant).all()

def get_unit_by_id(db: Session, unit_id: int):
    """Fetch a specific unit by ID, excluding soft-deleted units."""
    return db.query(StorageUnit).filter(StorageUnit.unit_id == unit_id, StorageUnit.is_deleted == False).first()

def get_tenant_by_id(db: Session, tenant_id: int):
    """Fetch a specific tenant by ID."""
    return db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()

# UPDATE Operations
def update_unit_status(db: Session, unit_id: int, new_status: bool):
    """Updates the occupancy status of a storage unit."""
    unit = db.query(StorageUnit).filter(StorageUnit.unit_id == unit_id, StorageUnit.is_deleted == False).first()
    if unit:
        unit.occupied = new_status
        db.commit()
        db.refresh(unit)
    return unit

# DELETE Operations
def delete_unit(db: Session, unit_id: int):
    """Soft deletes a storage unit."""
    unit = db.query(StorageUnit).filter(StorageUnit.unit_id == unit_id).first()
    if unit:
        unit.is_deleted = True
        db.commit()
    return unit

def delete_tenant(db: Session, tenant_id: int):
    """Deletes a tenant."""
    tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if tenant:
        db.delete(tenant)
        db.commit()
    return tenant
