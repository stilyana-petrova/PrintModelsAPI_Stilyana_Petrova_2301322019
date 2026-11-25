from sqlalchemy import String
from sqlalchemy import (
    String,
    ForeignKey,
    Text,
    CheckConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Designer(Base):
    __tablename__ = "designers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    print_models: Mapped[list["PrintModel"]] = relationship(
        back_populates="designer"
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    print_models: Mapped[list["PrintModel"]] = relationship(
        back_populates="category"
    )


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    print_model_associations: Mapped[list["PrintModelMaterial"]] = relationship(
        back_populates="material"
    )

class PrintModel(Base):
    __tablename__ = "print_models"

    __table_args__ = (
        CheckConstraint(
            "print_time > 0",
            name="ck_print_models_print_time_positive"
        ),
        CheckConstraint(
            "copies > 0",
            name="ck_print_models_copies_positive"
        ),

    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    instructions: Mapped[str] = mapped_column(Text)
    print_time: Mapped[int] = mapped_column()
    copies: Mapped[int] = mapped_column()


    designer_id: Mapped[int] = mapped_column(ForeignKey("designers.id"))
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )

    designer: Mapped["Designer"] = relationship(
        back_populates="print_models"
    )
    category: Mapped["Category | None"] = relationship(
        back_populates="print_models"
    )

    material_associations: Mapped[list["PrintModelMaterial"]] = relationship(
        back_populates="print_model",
        cascade="all, delete-orphan"
    )


class PrintModelMaterial(Base):
    __tablename__ = "print_model_materials"

    __table_args__ = (
        CheckConstraint("quantity > 0"),
        CheckConstraint("unit IN ('g', 'm', 'ml')"),

    )

    print_model_id: Mapped[int] = mapped_column(
        ForeignKey("print_models.id"),
        primary_key=True
    )
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id"),
        primary_key=True
    )
    quantity: Mapped[float] = mapped_column()
    unit: Mapped[str] = mapped_column(String(2))

    print_model: Mapped["PrintModel"] = relationship(
        back_populates="material_associations"
    )
    material: Mapped["Material"] = relationship(
        back_populates="print_model_associations"
    )