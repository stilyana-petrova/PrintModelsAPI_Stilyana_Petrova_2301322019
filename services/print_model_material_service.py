from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from db.models import PrintModel, Material, PrintModelMaterial


class PrintModelMaterialService:

    @staticmethod
    def get_all(db_session: Session, print_model_id: int):
        print_model = db_session.get(PrintModel, print_model_id)

        if print_model is None:
            raise HTTPException(status_code=404, detail="Print model not found")

        stmt = (
            select(PrintModelMaterial)
            .options(joinedload(PrintModelMaterial.material))
            .where(PrintModelMaterial.print_model_id == print_model_id)
        )

        return db_session.scalars(stmt).all()

    @staticmethod
    def add(db_session: Session, print_model_id: int, data):
        print_model = db_session.get(PrintModel, print_model_id)

        if print_model is None:
            raise HTTPException(status_code=404, detail="Print model not found")

        material = db_session.get(Material, data.material_id)

        if material is None:
            raise HTTPException(status_code=404, detail="Material not found")

        existing = db_session.get(
            PrintModelMaterial,
            (print_model_id, data.material_id)
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Material is already associated with this print model"
            )

        association = PrintModelMaterial(
            print_model_id=print_model_id,
            material_id=data.material_id,
            quantity=data.quantity,
            unit=data.unit
        )

        db_session.add(association)
        db_session.commit()
        db_session.refresh(association)

        return association

    @staticmethod
    def update(
        db_session: Session,
        print_model_id: int,
        material_id: int,
        data
    ):
        print_model = db_session.get(PrintModel, print_model_id)

        if print_model is None:
            raise HTTPException(status_code=404, detail="Print model not found")

        association = db_session.get(
            PrintModelMaterial,
            (print_model_id, material_id)
        )

        if association is None:
            raise HTTPException(
                status_code=404,
                detail="Material association not found"
            )

        association.quantity = data.quantity
        association.unit = data.unit

        db_session.commit()
        db_session.refresh(association)

        return association

    @staticmethod
    def delete(db_session: Session, print_model_id: int, material_id: int):
        print_model = db_session.get(PrintModel, print_model_id)

        if print_model is None:
            raise HTTPException(status_code=404, detail="Print model not found")

        association = db_session.get(
            PrintModelMaterial,
            (print_model_id, material_id)
        )

        if association is None:
            raise HTTPException(
                status_code=404,
                detail="Material association not found"
            )

        db_session.delete(association)
        db_session.commit()

        return {"message": "Material association deleted successfully"}

    @staticmethod
    def get_for_copies(
        db_session: Session,
        print_model_id: int,
        requested_copies: int
    ):
        print_model = db_session.get(PrintModel, print_model_id)

        if print_model is None:
            raise HTTPException(status_code=404, detail="Print model not found")

        stmt = (
            select(PrintModelMaterial)
            .options(joinedload(PrintModelMaterial.material))
            .where(PrintModelMaterial.print_model_id == print_model_id)
        )

        associations = db_session.scalars(stmt).all()

        materials = []

        for association in associations:
            calculated_quantity = (
                association.quantity * requested_copies / print_model.copies
            )

            materials.append({
                "material_id": association.material_id,
                "material_name": association.material.name,
                "quantity": round(calculated_quantity, 2),
                "unit": association.unit
            })

        return {
            "print_model_id": print_model.id,
            "print_model_name": print_model.name,
            "requested_copies": requested_copies,
            "materials": materials
        }