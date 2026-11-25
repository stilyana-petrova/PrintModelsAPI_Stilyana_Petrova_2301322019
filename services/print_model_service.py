from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from db.models import PrintModel, Designer, Category
from models.schemas import PrintModelCreate, PrintModelUpdate


class PrintModelService:

    @staticmethod
    def get_all(
        db_session: Session,
        name: str | None = None,
        category_id: int | None = None,
        max_print_time: int | None = None
    ):
        stmt = select(PrintModel).options(
            joinedload(PrintModel.designer),
            joinedload(PrintModel.category)
        )

        if name:
            stmt = stmt.where(
                func.lower(PrintModel.name).contains(name.strip().lower())
            )

        if category_id is not None:
            stmt = stmt.where(PrintModel.category_id == category_id)

        if max_print_time is not None:
            stmt = stmt.where(PrintModel.print_time <= max_print_time)

        return db_session.scalars(stmt).unique().all()

    @staticmethod
    def get_by_id(db_session: Session, print_model_id: int):
        stmt = (
            select(PrintModel)
            .options(
                joinedload(PrintModel.designer),
                joinedload(PrintModel.category)
            )
            .where(PrintModel.id == print_model_id)
        )

        print_model = db_session.scalars(stmt).first()

        if print_model is None:
            raise HTTPException(
                status_code=404,
                detail="Print model not found"
            )

        return print_model

    @staticmethod
    def create(db_session: Session, data: PrintModelCreate):
        designer = db_session.get(Designer, data.designer_id)

        if designer is None:
            raise HTTPException(status_code=404, detail="Designer not found")

        if data.category_id is not None:
            category = db_session.get(Category, data.category_id)

            if category is None:
                raise HTTPException(status_code=404, detail="Category not found")

        name = data.name.strip()

        stmt = select(PrintModel).where(
            PrintModel.designer_id == data.designer_id,
            func.lower(func.trim(PrintModel.name)) == name.lower()
        )

        if db_session.scalar(stmt):
            raise HTTPException(
                status_code=409,
                detail="Designer already has a print model with this name"
            )

        print_model = PrintModel(
            name=name,
            instructions=data.instructions.strip(),
            print_time=data.print_time,
            copies=data.copies,
            difficulty=data.difficulty,
            designer_id=data.designer_id,
            category_id=data.category_id
        )

        db_session.add(print_model)
        db_session.commit()
        db_session.refresh(print_model)

        return print_model

    @staticmethod
    def update(
        db_session: Session,
        print_model_id: int,
        data: PrintModelUpdate
    ):
        print_model = PrintModelService.get_by_id(
            db_session,
            print_model_id
        )

        designer = db_session.get(Designer, data.designer_id)

        if designer is None:
            raise HTTPException(status_code=404, detail="Designer not found")

        if data.category_id is not None:
            category = db_session.get(Category, data.category_id)

            if category is None:
                raise HTTPException(status_code=404, detail="Category not found")

        name = data.name.strip()

        stmt = select(PrintModel).where(
            PrintModel.designer_id == data.designer_id,
            func.lower(func.trim(PrintModel.name)) == name.lower(),
            PrintModel.id != print_model_id
        )

        if db_session.scalar(stmt):
            raise HTTPException(
                status_code=409,
                detail="Designer already has a print model with this name"
            )

        print_model.name = name
        print_model.instructions = data.instructions.strip()
        print_model.print_time = data.print_time
        print_model.copies = data.copies
        print_model.difficulty = data.difficulty
        print_model.designer_id = data.designer_id
        print_model.category_id = data.category_id

        db_session.commit()
        db_session.refresh(print_model)

        return print_model

    @staticmethod
    def delete(db_session: Session, print_model_id: int):
        print_model = PrintModelService.get_by_id(
            db_session,
            print_model_id
        )

        db_session.delete(print_model)
        db_session.commit()

        return {"message": "Print model deleted successfully"}