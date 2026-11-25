from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.schemas import (
    PrintModelMaterialCreate,
    PrintModelMaterialUpdate,
    PrintModelMaterialResponse,
    PrintModelMaterialsForCopiesResponse
)
from services.print_model_material_service import PrintModelMaterialService


router = APIRouter(
    prefix="/print-models/{print_model_id}/materials",
    tags=["Print Model Materials"]
)


@router.get("/", response_model=list[PrintModelMaterialResponse])
def get_materials(
    print_model_id: int,
    db_session: Session = Depends(get_db)
):
    return PrintModelMaterialService.get_all(db_session, print_model_id)


@router.post(
    "/",
    response_model=PrintModelMaterialResponse,
    status_code=status.HTTP_201_CREATED
)
def add_material(
    print_model_id: int,
    data: PrintModelMaterialCreate,
    db_session: Session = Depends(get_db)
):
    return PrintModelMaterialService.add(
        db_session,
        print_model_id,
        data
    )


@router.put(
    "/{material_id}",
    response_model=PrintModelMaterialResponse
)
def update_material(
    print_model_id: int,
    material_id: int,
    data: PrintModelMaterialUpdate,
    db_session: Session = Depends(get_db)
):
    return PrintModelMaterialService.update(
        db_session,
        print_model_id,
        material_id,
        data
    )


@router.delete("/{material_id}")
def delete_material(
    print_model_id: int,
    material_id: int,
    db_session: Session = Depends(get_db)
):
    return PrintModelMaterialService.delete(
        db_session,
        print_model_id,
        material_id
    )


@router.get(
    "/for-copies",
    response_model=PrintModelMaterialsForCopiesResponse
)
def get_materials_for_copies(
    print_model_id: int,
    copies: int = Query(gt=0, le=69),
    db_session: Session = Depends(get_db)
):
    return PrintModelMaterialService.get_for_copies(
        db_session,
        print_model_id,
        copies
    )