# from fastapi import APIRouter
# from sqlmodel import select

# from src.config.database import get_session
# from src.models.provas_model import Provas
# from src.models.resultados_model import Resultados

# resultados_router = APIRouter(prefix="/resultados")


# @resultados_router.post("")
# def cria_prova(resultado: Resultados):
#     with get_session() as session:
        
#         statement = select(Provas).where(Provas.id == resultado.prova_id)
#         prova = session.exec(statement).first()
       
#         resultado.nota = 10

#         session.add(resultado)
#         session.commit()
#         session.refresh(resultado)
#         return resultado

# resultados_provas_routes.py

# resultados_provas_routes.py
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.config.database import get_session
from src.models.provas_model import Provas
from src.models.resultados_model import Resultados

resultados_provas_router = APIRouter(prefix="/resultados_provas")

@resultados_provas_router.post("")
def cria_resultado_prova(resultado_prova: Resultados):
    with get_session() as session:

        # Verifica se a prova existe
        statement_prova = select(Provas).where(Provas.id == resultado_prova.prova_id)
        prova_existente = session.exec(statement_prova).first()
        if not prova_existente:
            raise HTTPException(status_code=404, detail="Prova não cadastrada")

        # Correção automática
        nota = 0
        respostas_corretas = [prova_existente.q1, prova_existente.q2, prova_existente.q3,
                              prova_existente.q4, prova_existente.q5, prova_existente.q6,
                              prova_existente.q7, prova_existente.q8, prova_existente.q9,
                              prova_existente.q10]

        for i in range(10):
            if getattr(resultado_prova, f"q{i + 1}") == respostas_corretas[i]:
                nota += 1

        resultado_prova.nota = nota

        # Insere na tabela resultados_provas
        session.add(resultado_prova)
        session.commit()
        session.refresh(resultado_prova)

        return resultado_prova


