from sqlalchemy.orm import Session
from models import Unit, Tenant

# CREATE Operations
def create_unit(db: Session, unit_number: str, status: str = "available"):
    """Adds a new storage unit."""
    new_unit = Unit(unit_number=unit_number, status=status)
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

def create_tenant(db: Session, name: str, email: str, phone: str = None):
    """Adds a new tenant."""
    new_tenant = Tenant(name=name, email=email, phone=phone)
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return new_tenant

# READ Operations
def get_units(db: Session):
    """Retrieves all storage units."""
    return db.query(Unit).all()

def get_tenants(db: Session):
    """Retrieves all tenants."""
    return db.query(Tenant).all()

def get_unit_by_id(db: Session, unit_id: int):
    """Fetch a specific unit by ID."""
    return db.query(Unit).filter(Unit.id == unit_id).first()

def get_tenant_by_id(db: Session, tenant_id: int):
    """Fetch a specific tenant by ID."""
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()

# UPDATE Operations
def update_unit_status(db: Session, unit_id: int, new_status: str):
    """Updates the status of a storage unit."""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if unit:
        unit.status = new_status
        db.commit()
        db.refresh(unit)
    return unit

# DELETE Operations
def delete_unit(db: Session, unit_id: int):
    """Deletes a storage unit."""
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if unit:
        db.delete(unit)
        db.commit()
    return unit

def delete_tenant(db: Session, tenant_id: int):
    """Deletes a tenant."""
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        db.delete(tenant)
        db.commit()
    return tenant
