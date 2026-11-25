# Web server programming course project
# PrintModelsAPI

REST API for managing 3D printing models, designers, categories, and materials.

## Project Description

PrintModelsAPI is a RESTful web application developed with FastAPI and SQLAlchemy. It provides functionality for managing 3D printing models and their related information.

Each print model belongs to a designer and can optionally belong to a category. Models can also be associated with multiple materials, with each association storing the required quantity and measurement unit.

The API supports CRUD operations, filtering, material management, and calculation of material quantities for a requested number of copies.

## Technologies

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Alembic

## Project Structure

```text
PrintModelsAPI/
│
├── db/
│   ├── database.py
│   └── models.py
│
├── models/
│   └── schemas.py
│
├── routers/
│   ├── designers.py
│   ├── categories.py
│   ├── materials.py
│   ├── print_models.py
│   └── print_model_materials.py
│
├── services/
│   ├── designer_service.py
│   ├── category_service.py
│   ├── material_service.py
│   ├── print_model_service.py
│   └── print_model_material_service.py
│
├── migrations/
│   └── versions/
│
├── alembic.ini
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd PrintModelsAPI
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

**Windows:**

```bash
venv\Scripts\activate
```

5. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

The project uses SQLite as its database and Alembic for database migrations.

To apply all database migrations, execute:

```bash
alembic upgrade head
```

This creates the database schema and applies the required changes.

## Running the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

These interfaces allow users to explore and test the available endpoints.

## Main Features

### Entity Management

Full CRUD operations for:

- Designers
- Categories
- Materials
- Print Models

### Print Model Management

- Assign a designer to each print model.
- Optionally assign a category.
- Set print time and number of copies.
- Define model difficulty: `easy`, `medium`, or `hard`.
- Filter models by name, category, and maximum print time.

### Material Management

- Associate existing materials with print models.
- Specify material quantity and measurement unit (`g`, `m`, `ml`).
- Update or remove material associations.
- Retrieve all materials associated with a print model.
- Calculate proportional material quantities for a requested number of copies (maximum 69).

## Database Migrations

Database schema changes are managed using Alembic.

The project includes two migrations:

1. **Initial database schema** – creates the core database tables and relationships.
2. **Add difficulty to print models** – adds the difficulty field to print models.

## Author

**Stilyana Petrova**

Software Engineering Student

