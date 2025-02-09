from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import Unit, Tenant  # Ensure correct import from models.py
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for input validation
class StorageUnitCreate(BaseModel):
    unit_id: int
    size: str
    price: float
    occupied: bool
    tenant_id: int | None = None

class StorageUnitUpdate(BaseModel):
    size: str | None = None
    price: float | None = None
    occupied: bool | None = None
    tenant_id: int | None = None

# Ensure `POST /units/` endpoint exists
@app.post("/units/")
def create_unit(unit: StorageUnitCreate, db: Session = Depends(get_db)):
    new_unit = StorageUnit(
        unit_id=unit.unit_id,
        size=unit.size,
        price=unit.price,
        occupied=unit.occupied,
        tenant_id=unit.tenant_id
    )
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

@app.get("/units/")
def get_units(db: Session = Depends(get_db)):
    units = db.query(StorageUnit).all()
    if not units:
        raise HTTPException(status_code=404, detail="No storage units found")
    
    return [
        {
            "unit_id": unit.unit_id,
            "size": unit.size,
            "price": unit.price,
            "occupied": unit.occupied,
            "tenant": {
                "tenant_id": unit.tenant.tenant_id,
                "name": unit.tenant.name,
                "contact": unit.tenant.contact,
                "move_in_date": unit.tenant.move_in_date,
                "lease_end_date": unit.tenant.lease_end_date,
                "payment_status": unit.tenant.payment_status
            } if unit.tenant else None
        }
        for unit in units
    ]

@app.put("/units/{unit_id}")
def update_unit(unit_id: int, unit_data: StorageUnitUpdate, db: Session = Depends(get_db)):
    unit = db.query(StorageUnit).filter(StorageUnit.unit_id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Storage unit not found")
    
    if unit_data.size is not None:
        unit.size = unit_data.size
    if unit_data.price is not None:
        unit.price = unit_data.price
    if unit_data.occupied is not None:
        unit.occupied = unit_data.occupied
    if unit_data.tenant_id is not None:
        unit.tenant_id = unit_data.tenant_id
    
    db.commit()
    db.refresh(unit)
    return unit

@app.delete("/units/{unit_id}")
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(StorageUnit).filter(StorageUnit.unit_id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Storage unit not found")
    
    db.delete(unit)
    db.commit()
    return {"message": "Unit deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "API is running with CORS enabled."}

