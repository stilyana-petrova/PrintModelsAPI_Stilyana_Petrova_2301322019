from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models.schemas import (
    DesignerCreate,
    DesignerUpdate,
    DesignerResponse
)
from services.designer_service import DesignerService


router = APIRouter(
    prefix="/designers",
    tags=["Designers"]
)


@router.get("/", response_model=list[DesignerResponse])
def get_all_designers(db_session: Session = Depends(get_db)):
    return DesignerService.get_all(db_session)

@router.get("/{designer_id}/print-models")
def get_designer_print_models(
    designer_id: int,
    db_session: Session = Depends(get_db)
):
    return DesignerService.get_print_models(db_session, designer_id)

@router.get("/{designer_id}", response_model=DesignerResponse)
def get_designer_by_id(
    designer_id: int,
    db_session: Session = Depends(get_db)
):
    return DesignerService.get_by_id(db_session, designer_id)


@router.post("/", response_model=DesignerResponse, status_code=201)
def create_designer(
    designer_data: DesignerCreate,
    db_session: Session = Depends(get_db)
):
    return DesignerService.create(db_session, designer_data)


@router.put("/{designer_id}", response_model=DesignerResponse)
def update_designer(
    designer_id: int,
    designer_data: DesignerUpdate,
    db_session: Session = Depends(get_db)
):
    return DesignerService.update(
        db_session,
        designer_id,
        designer_data
    )


@router.delete("/{designer_id}")
def delete_designer(
    designer_id: int,
    db_session: Session = Depends(get_db)
):
    return DesignerService.delete(db_session, designer_id)