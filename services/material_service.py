from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.models import Material
from models.schemas import MaterialCreate, MaterialUpdate


class MaterialService:

    @staticmethod
    def get_all(db_session: Session):
        stmt = select(Material)
        return db_session.scalars(stmt).all()

    @staticmethod
    def get_by_id(db_session: Session, material_id: int):
        material = db_session.get(Material, material_id)

        if material is None:
            raise HTTPException(status_code=404, detail="Material not found")

        return material

    @staticmethod
    def create(db_session: Session, material_data: MaterialCreate):
        name = material_data.name.strip()

        stmt = select(Material).where(
            func.lower(func.trim(Material.name)) == name.lower()
        )

        if db_session.scalar(stmt):
            raise HTTPException(status_code=409, detail="Material already exists")

        material = Material(name=name)
        db_session.add(material)
        db_session.commit()
        db_session.refresh(material)

        return material

    @staticmethod
    def update(db_session: Session, material_id: int, material_data: MaterialUpdate):
        material = MaterialService.get_by_id(db_session, material_id)
        name = material_data.name.strip()

        stmt = select(Material).where(
            func.lower(func.trim(Material.name)) == name.lower(),
            Material.id != material_id
        )

        if db_session.scalar(stmt):
            raise HTTPException(status_code=409, detail="Material already exists")

        material.name = name
        db_session.commit()
        db_session.refresh(material)

        return material

    @staticmethod
    def delete(db_session: Session, material_id: int):
        material = MaterialService.get_by_id(db_session, material_id)

        if material.print_model_associations:
            raise HTTPException(
                status_code=409,
                detail="Cannot delete material used by print models"
            )

        db_session.delete(material)
        db_session.commit()

        return {"message": "Material deleted successfully"}