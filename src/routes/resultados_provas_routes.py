from fastapi import APIRouter, HTTPException
from sqlmodel import select
from src.config.database import get_session
from src.models.provas_model import Provas
from src.models.resultados_model import Resultados

resultados_provas_router = APIRouter(prefix="/resultados_provas")

@resultados_provas_router.post("")
def cria_resultado_prova(resultado: Resultados):
    with get_session() as session:
        
        # Verificar se a prova com o ID fornecido existe
        statement_prova = select(Provas).where(Provas.id == resultado.prova_id)
        prova = session.exec(statement_prova).first()
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não cadastrada")

        # Simular correção automática comparando respostas com gabarito
        gabarito = [
            prova.q1, prova.q2, prova.q3, prova.q4, prova.q5,
            prova.q6, prova.q7, prova.q8, prova.q9, prova.q10
        ]
        nota_final = 0
        for questao, resposta_aluno in enumerate([resultado.q1, resultado.q2, resultado.q3, resultado.q4, resultado.q5,
                                                  resultado.q6, resultado.q7, resultado.q8, resultado.q9, resultado.q10], start=1):
            resposta_correta = gabarito[questao - 1]
            if resposta_aluno == resposta_correta:
                nota_final += 1

        resultado.nota = nota_final

        # Inserir o resultado na tabela resultados_provas
        session.add(resultado)
        session.commit()
        session.refresh(resultado)
        
        # Retornar os dados com status code 201
        return resultado
