from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from models.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from services.category_service import CategoryService


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
def get_all_categories(db_session: Session = Depends(get_db)):
    return CategoryService.get_all(db_session)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db_session: Session = Depends(get_db)):
    return CategoryService.get_by_id(db_session, category_id)


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, db_session: Session = Depends(get_db)):
    return CategoryService.create(db_session, data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db_session: Session = Depends(get_db)
):
    return CategoryService.update(db_session, category_id, data)


@router.delete("/{category_id}")
def delete_category(category_id: int, db_session: Session = Depends(get_db)):
    return CategoryService.delete(db_session, category_id)