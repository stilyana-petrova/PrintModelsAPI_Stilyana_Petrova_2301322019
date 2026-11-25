from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.schemas import (
    PrintModelCreate,
    PrintModelUpdate,
    PrintModelResponse
)
from services.print_model_service import PrintModelService


router = APIRouter(prefix="/print-models", tags=["Print Models"])


@router.get("/", response_model=list[PrintModelResponse])
def get_all_print_models(
    name: str | None = None,
    category_id: int | None = None,
    max_print_time: int | None = Query(default=None, gt=0),
    db_session: Session = Depends(get_db)
):
    return PrintModelService.get_all(
        db_session,
        name,
        category_id,
        max_print_time
    )


@router.get("/{print_model_id}", response_model=PrintModelResponse)
def get_print_model(
    print_model_id: int,
    db_session: Session = Depends(get_db)
):
    return PrintModelService.get_by_id(db_session, print_model_id)


@router.post("/", response_model=PrintModelResponse, status_code=201)
def create_print_model(
    data: PrintModelCreate,
    db_session: Session = Depends(get_db)
):
    return PrintModelService.create(db_session, data)


@router.put("/{print_model_id}", response_model=PrintModelResponse)
def update_print_model(
    print_model_id: int,
    data: PrintModelUpdate,
    db_session: Session = Depends(get_db)
):
    return PrintModelService.update(
        db_session,
        print_model_id,
        data
    )


@router.delete("/{print_model_id}")
def delete_print_model(
    print_model_id: int,
    db_session: Session = Depends(get_db)
):
    return PrintModelService.delete(db_session, print_model_id)