from fastapi import APIRouter



users_router = APIRouter(
    prefix='/users',
    tags=['User']
)
