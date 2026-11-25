from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.models import Category
from models.schemas import CategoryCreate, CategoryUpdate


class CategoryService:

    @staticmethod
    def get_all(db_session: Session):
        stmt = select(Category)
        return db_session.scalars(stmt).all()

    @staticmethod
    def get_by_id(db_session: Session, category_id: int):
        category = db_session.get(Category, category_id)

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

        return category

    @staticmethod
    def create(db_session: Session, category_data: CategoryCreate):
        name = category_data.name.strip()

        stmt = select(Category).where(
            func.lower(func.trim(Category.name)) == name.lower()
        )

        if db_session.scalar(stmt):
            raise HTTPException(status_code=409, detail="Category already exists")

        category = Category(name=name)
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        return category

    @staticmethod
    def update(db_session: Session, category_id: int, category_data: CategoryUpdate):
        category = CategoryService.get_by_id(db_session, category_id)
        name = category_data.name.strip()

        stmt = select(Category).where(
            func.lower(func.trim(Category.name)) == name.lower(),
            Category.id != category_id
        )

        if db_session.scalar(stmt):
            raise HTTPException(status_code=409, detail="Category already exists")

        category.name = name
        db_session.commit()
        db_session.refresh(category)

        return category

    @staticmethod
    def delete(db_session: Session, category_id: int):
        category = CategoryService.get_by_id(db_session, category_id)

        db_session.delete(category)
        db_session.commit()

        return {"message": "Category deleted successfully"}