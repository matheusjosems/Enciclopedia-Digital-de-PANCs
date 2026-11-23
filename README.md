# Enciclopédia Digital de PANCs

Sistema web em que o usuário fotografa uma planta, uma IA a identifica e o sistema mostra a descrição e receitas, guardando cada planta na coleção pessoal do usuário. As PANC (Plantas Alimentícias Não Convencionais) são plantas comestíveis pouco conhecidas, e o objetivo do projeto é ajudar as pessoas a reconhecê-las e usá-las na cozinha.

Projeto final da disciplina de Desenvolvimento de Sistemas, do curso de Ciência da Computação do CEUB.

## 🚀 Fluxo de Trabalho & Dailys (Execução Guiada por IA)

O planejamento do desenvolvimento deste projeto está organizado em **12 Dailys sequenciais** documentadas no arquivo [FLUXO_DE_TRABALHO.md](FLUXO_DE_TRABALHO.md). Cada daily contém o objetivo do dia, materiais de referência da pasta, requisitos atendidos, ferramentas 100% gratuitas e o comando gatilho para a IA executar a tarefa diária.

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

| Grupo | Método | Rota | Descrição |
| --- | --- | --- | --- |
| Autenticação | POST | `/auth/cadastro` | Cria uma conta com nome, e-mail e senha criptografada (bcrypt) |
| Autenticação | POST | `/auth/login` | Valida credenciais e devolve token de acesso Bearer JWT |
| Usuários | GET | `/usuarios/me` | Retorna o perfil do usuário logado e total de descobertas |
| Plantas | GET | `/plantas` | Lista as plantas do catálogo com busca e filtros |
| Plantas | GET | `/plantas/{id}` | Retorna os dados completos da planta |
| Receitas | GET | `/plantas/{id}/receitas` | Lista as receitas culinárias feitas com a planta |
| Receitas | GET | `/receitas/{id}` | Retorna uma receita com ingredientes e modo de preparo |
| Receitas | GET | `/receitas` | Catálogo geral de todas as receitas culinárias |
| Coleção | POST | `/colecao` | Salva uma planta na coleção pessoal com foto e data |
| Coleção | GET | `/colecao` | Lista exclusivamente as plantas descobertas pelo usuário logado |
| Coleção | GET | `/colecao/{id}` | Mostra os detalhes da descoberta com foto e receitas |
| Coleção | DELETE | `/colecao/{id}` | Remove uma planta da coleção pessoal |
| Identificação | POST | `/identificacoes` | Identifica a espécie por IA, informa confiança (%) e aviso botânico |
| Uploads | POST | `/upload-foto` | Envia foto JPG/PNG até 5MB e salva no servidor local com UUID |
| Estáticos | GET | `/uploads/{foto}` | Servidor estático público de exibição das fotos salvas |

Todas as 12 APIs REST especificadas no [FLUXO_DE_TRABALHO.md](FLUXO_DE_TRABALHO.md) e [notas.txt](notas.txt) estão implementadas e ativas.

## Estrutura do projeto

```
├── main.py              # app e rotas
├── requirements.txt     # dependências
└── models/
    └── planta.py        # modelo de dados da planta
```

## Autor

Matheus de Morais
