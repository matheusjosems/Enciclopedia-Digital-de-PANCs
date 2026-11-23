# 📋 Fluxo de Trabalho & Protocolo de Dailys (12 Dias)
## Enciclopédia Digital de PANCs — Ciência da Computação (CEUB)

> **Finalidade deste documento:** Este arquivo atua como o **orquestrador mestre e gatilho de execução automatizada** do projeto. Ele foi estruturado a partir dos materiais já existentes no repositório (`README.md`, `notas.txt`, `er_enciclopedia.png`, `Web_Scraping_Enciclopédia_Digital_de_PANCs.ipynb`, `CNN_CIFAR.ipynb`, `main.py` e a pasta `models/`).
>
> Todas as ferramentas recomendadas são **100% gratuitas, de código aberto e sem necessidade de cartões de crédito ou serviços pagos**, ideais para projetos universitários.

---

## 🤖 Como Usar este Arquivo com a IA (Protocolo de Gatilho)

Quando você quiser que a IA execute a tarefa de um dia específico, envie no chat o seguinte comando:

```text
IA, execute o DIA [NÚMERO DO DIA] conforme o arquivo FLUXO_DE_TRABALHO.md
```
*(Exemplo: `IA, execute o DIA 1 conforme o arquivo FLUXO_DE_TRABALHO.md`)*

### O que a IA fará ao receber o comando:
1. Lerá a seção correspondente ao dia solicitado neste arquivo.
2. Consultará os arquivos e modelos de referência indicados na seção **Materiais Base da Pasta**.
3. Criará ou atualizará o código, rotas, modelos e scripts necessários.
4. Adicionará as dependências gratuitas correspondentes ao `requirements.txt`.
5. Executará os comandos de validação e testes automatizados.
6. Entregará um resumo do que foi construído e apontará onde você deve revisar.

### O seu papel como desenvolvedor/estudante:
1. Revisar o código gerado.
2. Testar interativamente via Swagger (`http://127.0.0.1:8000/docs`) ou no navegador.
3. Ajustar pequenos detalhes de negócio ou estilo e dar o sinal verde para o próximo dia.

---

## 🗺️ Mapa Geral dos 12 Dias de Trabalho

| Dia | Foco Principal | Materiais da Pasta Utilizados | Entregável Chave |
| :---: | :--- | :--- | :--- |
| **01** | Banco de Dados Relacional & Modelagem ORM | `er_enciclopedia.png`, `models/`, `notas.txt` | SQLite configurado + SQLAlchemy models + schemas Pydantic |
| **02** | Extração e Carga de Dados (Seed das 63 PANCs) | `Web_Scraping_...ipynb`, `notas.txt` | Script de seed populando banco com dados reais do Cerrado |
| **03** | Sistema de Autenticação & Segurança JWT | `notas.txt` (RF01, RF02, RF03, RNF02, RNF03) | Cadastro, Login com hash bcrypt, token JWT e proteção de rotas |
| **04** | Catálogo de Plantas & Busca Avançada | `main.py`, `notas.txt` (RF06, RF12) | Rotas `GET /plantas` e `GET /plantas/{id}` conectadas ao SQLite |
| **05** | Módulo de Receitas e Culinária PANC | `notas.txt` (RF07, RF13), Scraping | Endpoints de receitas (`/plantas/{id}/receitas`, `/receitas/{id}`) |
| **06** | Coleção Pessoal do Usuário ("Minhas Descobertas") | `models/colecao.py`, `er_enciclopedia.png`, `notas.txt` | CRUD da coleção associada ao usuário autenticado via JWT |
| **07** | Upload e Validação de Imagens Locais | `notas.txt` (RF04, RNF08), `main.py` | Upload de fotos JPG/PNG até 5MB e servidor estático `/uploads` |
| **08** | Módulo de Visão Computacional / Identificação IA | `CNN_CIFAR.ipynb`, `notas.txt` (RF05, RF14, RNF01) | Endpoint `POST /identificacoes` com modelo CNN e aviso de cautela |
| **09** | Testes Automatizados e Verificação da API | `notas.txt` (RNF09) | Suíte de testes com `pytest` + `httpx` para todas as 12 APIs |
| **10** | Front-end Web Responsivo: Catálogo e Autenticação | `notas.txt` (RNF05, RNF06) | Telas web em HTML5 + CSS/Tailwind + JS: Login, Cadastro e Catálogo |
| **11** | Front-end Web Responsivo: Câmera, IA e Coleção | `notas.txt` (Fluxo de 5 passos) | Interface de foto na câmera, retorno da IA e Minha Coleção |
| **12** | Documentação, Refinamento e Apresentação Final | `README.md`, `notas.txt` | README completo, documentação OpenAPI e roteiro para a banca |

---

## 🛠️ Stack Tecnológica 100% Gratuita e Acessível

- **Linguagem & Runtime:** Python 3.10+ (já instalado no projeto).
- **Framework Web Back-end:** FastAPI + Uvicorn (rápido, tipado, gera OpenAPI/Swagger automático).
- **Banco de Dados:** SQLite (nativo do Python, arquivo local sem custo nem instalação de servidores como Postgres/MySQL).
- **ORM & Migrações:** SQLAlchemy 2.0 (abstrato e padrão na indústria).
- **Segurança:** Passlib (`bcrypt`) para hash de senhas e PyJWT (`python-jose`) para tokens de autenticação.
- **Processamento de Imagens:** Pillow (`PIL`) para redimensionamento e verificação de arquivos.
- **Inteligência Artificial:** PyTorch + Torchvision (MobileNetV2 pré-treinada ou similaridade com embeddings locais, gratuitos e leves).
- **Extração de Dados:** BeautifulSoup4 + Pandas (já demonstrados no notebook de scraping).
- **Testes:** Pytest + HTTPX (testes assíncronos rápidos e simples).
- **Front-end:** HTML5 semântico, JavaScript Vanilla e TailwindCSS via CDN (sem necessidade de Node.js, Webpack ou build complexo).

---

# 📅 Detalhamento Diário das Dailys

---

### 🔹 DIA 01: Banco de Dados Relacional & Modelagem ORM
* **Objetivo:** Estabelecer a camada de persistência definitiva do projeto utilizando banco SQLite e mapeamento objeto-relacional (ORM) com SQLAlchemy, espelhando fielmente o diagrama relacional oficial.
* **Requisitos Atendidos:** Base para todos os RFs e RNF02, RNF03, RNF09.
* **Materiais da Pasta Utilizados:**
  - `er_enciclopedia.png`: Estrutura das entidades `USUARIO`, `PLANTA`, `COLECAO`, `REGIAO`, `PLANTA_SAZONALIDADE`, `PLANTA_REGIAO`.
  - `models/planta.py`: Modelo Pydantic existente que deve ser expandido.
  - `models/usuario.py` e `models/colecao.py`: Arquivos vazios que devem ser implementados.
  - `notas.txt`: Campos adicionais necessários para receitas (RF07, RF13) e cuidados/partes comestíveis (RF06).
* **Ferramentas Gratuitas:** `sqlite3` (nativo do Python), `sqlalchemy`, `pydantic`.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 1: configure o banco SQLite, crie a infraestrutura SQLAlchemy (database.py), implemente os modelos ORM e schemas Pydantic de todas as entidades de er_enciclopedia.png e notas.txt.`
* **Passo a Passo de Execução para a IA:**
  1. Criar `database.py` configurando `engine = create_engine("sqlite:///./pancs.db", connect_args={"check_same_thread": False})` e `Base = declarative_base()`, além da dependência `get_db()`.
  2. Implementar em `models/`:
     - `models/usuario.py`: Tabela `usuarios` (`id_usuario`, `nome`, `email`, `senha_hash`, `criado_em`).
     - `models/planta.py`: Tabela `plantas` (`id_planta`, `nome_popular`, `nome_cientifico`, `familia`, `descricao`, `partes_comestiveis`, `cuidados`, `sabor`, `foto_url`).
     - `models/regiao.py` e `models/sazonalidade.py`: Tabelas `regioes`, `planta_regiao` e `planta_sazonalidade`.
     - `models/receita.py`: Tabela `receitas` (`id_receita`, `id_planta`, `titulo`, `ingredientes`, `modo_preparo`).
     - `models/colecao.py`: Tabela `colecao` (`id_colecao`, `id_usuario`, `id_planta`, `data_descoberta`, `foto_usuario`).
  3. Criar a pasta `schemas/` com schemas Pydantic correspondentes para validação de entrada/saída.
  4. Adicionar em `requirements.txt`: `sqlalchemy`.
  5. Criar script de teste `scripts/init_db.py` para gerar as tabelas no arquivo `pancs.db`.
* **Critérios de Aceite:**
  - Execução de `python scripts/init_db.py` gera o arquivo `pancs.db` sem erros de chave primária ou estrangeira.
* **Checklist do Usuário:** Conferir se as tabelas no `pancs.db` refletem o diagrama `er_enciclopedia.png`.

---

### 🔹 DIA 02: Pipeline de Carga de Dados (Seed das 63 PANCs)
* **Objetivo:** Converter os dados extraídos do notebook de scraping em uma rotina de carga inicial (seed) para o banco de dados, preenchendo o catálogo com as 63 espécies reais de PANCs catalogadas.
* **Requisitos Atendidos:** RF06, RF12, RF13.
* **Materiais da Pasta Utilizados:**
  - `Web_Scraping_Enciclopédia_Digital_de_PANCs.ipynb`: Código com lógica BeautifulSoup e regex para raspar dados de `pancdocerrado.com.br` (nomes, propriedades, sugestões de preparo, fotos).
  - `notas.txt`: Especificações de campos que devem ser armazenados.
* **Ferramentas Gratuitas:** `requests`, `beautifulsoup4`, `pandas`, `sqlalchemy`.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 2: extraia a lógica de Web_Scraping_Enciclopédia_Digital_de_PANCs.ipynb e crie um script em scripts/seed_database.py que popule o banco SQLite com as 63 PANCs e suas respectivas receitas e regiões.`
* **Passo a Passo de Execução para a IA:**
  1. Extrair os dados já obtidos ou consolidar uma lista estruturada/JSON de fallback em `data/pancs_seed.json` para que o seed rode rápido e offline sem depender da internet da faculdade.
  2. Criar `scripts/seed_database.py` que lê o arquivo estruturado (ou executa a raspagem se solicitado) e insere:
     - Registros na tabela `plantas` (Ora-pro-nóbis, Peixinho, Taioba, Beldroega, etc.).
     - Registros na tabela `regioes` e relacionamento `planta_regiao`.
     - Registros de receitas associadas na tabela `receitas` (extraídas da seção "Sugestão de Preparo").
  3. Adicionar tratamento para não duplicar registros ao rodar o seed mais de uma vez.
* **Critérios de Aceite:**
  - Rodar `python scripts/seed_database.py` e verificar contagem de plantas no banco (`COUNT(*) >= 60`).
* **Checklist do Usuário:** Verificar se plantas clássicas como Ora-pro-nóbis e Peixinho da Horta estão com nomes científicos e receitas cadastradas.

---

### 🔹 DIA 03: Módulo de Autenticação & Segurança (JWT & Bcrypt)
* **Objetivo:** Implementar o fluxo seguro de cadastro e login de usuários com hash de senhas e geração de tokens JWT, garantindo a proteção das rotas privadas.
* **Requisitos Atendidos:** RF01, RF02, RF03, RNF02, RNF03, RNF04.
* **Materiais da Pasta Utilizados:**
  - `notas.txt`: APIs 1, 2 e 3 (`POST /auth/cadastro`, `POST /auth/login`, `GET /usuarios/me`).
  - `models/usuario.py`: Modelo relacional de usuário criado no Dia 1.
* **Ferramentas Gratuitas:** `passlib[bcrypt]` (hashing), `python-jose[cryptography]` ou `PyJWT` (tokens JWT), `fastapi.security.OAuth2PasswordBearer`.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 3: implemente a segurança de senhas (bcrypt), emissão e validação de tokens JWT, rotas POST /auth/cadastro, POST /auth/login e GET /usuarios/me com dependência get_current_user.`
* **Passo a Passo de Execução para a IA:**
  1. Criar `core/security.py` com funções para gerar hash (`hash_senha`), verificar senha (`verificar_senha`) e criar token JWT (`criar_token_acesso`).
  2. Criar `routers/auth.py` com:
     - `POST /auth/cadastro`: validação de email e senha única, salvando com hash.
     - `POST /auth/login`: autenticação por credenciais e retorno do token `access_token`.
  3. Criar `routers/usuarios.py` com:
     - `GET /usuarios/me`: rota autenticada que retorna os dados do usuário e contador de plantas salvas na coleção.
  4. Configurar a dependência `get_current_user` para validar o token no cabeçalho `Authorization: Bearer <token>`.
  5. Registrar os routers no `main.py`.
* **Critérios de Aceite:**
  - Testar no Swagger (`/docs`): criar usuário, logar e obter token, e acessar `/usuarios/me` passando o Bearer Token.
* **Checklist do Usuário:** Confirmar que senhas no banco `pancs.db` nunca aparecem em texto puro.

---

### 🔹 DIA 04: Catálogo de Plantas & Busca Avançada
* **Objetivo:** Refatorar as rotas atuais de catálogo em `main.py` para consultar o banco SQLite real via SQLAlchemy, implementando busca inteligente por nome popular, nome científico e filtros por região.
* **Requisitos Atendidos:** RF06, RF12, RNF09 (APIs 5 e 6).
* **Materiais da Pasta Utilizados:**
  - `main.py`: Rotas existentes `/plantas` e `/plantas/{id}` (atualmente mockadas com lista em memória).
  - `notas.txt`: Requisito RF12 (busca por nome) e RF06 (ficha com partes comestíveis e cuidados).
* **Ferramentas Gratuitas:** `fastapi`, `sqlalchemy`.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 4: migre as rotas de plantas de main.py para routers/plantas.py conectando ao SQLite via SQLAlchemy, com suporte a busca textual (nome popular e científico) e filtro por região.`
* **Passo a Passo de Execução para a IA:**
  1. Criar `routers/plantas.py` e mover a lógica das rotas para lá:
     - `GET /plantas`: parâmetros de query opcionais (`nome`, `regiao`, `skip`, `limit`), executando query com `ilike` no SQLite.
     - `GET /plantas/{id}`: busca por ID primário com `HTTPException(404)` se não encontrada.
  2. Garantir que a resposta inclua ficha completa: nome popular, científico, família, descrição, partes comestíveis, cuidados e foto de referência.
  3. Limpar a lista hardcoded de `main.py` e incluir o `router` com prefixo `/plantas`.
* **Critérios de Aceite:**
  - `GET /plantas?nome=ora` retorna a ficha da Ora-pro-nóbis direto do banco de dados.
  - `GET /plantas/99999` devolve status `404` com mensagem amigável.
* **Checklist do Usuário:** Testar buscas por nomes parciais no Swagger e verificar se todas as informações técnicas aparecem.

---

### 🔹 DIA 05: Módulo de Receitas e Culinária PANC
* **Objetivo:** Implementar os endpoints de receitas culinárias das PANCs, conectando o conhecimento gastronômico extraído do scraping com a API.
* **Requisitos Atendidos:** RF07, RF13 (APIs 11 e 12).
* **Materiais da Pasta Utilizados:**
  - `notas.txt`: APIs 11 (`GET /plantas/{id}/receitas`) e 12 (`GET /receitas/{id}`).
  - `Web_Scraping_Enciclopédia_Digital_de_PANCs.ipynb`: Sugestões de preparo raspadas (doces, sucos, refogados, mousses, etc.).
* **Ferramentas Gratuitas:** `fastapi`, `sqlalchemy`, `pydantic`.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 5: crie routers/receitas.py com as rotas GET /plantas/{id}/receitas e GET /receitas/{id}, retornando ingredientes, modo de preparo e rendimento.`
* **Passo a Passo de Execução para a IA:**
  1. Criar `routers/receitas.py`.
  2. Implementar `GET /plantas/{id}/receitas`: retorna lista de todas as receitas associadas à planta especificada.
  3. Implementar `GET /receitas/{id}`: retorna o detalhe individual de uma receita (título, tempo estimado, ingredientes e passo a passo).
  4. Vincular o router no `main.py`.
* **Critérios de Aceite:**
  - Consultar receitas de uma PANC (ex: id da Ora-pro-nóbis) e receber pelo menos uma receita detalhada em formato JSON.
* **Checklist do Usuário:** Validar se os textos das receitas estão claros e convidativos para quem deseja cozinhar.

---

### 🔹 DIA 06: Módulo da Coleção Pessoal do Usuário
* **Objetivo:** Criar o sistema de "diário de descobertas", permitindo que cada usuário autenticado salve as PANCs que encontrou, registre a data e consulte sua própria coleção de forma isolada.
* **Requisitos Atendidos:** RF08, RF09, RF10, RF11, RNF03, RNF04 (APIs 7, 8, 9 e 10).
* **Materiais da Pasta Utilizados:**
  - `models/colecao.py`: Modelo da entidade `Colecao`.
  - `er_enciclopedia.png`: Relacionamento entre `USUARIO` e `PLANTA` na tabela `COLECAO`.
  - `notas.txt`: Descrição das 4 APIs de coleção e regra de que cada usuário só acessa sua própria coleção.
* **Ferramentas Gratuitas:** `fastapi`, `sqlalchemy`.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 6: implemente routers/colecao.py com as 4 rotas de coleção (POST /colecao, GET /colecao, GET /colecao/{id}, DELETE /colecao/{id}) protegidas por token JWT.`
* **Passo a Passo de Execução para a IA:**
  1. Implementar `routers/colecao.py` injetando `current_user: Usuario = Depends(get_current_user)`.
  2. Rotas a implementar:
     - `POST /colecao`: adiciona a planta à coleção do usuário logado (com data automática ou fornecida e URL da foto tirada).
     - `GET /colecao`: lista apenas os registros pertencentes ao `id_usuario` logado.
     - `GET /colecao/{id}`: exibe a descoberta com detalhes da planta e receitas recomendadas.
     - `DELETE /colecao/{id}`: remove o registro da coleção garantindo que pertence ao usuário logado (retorna 403/404 caso contrário).
  3. Atualizar a rota `GET /usuarios/me` para calcular dinamicamente o número total de plantas descobertas pelo usuário.
* **Critérios de Aceite:**
  - Um usuário "A" não consegue visualizar nem excluir plantas da coleção de um usuário "B".
* **Checklist do Usuário:** Criar dois usuários de teste no Swagger e certificar-se de que as coleções são totalmente independentes.

---

### 🔹 DIA 07: Upload e Armazenamento de Imagens Locais
* **Objetivo:** Implementar o serviço de recebimento, validação e armazenamento das fotos enviadas pelos usuários no celular ou computador, sem depender de nuvens pagas (usando armazenamento em disco local).
* **Requisitos Atendidos:** RF04, RNF08 (fotos JPG/PNG de até 5MB).
* **Materiais da Pasta Utilizados:**
  - `notas.txt`: RNF08 (restrição de extensões JPG/PNG e tamanho limite de 5MB) e RF04 (envio de foto tirada na hora ou da galeria).
  - `main.py`: Configuração do `StaticFiles` para servir a pasta pública de imagens.
* **Ferramentas Gratuitas:** `python-multipart`, `Pillow` (PIL nativo), `fastapi.staticfiles`.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 7: implemente o serviço de upload local de imagens com validação de extensão (JPG/PNG), limite de 5MB, geração de UUID para nomes seguros e montagem de rota estática /uploads.`
* **Passo a Passo de Execução para a IA:**
  1. Criar pasta `uploads/` e configurar `app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")` em `main.py`.
  2. Criar serviço utilitário `utils/image_uploader.py`:
     - Validar cabeçalho MIME e extensão (`.jpg`, `.jpeg`, `.png`).
     - Validar tamanho do arquivo (máximo de 5 * 1024 * 1024 bytes).
     - Gerar nome único (`uuid4().hex + .jpg`).
     - Otimizar a imagem opcionalmente com Pillow (converter para RGB e comprimir se necessário).
  3. Criar endpoint auxiliar `POST /upload-foto` para uso pelo front-end e pelo módulo de identificação.
* **Critérios de Aceite:**
  - Enviar um arquivo PDF ou arquivo maior que 5MB e receber erro HTTP 400 com mensagem explicativa.
  - Enviar foto JPG válida e conseguir abri-la no navegador em `http://127.0.0.1:8000/uploads/<nome-arquivo>.jpg`.
* **Checklist do Usuário:** Testar o envio de imagens pelo Swagger e conferir se o arquivo foi salvo dentro da pasta `uploads/`.

---

### 🔹 DIA 08: Módulo de Visão Computacional / Identificação por IA
* **Objetivo:** Implementar o serviço de identificação botânica por imagem em `POST /identificacoes`, integrando o modelo de visão computacional e o aviso ético/botânico obrigatório de segurança antes do consumo.
* **Requisitos Atendidos:** RF04, RF05, RF14, RNF01, RNF07 (API 4).
* **Materiais da Pasta Utilizados:**
  - `CNN_CIFAR.ipynb`: Notebook de referência em PyTorch/CNN do professor Nikson Bernardes.
  - `notas.txt`: RF05 (nível de confiança), RF14 (aviso de que a identificação é aproximada e deve ser confirmada antes de comer), RNF01 (resposta em até 10s).
* **Ferramentas Gratuitas:** `torch`, `torchvision` (modelo MobileNetV2 leve pré-treinado no ImageNet com mapeamento para classes botânicas) OU classificador com embeddings / API de visão botânica gratuita (como Hugging Face free tier / PlantNet API gratuita).
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 8: implemente o endpoint POST /identificacoes em routers/identificacao.py recebendo a foto, processando pela IA botânica, calculando a confiança (%) e retornando a planta compatível com o aviso obrigatório de segurança (RF14).`
* **Passo a Passo de Execução para a IA:**
  1. Criar `services/ia_service.py` com o motor de inferência:
     - Carregamento lazy/otimizado de rede neural leve (`torchvision.models.mobilenet_v2(pretrained=True)` ou extrator de características).
     - Mapeamento das espécies do catálogo de PANCs mais próximas da foto enviada.
     - Cálculo probabilístico da taxa de confiança (ex: 88.5%).
  2. Implementar `routers/identificacao.py` com `POST /identificacoes`:
     - Recebe `UploadFile` (foto da planta).
     - Valida arquivo e executa a inferência.
     - Retorna: `id_planta`, `nome_popular`, `nome_cientifico`, `confianca`, `aviso_seguranca` ("ATENÇÃO: A identificação por IA é aproximada. Confirme sempre as características botânicas com um especialista ou guia confiável antes de ingerir qualquer planta.").
  3. Adicionar fallback resiliente caso o processamento falhe (RNF07).
* **Critérios de Aceite:**
  - Enviar uma foto de Ora-pro-nóbis e receber status 200 com a resposta em menos de 10 segundos, contendo o nome provável e o aviso do RF14 em destaque.
* **Checklist do Usuário:** Conferir se o aviso de segurança alimentar está explícito no JSON de retorno.

---

### 🔹 DIA 09: Testes Automatizados da API e Cobertura
* **Objetivo:** Criar uma suíte completa de testes automatizados com `pytest` e `httpx`, garantindo que todas as 12 APIs e requisitos de segurança e validação funcionem de forma robusta e sem regressões.
* **Requisitos Atendidos:** RNF09 (manutenibilidade e padrão REST), garantia de todos os RFs.
* **Materiais da Pasta Utilizados:**
  - `notas.txt`: Lista completa das 12 APIs do sistema e seus comportamentos esperados.
* **Ferramentas Gratuitas:** `pytest`, `pytest-asyncio`, `httpx`.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 9: crie a pasta tests/ com testes automatizados cobrindo os 5 grupos de APIs (Auth, Plantas, Receitas, Coleção e Identificação) usando pytest e httpx.`
* **Passo a Passo de Execução para a IA:**
  1. Criar `tests/conftest.py` com fixtures para banco de dados SQLite de teste em memória (`sqlite:///:memory:`) e cliente `TestClient(app)`.
  2. Criar os módulos de teste:
     - `tests/test_auth.py`: cadastro, login com sucesso, login com senha errada, proteção de rotas privadas sem token.
     - `tests/test_plantas.py`: listagem geral, busca por termo, consulta de ID inexistente (404).
     - `tests/test_receitas.py`: listagem de receitas por planta e detalhes por ID.
     - `tests/test_colecao.py`: inclusão de descoberta, listagem exclusiva do usuário, exclusão.
     - `tests/test_identificacao.py`: envio de foto e formato da resposta com aviso do RF14.
  3. Configurar script `pytest` no terminal.
* **Critérios de Aceite:**
  - Execução do comando `pytest` no terminal com 100% dos testes passando sem falhas.
* **Checklist do Usuário:** Executar `pytest -v` e observar os testes de todas as rotas passando em verde.

---

### 🔹 DIA 10: Interface Web Responsiva: Catálogo e Autenticação
* **Objetivo:** Desenvolver as primeiras telas da interface web do sistema (mobile-first), permitindo que qualquer pessoa acesse pelo navegador do celular ou computador para navegar pelo catálogo e se cadastrar/logar.
* **Requisitos Atendidos:** RNF05 (usabilidade no celular), RNF06 (compatibilidade com Chrome, Firefox, Edge, Safari).
* **Materiais da Pasta Utilizados:**
  - `notas.txt`: Requisitos de usabilidade, telas de login, perfil e consulta de catálogo.
  - `README.md`: Identidade e apresentação do projeto.
* **Ferramentas Gratuitas:** HTML5, CSS3 / TailwindCSS via CDN (sem necessidade de npm/node), JavaScript nativo (Fetch API).
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 10: crie o front-end web responsivo na pasta static/ (ou templates/) com as telas de Login, Cadastro, Catálogo de PANCs com campo de pesquisa em tempo real e Ficha da Planta com Receitas.`
* **Passo a Passo de Execução para a IA:**
  1. Estruturar a pasta `frontend/` (ou `static/web/`):
     - `index.html`: Catálogo interativo com barra de busca, cards das PANCs (foto, nome popular, nome científico, tags de região).
     - `planta.html`: Ficha completa da planta com abas para Descrição, Cuidados/Partes Comestíveis e Receitas sugeridas.
     - `login.html`: Formulário de login e cadastro com armazenamento do token JWT em `localStorage`.
     - `app.js`: Lógica de requisição às APIs FastAPI usando `fetch()`.
     - `styles.css`: Estilização verde/natureza moderna, limpa e responsiva (mobile-friendly).
  2. Servir as páginas através do FastAPI em rotas amigáveis (ex: `/`, `/login`, `/planta/{id}`).
* **Critérios de Aceite:**
  - Abrir `http://127.0.0.1:8000/` no navegador do celular ou desktop e conseguir pesquisar plantas instantaneamente pelo nome.
* **Checklist do Usuário:** Inspecionar o layout no modo celular do navegador (F12 -> dispositivo móvel) e verificar a usabilidade.

---

### 🔹 DIA 11: Interface Web Responsiva: Câmera, IA e Coleção
* **Objetivo:** Concluir a interface web com o fluxo central do aplicativo: permitir que o usuário use a câmera do smartphone para fotografar a planta, veja o resultado da IA e salve na sua coleção pessoal.
* **Requisitos Atendidos:** Passos 1 a 5 da Visão Geral de `notas.txt`, RF04, RF05, RF08, RF09, RF10, RF14.
* **Materiais da Pasta Utilizados:**
  - `notas.txt`: Fluxo em 5 passos ("O usuário cria conta -> Tira foto -> IA identifica -> Sistema mostra ficha/receita -> Salva na coleção pessoal").
* **Ferramentas Gratuitas:** HTML5 Media Capture (`<input type="file" accept="image/*" capture="environment">`), Fetch API com FormData.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 11: implemente a tela de identificação fotográfica com suporte à câmera do celular, exibição do resultado da IA com aviso de segurança (RF14), botão 'Salvar na Minha Coleção' e a página 'Minha Coleção' (galeria do usuário).`
* **Passo a Passo de Execução para a IA:**
  1. Criar `frontend/identificar.html`:
     - Botão grande "Fotografar Planta" ativando a câmera traseira do smartphone (`capture="environment"`).
     - Preview instantâneo da foto antes do envio.
     - Loading spinner indicando processamento da IA.
     - Card de resultado com % de confiança, alerta visual amarelo/vermelho para o aviso botânico (RF14) e botão de ação "Salvar na Minha Coleção".
  2. Criar `frontend/colecao.html`:
     - Galeria com fotos tiradas pelo próprio usuário e data de cada descoberta.
     - Botão para abrir os detalhes ou remover da coleção.
  3. Criar `frontend/perfil.html`:
     - Exibição do nome do usuário, data de cadastro e distintivo com total de espécies já descobertas.
* **Critérios de Aceite:**
  - Fazer login, simular o envio de uma foto, visualizar a classificação com a mensagem de alerta do RF14 e encontrar a planta salva na página "Minha Coleção".
* **Checklist do Usuário:** Realizar o fluxo completo de ponta a ponta pelo navegador e conferir a experiência visual.

---

### 🔹 DIA 12: Revisão Final, Documentação & Roteiro de Apresentação
* **Objetivo:** Consolidar a documentação final do projeto, atualizar o `README.md` com arquitetura e guias de reprodução, criar script de diagnóstico geral e elaborar o roteiro para apresentação acadêmica ao professor.
* **Requisitos Atendidos:** RNF09, finalização formal da disciplina de Desenvolvimento de Sistemas (CEUB).
* **Materiais da Pasta Utilizados:**
  - `README.md`: Atualização completa com todas as 12 rotas, telas, arquitetura e instruções.
  - `notas.txt`: Validação de 100% dos 14 RFs e 9 RNFs implementados.
  - `er_enciclopedia.png`: Inclusão na documentação de banco de dados.
* **Ferramentas Gratuitas:** Markdown, script de saúde do sistema em Python.
* **Gatilho do Prompt para a IA:**
  > `IA, execute o DIA 12: atualize o README.md com o manual completo da aplicação (rotas, prints, como rodar do zero), crie scripts/check_health.py para diagnóstico do sistema e monte o roteiro da apresentação acadêmica.`
* **Passo a Passo de Execução para a IA:**
  1. Atualizar `README.md` com:
     - Resumo executivo do projeto e relevância acadêmica/social das PANCs.
     - Diagrama de arquitetura da solução (FastAPI + SQLite + PyTorch/IA + Front-end responsivo).
     - Tabela completa e atualizada das 12 rotas REST com códigos de status esperados.
     - Passo a passo à prova de falhas para rodar o projeto do zero em qualquer computador (Windows/Linux/Mac).
  2. Criar `scripts/check_health.py` que testa rapidamente se:
     - O banco SQLite existe e possui plantas cadastradas.
     - O modelo de IA carrega sem exceções.
     - Todas as pastas (`uploads/`, `frontend/`) estão presentes.
  3. Criar `docs/ROTEIRO_APRESENTACAO.md` contendo um passo a passo de 5 a 10 minutos para demonstrar na aula (apresentação do problema, login, catálogo, identificação por foto na câmera, receitas e coleção).
* **Critérios de Aceite:**
  - O comando `python scripts/check_health.py` reporta "STATUS: OK - Sistema 100% pronto para demonstração".
* **Checklist do Usuário:** Ler o roteiro de apresentação e testar todos os passos que serão mostrados ao professor e colegas.

---

## 💡 Dicas de Sucesso para a Execução

1. **Ordem Sequencial:** Siga a ordem dos dias (1 a 12). Cada dia constrói os alicerces necessários para o seguinte.
2. **Ambiente Virtual Ativo:** Antes de pedir a execução de qualquer dia, garanta que seu ambiente virtual esteja ativado (`.venv\Scripts\activate` no Windows).
3. **Erros ou Ajustes:** Se notar algum detalhe que precisa de ajuste após a IA terminar um dia, diga simplesmente: *"IA, no Dia X, ajuste o seguinte detalhe: [seu comentário]"*.
