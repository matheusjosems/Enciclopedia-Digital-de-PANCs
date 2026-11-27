from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioResponse, TokenResponse, UsuarioLogin
from core.security import hash_senha, verificar_senha, criar_token_acesso

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/cadastro",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastro de Novo Usuário (RF01)",
    description="Cria uma nova conta no sistema com nome, e-mail único e senha criptografada com bcrypt."
)
def cadastrar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db)
):
    # Verifica duplicidade de e-mail
    if db.query(Usuario).filter(Usuario.email == dados.email.strip().lower()).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário cadastrado com este e-mail."
        )

    # Verifica duplicidade de nome de usuário
    if db.query(Usuario).filter(Usuario.nome == dados.nome.strip()).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este nome de usuário já está em uso."
        )

    if len(dados.senha) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha deve ter no mínimo 6 caracteres."
        )

    novo_usuario = Usuario(
        nome=dados.nome.strip(),
        email=dados.email.strip().lower(),
        senha_hash=hash_senha(dados.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Autenticação e Login (RF02)",
    description="Autentica credenciais (e-mail e senha) e retorna um Bearer Token JWT para acesso a rotas privadas. Aceita JSON ou Form Data."
)
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    # Suporta requisição tanto em JSON quanto em Form Data (OAuth2 / Swagger UI)
    email = None
    senha = None
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            body = await request.json()
            email = body.get("email") or body.get("username")
            senha = body.get("senha") or body.get("password")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato JSON inválido."
            )
    else:
        # Form Data (usado pelo botão 'Authorize' do Swagger)
        form = await request.form()
        email = form.get("username") or form.get("email")
        senha = form.get("password") or form.get("senha")

    if not email or not senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail e senha são obrigatórios."
        )

    identificador = email.strip()
    usuario = db.query(Usuario).filter(
        or_(
            Usuario.email == identificador.lower(),
            Usuario.nome == identificador
        )
    ).first()

    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera token JWT contendo o e-mail no subject
    access_token = criar_token_acesso(
        dados={"sub": usuario.email, "id_usuario": usuario.id_usuario, "nome": usuario.nome}
    )

    return {"access_token": access_token, "token_type": "bearer"}
