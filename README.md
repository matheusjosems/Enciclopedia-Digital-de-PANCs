# Enciclopédia Digital de PANCs

Sistema web em que o usuário fotografa uma planta, uma IA a identifica e o sistema mostra a descrição e receitas, guardando cada planta na coleção pessoal do usuário. As PANC (Plantas Alimentícias Não Convencionais) são plantas comestíveis pouco conhecidas, e o objetivo do projeto é ajudar as pessoas a reconhecê-las e usá-las na cozinha.

Projeto final da disciplina de Desenvolvimento de Sistemas, do curso de Ciência da Computação do CEUB.

## Tecnologias

- Python
- FastAPI
- Uvicorn

## Como rodar

1. Clone o repositório:

   ```
   git clone https://github.com/matheusjosems/Enciclopedia-Digital-de-PANCs.git
   cd Enciclopedia-Digital-de-PANCs
   ```

2. Crie e ative o ambiente virtual (Windows):

   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

4. Inicie o servidor:

   ```
   uvicorn main:app --reload
   ```

5. Abra `http://127.0.0.1:8000/docs` no navegador para ver e testar as rotas.

## Rotas disponíveis

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/plantas` | Lista as plantas do catálogo |
| GET | `/plantas/{id}` | Retorna os dados de uma planta |

As demais rotas planejadas (cadastro e login, identificação por foto, coleção e receitas) estão descritas no documento de requisitos do projeto e serão implementadas nas próximas entregas.

## Estrutura do projeto

```
├── main.py              # app e rotas
├── requirements.txt     # dependências
└── models/
    └── planta.py        # modelo de dados da planta
```

## Autor

Matheus de Morais
