from fastapi import APIRouter, HTTPException

from src.models.provas_model import Provas
from src.config.database import get_session
from sqlalchemy import select, and_

provas_router = APIRouter(prefix="/provas")

@provas_router.post("")
def cria_prova(prova: Provas):
    with get_session() as session:
        
        statement = select(Provas).where(
            and_(Provas.descricao == prova.descricao, Provas.data_prova == prova.data_prova)
        )
        prova_existente = session.exec(statement).first()
        if prova_existente:
            raise HTTPException(status_code=400, detail="Prova já cadastrada.")
        
        session.add(prova)
        session.commit()
        session.refresh(prova)
        
        return prova
