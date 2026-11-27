# 🌿 Enciclopédia Digital de PANCs

Sistema web responsivo para identificação botânica por imagem, consulta de fichas técnicas, receitas culinárias e diário pessoal de descobertas de **PANCs (Plantas Alimentícias Não Convencionais)** do Cerrado brasileiro.

> Projeto final da disciplina de **Desenvolvimento de Sistemas** — Ciência da Computação (CEUB).  
> Planejamento executado em 12 Dailys sequenciais documentadas em [FLUXO_DE_TRABALHO.md](FLUXO_DE_TRABALHO.md) com base nos requisitos de [notas.txt](notas.txt).

---

## 🎯 Resumo Executivo & Relevância

Embora o Brasil abrigue enorme biodiversidade, grande parte das plantas comestíveis espontâneas permanece desconhecida da população urbana. Quem encontra uma PANC enfrenta quatro barreiras centrais:
1. **Dificuldade de identificação** (risco de confusão com espécies tóxicas).
2. **Informação dispersa** em artigos científicos e guias técnicos pouco acessíveis.
3. **Falta de uso prático na cozinha** (poucas receitas rápidas disponíveis).
4. **Baixo engajamento** pela ausência de um registro pessoal de descobertas.

A **Enciclopédia Digital de PANCs** resolve essas dores em um fluxo de 5 passos:
1. O usuário cria sua conta e faz login (JWT + bcrypt).
2. Fotografa a planta pela câmera do celular ou envia uma foto da galeria.
3. O sistema valida e salva a imagem localmente e executa a inferência de visão computacional, exibindo a espécie provável, confiança (%) e **aviso obrigatório de segurança botânica (RF14)**.
4. O usuário consulta partes comestíveis, cuidados de preparo e receitas regionais.
5. Salva a descoberta com foto e data em sua **Coleção Pessoal** isolada por usuário.

---

## 🏗️ Arquitetura da Solução

```text
┌────────────────────────────────────────────────────────────────────┐
│                     Front-end Responsivo (Web)                     │
│  HTML5 + TailwindCSS (CDN) + JavaScript Vanilla (Fetch API / JWT)  │
│  Telas: /  |  /login  |  /planta/{id}  |  /identificar  |          │
│         /minha-colecao  |  /perfil                                 │
└───────────────────────────────┬────────────────────────────────────┘
                                │ HTTP / REST (JSON & FormData)
┌───────────────────────────────▼────────────────────────────────────┐
│                    Back-end FastAPI + Uvicorn                      │
│  • Auth & Segurança: JWT (PyJWT) + Hash bcrypt (routers/auth.py)   │
│  • Catálogo & Receitas: SQLAlchemy ORM (plantas.py, receitas.py)   │
│  • Coleção Privada: Isolamento por usuário (routers/colecao.py)    │
│  • Upload Local: Validação JPG/PNG <= 5MB (utils/image_uploader.py)│
│  • IA Botânica: Inferência visual Pillow+NumPy (services/ia_service)│
└───────────┬───────────────────────────────────────┬────────────────┘
            │                                       │
┌───────────▼───────────┐               ┌───────────▼───────────┐
│   Banco Relacional    │               │  Armazenamento Local  │
│  SQLite (pancs.db)    │               │   Pasta uploads/      │
│  63 PANCs + Receitas  │               │  Servida em /uploads  │
└───────────────────────┘               └───────────────────────┘
```

### Modelagem de Banco de Dados
O esquema relacional segue o diagrama oficial [er_enciclopedia.png](er_enciclopedia.png) com as entidades `usuarios`, `plantas`, `regioes`, `planta_regiao`, `planta_sazonalidade`, `receitas` e `colecao`.

---

## 🛠️ Stack Tecnológica (100% Gratuita e Open Source)

- **Linguagem:** Python 3.10+
- **API REST & Servidor:** FastAPI + Uvicorn (Swagger automático em `/docs`)
- **Banco de Dados & ORM:** SQLite (`pancs.db`) + SQLAlchemy
- **Segurança:** `bcrypt` (hash de senhas) + `PyJWT` (autenticação Bearer JWT)
- **Processamento de Imagem & IA:** Pillow (`PIL`) + NumPy (inferência visual rápida em < 1s e validação de imagens)
- **Testes Automatizados:** `pytest` + `httpx`
- **Front-end:** HTML5 semântico, TailwindCSS via CDN, CSS3 e JavaScript Vanilla

---

## 🔌 Rotas da API REST & Páginas Web

### 12 APIs Principais (Especificadas em `notas.txt`) + Auxiliares

| Grupo | Método | Rota | Autenticação | Status Esperados | Descrição |
| :--- | :---: | :--- | :---: | :---: | :--- |
| Autenticação | `POST` | `/auth/cadastro` | Pública | `201`, `400` | Cria conta com nome, e-mail único e senha com hash bcrypt (**RF01**, **RNF02**) |
| Autenticação | `POST` | `/auth/login` | Pública | `200`, `400`, `401` | Valida credenciais (JSON ou Form Data) e devolve token JWT (**RF02**) |
| Usuários | `GET` | `/usuarios/me` | Bearer JWT | `200`, `401` | Retorna perfil e total de plantas descobertas (**RF03**, **RNF03**) |
| Identificação | `POST` | `/identificacoes` | Pública | `200`, `400`, `500` | Recebe foto JPG/PNG até 5MB, identifica planta, calcula confiança e retorna aviso **RF14** e alerta **RNF07** |
| Plantas | `GET` | `/plantas` | Pública | `200` | Lista catálogo com busca (`nome`), filtro (`regiao`) e paginação (`skip`, `limit`) (**RF12**) |
| Plantas | `GET` | `/plantas/{id}` | Pública | `200`, `404` | Ficha completa: nome popular/científico, partes comestíveis, cuidados e regiões (**RF06**) |
| Coleção | `POST` | `/colecao` | Bearer JWT | `201`, `400`, `401`, `404` | Salva descoberta na coleção do usuário com foto e data (**RF08**) |
| Coleção | `GET` | `/colecao` | Bearer JWT | `200`, `401` | Lista exclusivamente as descobertas do usuário logado (**RF09**, **RNF03**) |
| Coleção | `GET` | `/colecao/{id}` | Bearer JWT | `200`, `401`, `403`, `404` | Detalhes da descoberta com foto do usuário e receitas recomendadas (**RF10**) |
| Coleção | `DELETE` | `/colecao/{id}` | Bearer JWT | `200`, `401`, `403`, `404` | Remove uma planta da coleção do próprio usuário (**RF11**) |
| Receitas | `GET` | `/plantas/{id}/receitas` | Pública | `200`, `404` | Lista receitas associadas à planta informada (**RF07**) |
| Receitas | `GET` | `/receitas/{id}` | Pública | `200`, `404` | Detalha ingredientes, modo de preparo, tempo e rendimento (**RF13**) |
| Receitas *(extra)* | `GET` | `/receitas` | Pública | `200` | Lista todas as receitas cadastradas no catálogo |
| Uploads *(extra)* | `POST` | `/upload-foto` | Pública | `201`, `400` | Valida (JPG/PNG <= 5MB) e salva foto com UUID em `uploads/` (**RNF08**) |
| Estáticos | `GET` | `/uploads/{arquivo}` | Pública | `200`, `404` | Serve as imagens enviadas pelos usuários |

### Páginas Web Responsivas (`frontend/`)

| Rota Web | Arquivo | Finalidade |
| :--- | :--- | :--- |
| `/` | `frontend/index.html` | Catálogo interativo das 63 PANCs com busca em tempo real e filtro por bioma |
| `/login` | `frontend/login.html` | Cadastro de conta e login com armazenamento do JWT em `localStorage` |
| `/planta/{id}` | `frontend/planta.html` | Ficha técnica da espécie com abas (Descrição, Cuidados, Receitas) |
| `/identificar` | `frontend/identificar.html` | Câmera do celular (`capture="environment"`) / galeria, resultado da IA, aviso RF14 e salvar na coleção |
| `/minha-colecao` | `frontend/colecao.html` | Galeria pessoal de descobertas com modal de receitas e exclusão |
| `/perfil` | `frontend/perfil.html` | Dados da conta, contador de espécies descobertas e distintivo |

---

## ▶️ Passo a Passo para Rodar do Zero

### 1. Clonar o repositório
```bash
git clone https://github.com/matheusjosems/Enciclopedia-Digital-de-PANCs.git
cd Enciclopedia-Digital-de-PANCs
```

### 2. Criar e ativar o ambiente virtual
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Criar tabelas e popular o banco SQLite (63 PANCs)
```bash
python scripts/init_db.py
python scripts/seed_database.py
```

### 5. Validar saúde do sistema e executar testes automatizados
```bash
python scripts/check_health.py
pytest -v
```

### 6. Iniciar a aplicação
```bash
uvicorn main:app --reload
```
Acesse no navegador:
- **Aplicação Web:** `http://127.0.0.1:8000/`
- **Documentação Interativa (Swagger / OpenAPI):** `http://127.0.0.1:8000/docs`

---

## 📁 Estrutura do Projeto

```text
├── main.py                      # Aplicação FastAPI, StaticFiles e rotas web
├── database.py                  # Engine SQLite e sessão SQLAlchemy
├── requirements.txt             # Dependências gratuitas do projeto
├── pytest.ini                   # Configuração do pytest
├── er_enciclopedia.png          # Diagrama Entidade-Relacionamento oficial
├── notas.txt                    # Especificação dos 14 RFs, 9 RNFs e 12 APIs
├── core/                        # Segurança JWT, hashing bcrypt e dependência get_current_user
├── models/                      # Modelos ORM SQLAlchemy (Usuario, Planta, Regiao, Receita, Colecao, Sazonalidade)
├── schemas/                     # Schemas Pydantic de validação entrada/saída
├── routers/                     # Roteadores REST (auth, usuarios, plantas, receitas, colecao, upload, identificacao)
├── services/                    # Motor de visão computacional e inferência botânica (ia_service.py)
├── utils/                       # Validação e upload local de imagens (image_uploader.py)
├── data/                        # Base estruturada das 63 PANCs (pancs_seed.json)
├── frontend/                    # Interface web responsiva (HTML5, CSS, JS Vanilla)
├── scripts/                     # Scripts de inicialização, seed, diagnóstico (check_health.py) e fluxos
├── tests/                       # Suíte completa de testes automatizados (pytest)
├── docs/                        # Roteiro de apresentação acadêmica (ROTEIRO_APRESENTACAO.md)
└── uploads/                     # Diretório local para fotos enviadas pelos usuários
```

---

## 👤 Autor

**Matheus José de Morais Silva** — Ciência da Computação (CEUB)
