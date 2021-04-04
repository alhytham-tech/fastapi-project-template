# {{cookiecutter.project_name}}

This is a backend server application power with Python and [FastAPI](https://fastapi.tiangolo.com).

## Local Development

### Install the dependencies

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
```bash
venv/Scripts/activate
```
Change directory to `app/` folder
```bash
cd app/
```
Install dependencies
```bash
pip install -r requirements.txt
```
Ensure that your database config in `.env` is correct, then run [alembic](https://alembic.sqlalchemy.org) migrations
```bash
alembic upgrade head
```
Initialise database with User & RBAC tables and initial entries
```bash
python initial_data.py
```

### Start the development server
Run without `--reload` flag if you want to disable hot module reloading (HMR)
```bash
uvicorn main:app --reload
```