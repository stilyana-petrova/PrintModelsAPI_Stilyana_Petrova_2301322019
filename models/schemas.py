from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Literal


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# DESIGNER

class DesignerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class DesignerUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class DesignerResponse(BaseSchema):
    id: int
    name: str
    email: EmailStr


# CATEGORY

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class CategoryUpdate(CategoryCreate):
    pass


class CategoryResponse(BaseSchema):
    id: int
    name: str


# MATERIAL

class MaterialCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class MaterialUpdate(MaterialCreate):
    pass


class MaterialResponse(BaseSchema):
    id: int
    name: str



class PrintModelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    instructions: str = Field(min_length=1)
    print_time: int = Field(gt=0)
    copies: int = Field(gt=0)
    designer_id: int = Field(gt=0)
    category_id: int | None = None
    difficulty: Literal["easy", "medium", "hard"] = "medium"

    @field_validator("name", "instructions")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value


class PrintModelUpdate(PrintModelCreate):
    pass


class PrintModelResponse(BaseSchema):
    id: int
    name: str
    instructions: str
    print_time: int
    copies: int
    designer_id: int
    category_id: int | None
    difficulty: str



class PrintModelMaterialCreate(BaseModel):
    material_id: int = Field(gt=0)
    quantity: float = Field(gt=0)
    unit: Literal["g", "m", "ml"]


class PrintModelMaterialUpdate(BaseModel):
    quantity: float = Field(gt=0)
    unit: Literal["g", "m", "ml"]


class PrintModelMaterialResponse(BaseSchema):
    material_id: int
    material: MaterialResponse
    quantity: float
    unit: Literal["g", "m", "ml"]



class MaterialForCopiesResponse(BaseModel):
    material_id: int
    material_name: str
    quantity: float
    unit: str


class PrintModelForCopiesResponse(BaseModel):
    print_model_id: int
    print_model_name: str
    requested_copies: int
    materials: list[MaterialForCopiesResponse]

class MaterialQuantityForCopiesResponse(BaseModel):
    material_id: int
    material_name: str
    quantity: float
    unit: str


class PrintModelMaterialsForCopiesResponse(BaseModel):
    print_model_id: int
    print_model_name: str
    requested_copies: int
    materials: list[MaterialQuantityForCopiesResponse]