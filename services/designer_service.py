from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.models import Designer, PrintModel
from models.schemas import DesignerCreate, DesignerUpdate



class DesignerService:

    @staticmethod
    def get_print_models(db_session: Session, designer_id: int):
        designer = db_session.get(Designer, designer_id)

        if designer is None:
            raise HTTPException(status_code=404, detail="Designer not found")

        stmt = select(PrintModel).where(
            PrintModel.designer_id == designer_id
        )

        return db_session.scalars(stmt).all()

    @staticmethod
    def get_all(db_session: Session):
        stmt = select(Designer)
        return db_session.scalars(stmt).all()

    @staticmethod
    def get_by_id(db_session: Session, designer_id: int):
        designer = db_session.get(Designer, designer_id)

        if designer is None:
            raise HTTPException(
                status_code=404,
                detail="Designer not found"
            )

        return designer

    @staticmethod
    def create(db_session: Session, designer_data: DesignerCreate):
        email = str(designer_data.email).lower()

        stmt = select(Designer).where(Designer.email == email)
        existing = db_session.scalar(stmt)

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Designer with this email already exists"
            )

        designer = Designer(
            name=designer_data.name.strip(),
            email=email
        )

        db_session.add(designer)
        db_session.commit()
        db_session.refresh(designer)

        return designer

    @staticmethod
    def update(
        db_session: Session,
        designer_id: int,
        designer_data: DesignerUpdate
    ):
        designer = DesignerService.get_by_id(db_session, designer_id)

        email = str(designer_data.email).lower()

        stmt = select(Designer).where(
            Designer.email == email,
            Designer.id != designer_id
        )

        if db_session.scalar(stmt):
            raise HTTPException(
                status_code=409,
                detail="Designer with this email already exists"
            )

        designer.name = designer_data.name.strip()
        designer.email = email

        db_session.commit()
        db_session.refresh(designer)

        return designer

    @staticmethod
    def delete(db_session: Session, designer_id: int):
        designer = DesignerService.get_by_id(db_session, designer_id)

        if designer.print_models:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete designer with existing print models"
            )

        db_session.delete(designer)
        db_session.commit()

        return {"message": "Designer deleted successfully"}