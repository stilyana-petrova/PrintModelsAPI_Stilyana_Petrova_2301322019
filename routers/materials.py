from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models.schemas import MaterialCreate, MaterialUpdate, MaterialResponse
from services.material_service import MaterialService


router = APIRouter(prefix="/materials", tags=["Materials"])


@router.get("/", response_model=list[MaterialResponse])
def get_all_materials(db_session: Session = Depends(get_db)):
    return MaterialService.get_all(db_session)


@router.get("/{material_id}", response_model=MaterialResponse)
def get_material(material_id: int, db_session: Session = Depends(get_db)):
    return MaterialService.get_by_id(db_session, material_id)


@router.post("/", response_model=MaterialResponse, status_code=201)
def create_material(data: MaterialCreate, db_session: Session = Depends(get_db)):
    return MaterialService.create(db_session, data)


@router.put("/{material_id}", response_model=MaterialResponse)
def update_material(
    material_id: int,
    data: MaterialUpdate,
    db_session: Session = Depends(get_db)
):
    return MaterialService.update(db_session, material_id, data)


@router.delete("/{material_id}")
def delete_material(material_id: int, db_session: Session = Depends(get_db)):
    return MaterialService.delete(db_session, material_id)