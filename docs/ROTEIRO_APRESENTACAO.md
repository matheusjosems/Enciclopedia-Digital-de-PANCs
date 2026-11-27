# 🎤 Roteiro de Apresentação Acadêmica (5 a 10 minutos)
## Enciclopédia Digital de PANCs — Ciência da Computação (CEUB)

Este roteiro organiza a demonstração ao vivo para o professor e a banca, cobrindo o problema, a arquitetura técnica e os **5 passos do fluxo do usuário** definidos em [notas.txt](../notas.txt).

---

## ⏱️ Cronograma Sugerido (8 minutos)

| Etapa | Tempo | Foco |
| :--- | :---: | :--- |
| 1. Abertura e Problema | 1 min | Contexto das PANCs, riscos de identificação errada e objetivo do sistema |
| 2. Arquitetura & Banco | 1 min | Stack gratuita (FastAPI + SQLite + IA + Front-end responsivo) e diagrama ER |
| 3. Demo: Cadastro/Login | 1 min | Fluxo seguro com bcrypt e JWT (`/login`) |
| 4. Demo: Catálogo e Busca | 1,5 min | Busca em tempo real e ficha técnica com receitas (`/`, `/planta/{id}`) |
| 5. Demo: Câmera + IA + Coleção | 2,5 min | Identificação por foto (`/identificar`), aviso RF14, salvar e abrir `/minha-colecao` e `/perfil` |
| 6. Evidência Técnica (Swagger & Testes) | 1 min | `/docs`, `check_health.py` e `pytest -v` (47 testes passando) |

---

## 🚀 Preparação Antes da Apresentação

No diretório do projeto, com o ambiente virtual ativado:

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/check_health.py
pytest -v
uvicorn main:app --reload
```

Deixe duas abas abertas no navegador:
1. `http://127.0.0.1:8000/` (com DevTools `F12` pronto para alternar para visualização mobile).
2. `http://127.0.0.1:8000/docs` (Swagger / OpenAPI).

---

## 🗣️ Roteiro Passo a Passo

### 1. Problema e Proposta de Valor (1 min)
- Explique o que são **PANCs (Plantas Alimentícias Não Convencionais)** e a dor central: quem encontra uma planta espontânea muitas vezes não sabe identificá-la com segurança, não sabe quais partes são comestíveis nem como prepará-la.
- Apresente a proposta: reunir em um único aplicativo web responsivo **identificação por foto com IA**, **aviso ético de segurança alimentar (RF14)**, **ficha botânica com receitas regionais** e **coleção pessoal gamificada**.

### 2. Arquitetura e Dados Reais do Cerrado (1 min)
- Mostre rapidamente [er_enciclopedia.png](../er_enciclopedia.png) e destaque que o banco `pancs.db` foi populado com **63 espécies reais** e suas receitas extraídas via web scraping (`Web_Scraping_Enciclopédia_Digital_de_PANCs.ipynb` -> `scripts/seed_database.py`).
- Cite a stack 100% gratuita: Python, FastAPI, SQLAlchemy/SQLite, bcrypt + PyJWT, Pillow/NumPy e HTML5 + TailwindCSS + JS Vanilla.

### 3. Passo 1 — Cadastro e Login Seguro (1 min)
- Acesse `http://127.0.0.1:8000/login`.
- Crie uma conta de demonstração (ou entre com uma já criada).
- Destaque que a senha é armazenada com hash `bcrypt` (**RNF02**) e o acesso usa Bearer Token JWT armazenado para as rotas privadas (**RNF03**).

### 4. Passo 2 — Catálogo e Ficha com Receitas (1,5 min)
- Na página inicial (`/`), digite `"ora"` ou `"peixinho"` na busca em tempo real e teste os filtros de bioma (`Cerrado`, `Mata Atlântica`).
- Abra uma ficha (`/planta/{id}`) e navegue pelas 3 abas: **Descrição Botânica**, **Partes Comestíveis & Cuidados** e **Receitas Culinárias**.

### 5. Passos 3, 4 e 5 — Foto na Câmera, IA, Aviso RF14 e Coleção (2,5 min)
- Acesse `/identificar` (ative o modo celular no `F12` para demonstrar o layout mobile-first).
- Mostre o botão **Fotografar Planta** (`capture="environment"`) e envie uma imagem pela opção **Escolher da Galeria**.
- Clique em **Identificar Espécie com IA** e aponte os elementos na tela:
  1. Tempo de resposta imediato (< 1s, atendendo **RNF01** < 10s).
  2. Badge de **nível de confiança (%)** (**RF05**) e tratamento de **baixa confiança (RNF07)**.
  3. **Aviso obrigatório de segurança botânica (RF14)** em destaque amarelo antes do consumo.
  4. Receitas sugeridas e outras espécies semelhantes.
- Clique em **Salvar na Minha Coleção** (**RF08**).
- Acesse `/minha-colecao` para mostrar a foto enviada pelo usuário salva com data, abra **Detalhes & Receitas (RF10)** e mostre o botão de remoção (**RF11**).
- Acesse `/perfil` para exibir o contador dinâmico de descobertas e o distintivo do usuário (**RF03**).

### 6. Encerramento Técnico — Swagger e Testes Automatizados (1 min)
- Mostre `http://127.0.0.1:8000/docs` exibindo todas as **12 APIs REST** organizadas por grupo.
- No terminal, mostre a saída de `python scripts/check_health.py` (`STATUS: OK - Sistema 100% pronto para demonstração`) e `pytest -v` (**47 testes automatizados passando** cobrindo autenticação, isolamento entre usuários, upload, IA e rotas web).

---

## 💡 Checklist Pré-Banca
- [ ] `pancs.db` populado com 63 plantas e receitas (`python scripts/check_health.py` retornando OK)
- [ ] `pytest -v` com 100% dos testes em verde
- [ ] Imagem JPG de teste separada na pasta para demonstração rápida no navegador
- [ ] Modo responsivo (mobile) conferido no navegador
