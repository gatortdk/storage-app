from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import StorageUnit, Tenant
from backend.crud import create_unit, create_tenant, get_units, get_tenants, get_unit_by_id, get_tenant_by_id, update_unit_status, delete_unit, delete_tenant
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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        db.close()

# Pydantic models for input validation
class StorageUnitCreate(BaseModel):
    size: str
    price: float
    occupied: bool = False
    tenant_id: int | None = None

@app.post("/units/")
def create_unit_api(unit: StorageUnitCreate, db: Session = Depends(get_db)):
    return create_unit(db, size=unit.size, price=unit.price, occupied=unit.occupied, tenant_id=unit.tenant_id)

@app.get("/units/")
def get_units_api(db: Session = Depends(get_db)):
    return get_units(db)

@app.get("/units/{unit_id}")
def get_unit_api(unit_id: int, db: Session = Depends(get_db)):
    unit = get_unit_by_id(db, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Storage unit not found")
    return unit

@app.put("/units/{unit_id}/status")
def update_unit_status_api(unit_id: int, new_status: bool, db: Session = Depends(get_db)):
    return update_unit_status(db, unit_id, new_status)

@app.delete("/units/{unit_id}")
def delete_unit_api(unit_id: int, db: Session = Depends(get_db)):
    return delete_unit(db, unit_id)

@app.get("/")
def read_root():
    return {"message": "API is running with CORS enabled."}
