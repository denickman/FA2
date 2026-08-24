from fastapi import APIRouter, HTTPException
from routers.dependencies import db_dependency, get_db


router = APIRouter()

@router.get('/auth/')
async def get_user():
    return {'user': 'authenticated'}