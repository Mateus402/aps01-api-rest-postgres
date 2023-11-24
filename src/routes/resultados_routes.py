from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from typing import List
from sqlalchemy.orm import Session

from src.config.database import get_session
from src.models.provas_model import Provas
from src.models.resultados_model import Resultados

resultados_provas_router = APIRouter(prefix="/resultados_provas")

@resultados_provas_router.post("")
def cria_resultado_prova(resultado_prova: Resultados):
    with get_session() as session:

        statement_prova = select(Provas).where(Provas.id == resultado_prova.prova_id)
        prova_existente = session.exec(statement_prova).first()
        if not prova_existente:
            raise HTTPException(status_code=404, detail="Prova não cadastrada")

        nota = 0
        respostas_corretas = [prova_existente.q1, prova_existente.q2, prova_existente.q3,
                              prova_existente.q4, prova_existente.q5, prova_existente.q6,
                              prova_existente.q7, prova_existente.q8, prova_existente.q9,
                              prova_existente.q10]

        for i in range(10):
            if getattr(resultado_prova, f"q{i + 1}") == respostas_corretas[i]:
                nota += 1

        resultado_prova.nota = nota

        session.add(resultado_prova)
        session.commit()
        session.refresh(resultado_prova)

        return resultado_prova



@resultados_provas_router.get("/{prova_id}")
def get_resultados_prova(prova_id: int):
    with get_session() as session:
        prova = session.exec(select(Provas).where(Provas.id == prova_id)).first()
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não encontrada")

        resultados = session.exec(select(Resultados).where(Resultados.prova_id == prova.id)).all()

        resultados_alunos = []
        for resultado in resultados:
            if resultado.nota >= 7:
                status_final = "aprovado"
            elif resultado.nota >= 5:
                status_final = "recuperação"
            else:
                status_final = "reprovado"

            resultados_alunos.append({
                "nome": resultado.nome,
                "nota": resultado.nota,
                "status_final": status_final
            })

        return {
            "descricao_prova": prova.descricao,
            "data_prova": prova.data_prova,
            "resultados_alunos": resultados_alunos
        }



provas_aplicadas_router = APIRouter(prefix="/provas_aplicadas")
@provas_aplicadas_router.patch("/{id}")
def update_prova_aplicada(
    id: int,
    resultado_prova: Resultados,
    novo_resultado: Resultados
):
    print(f"ID recebido na função: {id}")
    with get_session() as session:
        resultado_antigo = session.query(Resultados).filter(Resultados.id == id).first()

    statement_prova = select(Provas).where(Provas.id == resultado_prova.prova_id)
    prova_existente = session.exec(statement_prova).first()

    if not resultado_antigo:
        print("Resultado da prova não encontrado.")
        raise HTTPException(status_code=404, detail="Resultado da prova não encontrado")

    resultado_antigo.q1 = novo_resultado.q1
    resultado_antigo.q2 = novo_resultado.q2
    resultado_antigo.q3 = novo_resultado.q3
    resultado_antigo.q4 = novo_resultado.q4
    resultado_antigo.q5 = novo_resultado.q5
    resultado_antigo.q6 = novo_resultado.q6
    resultado_antigo.q7 = novo_resultado.q7
    resultado_antigo.q8 = novo_resultado.q8
    resultado_antigo.q9 = novo_resultado.q9
    resultado_antigo.q10 = novo_resultado.q10

    prova_existente = session.exec(select(Provas).where(Provas.id == resultado_antigo.prova_id)).first()
    respostas_corretas = [
        prova_existente.q1, prova_existente.q2, prova_existente.q3,
        prova_existente.q4, prova_existente.q5, prova_existente.q6,
        prova_existente.q7, prova_existente.q8, prova_existente.q9,
        prova_existente.q10
    ]


    def calcular_nota(resultado_prova):
        nota = 0
        for i in range(10):
            if getattr(resultado_prova, f"q{i + 1}") == respostas_corretas[i]:
                nota += 1
        return nota


    resultado_antigo.nota = calcular_nota(resultado_antigo)

    session.commit()
    session.refresh(resultado_antigo)

    return resultado_antigo





