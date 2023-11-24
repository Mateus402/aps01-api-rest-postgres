from fastapi import APIRouter, HTTPException

from src.models.provas_model import Provas
from src.config.database import get_session
from sqlalchemy import select, and_
from src.models.resultados_model import Resultados

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


@provas_router.delete("/{id}")
def delete_prova(id: int):
    with get_session() as session:
        # Verifica se a prova existe
        prova_existente = session.exec(select(Provas).where(Provas.id == id)).first()
        if not prova_existente:
            raise HTTPException(status_code=404, detail="Prova não encontrada")

        # Verifica se há resultados associados à prova
        resultados_associados = session.exec(select(Resultados).where(Resultados.prova_id == id)).all()
        if resultados_associados:
            raise HTTPException(status_code=400, detail="Não é possível excluir a prova pois há resultados associados")

        # Exclui a prova
        session.delete(prova_existente)
        session.commit()

        return {"message": "Prova excluída com sucesso"}
