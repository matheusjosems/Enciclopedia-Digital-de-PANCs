import os
import uuid
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException, status
from PIL import Image

# Diretório raiz para armazenamento das fotos
UPLOADS_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Limite máximo de 5 MB conforme requisito RNF08
TAMANHO_MAXIMO_BYTES = 5 * 1024 * 1024  # 5 MB

# Extensões e tipos MIME permitidos
EXTENSOES_PERMITIDAS = {".jpg", ".jpeg", ".png"}
MIME_PERMITIDOS = {"image/jpeg", "image/png", "image/pjpeg", "image/x-png"}


def salvar_e_validar_imagem(arquivo: UploadFile) -> Tuple[str, str, int]:
    """
    Valida a imagem conforme RNF08:
    1. Verifica a extensão (.jpg, .jpeg, .png)
    2. Valida o tipo MIME
    3. Valida o tamanho máximo de 5MB
    4. Valida a integridade real da imagem com Pillow
    5. Salva no disco com UUID único e otimiza para RGB JPEG
    Retorna: (nome_arquivo, url_relativa, tamanho_bytes)
    """
    nome_original = arquivo.filename or ""
    extensao = Path(nome_original).suffix.lower()

    # 1. Validação de extensão
    if extensao not in EXTENSOES_PERMITIDAS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extensão de arquivo inválida '{extensao}'. Apenas imagens JPG, JPEG e PNG são permitidas (RNF08)."
        )

    # 2. Validação de tipo MIME
    if arquivo.content_type and arquivo.content_type.lower() not in MIME_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de mídia inválido '{arquivo.content_type}'. O arquivo deve ser uma imagem válida JPG ou PNG."
        )

    # Lê o conteúdo do arquivo em memória
    conteudo = arquivo.file.read()
    tamanho = len(conteudo)

    # 3. Validação de tamanho (máximo 5MB)
    if tamanho > TAMANHO_MAXIMO_BYTES:
        tamanho_mb = tamanho / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O arquivo enviado tem {tamanho_mb:.2f} MB. O limite máximo permitido é de 5 MB (RNF08)."
        )

    if tamanho == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo enviado está vazio."
        )

    # 4. Validação botânica/visual com Pillow (garante que não é um malware com extensão renomeada)
    import io
    try:
        imagem = Image.open(io.BytesIO(conteudo))
        imagem.verify()  # Valida integridade do cabeçalho
        # Reabre para manipulação
        imagem = Image.open(io.BytesIO(conteudo))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo de imagem corrompido ou inválido. Envie uma foto válida."
        )

    # 5. Geração de nome único com UUID4
    nome_seguro = f"{uuid.uuid4().hex}.jpg"
    caminho_final = UPLOADS_DIR / nome_seguro

    # Converte para RGB e salva como JPEG otimizado
    if imagem.mode in ("RGBA", "P"):
        imagem = imagem.convert("RGB")

    imagem.save(caminho_final, format="JPEG", quality=85, optimize=True)

    tamanho_final = os.path.getsize(caminho_final)
    url_relativa = f"/uploads/{nome_seguro}"

    return nome_seguro, url_relativa, tamanho_final
