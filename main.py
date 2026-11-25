from fastapi import FastAPI
from routers.designers import router as designers_router
from routers.categories import router as categories_router
from routers.materials import router as materials_router
from routers.print_models import router as print_models_router
from routers.print_model_materials import router as print_model_materials_router

app = FastAPI(
    title="Print Models API",
    description="REST API for a 3D printing models catalog",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Welcome to Print Models API!"}


app.include_router(designers_router)
app.include_router(categories_router)
app.include_router(materials_router)
app.include_router(print_models_router)
app.include_router(print_model_materials_router)