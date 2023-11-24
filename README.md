# Projeto de API REST com FastAPI, SQLModel, Docker e PostgreSQL

## Participantes do Grupo:
- Mateus Stangherlin
- Samuel Matsuo
- Felipe Carli

---

## Descrição

Este projeto consiste em uma API REST desenvolvida usando FastAPI, SQLModel e PostgreSQL. A API gerencia provas, resultados de provas e alunos.

---

## Configuração do banco de dados:
    
1. **Alterar Arquivo docker-compose:**
    
    ```Execute o docker
   docker-compose up

## Configuração do Ambiente

1. **Clonar o Repositório:**

   ```bash
   git clone https://github.com/Mateus402/aps01-api-rest-postgres.git
   cd nome-do-repositorio

1. **Instalar dependências:**

   ```Instale as dependências do projeto.
   pip install -r requirements.txt

1. **Execute o Projeto:**
    
    ```Execute o servidor FastAPI.
   uvicorn src.server:app --reload

## Funcionalidades da API:

Gerenciamento de Provas:

- POST /provas: Cria uma nova prova.
- GET /provas/{prova_id}: Obtém detalhes de uma prova específica.

Resultados de Provas:

- POST /resultados_provas: Cria um novo resultado de prova.
- GET /resultados_provas/{prova_id}: Obtém os resultados de uma prova específica.

Alunos e Respostas:

- PATCH /provas_aplicadas/{aluno_id}: Permite a alteração das respostas de um aluno em uma prova.

Exclusão de Provas:

- DELETE /provas/{prova_id}: Permite a exclusão de uma prova se não houver resultados associados.
    


