from pathlib import Path
from fastapi import APIRouter, UploadFile, File, status
from pydantic import BaseModel
from utils.image_uploader import salvar_e_validar_imagem

router = APIRouter(tags=["Uploads & Imagens"])


class UploadResponse(BaseModel):
    mensagem: str
    filename: str
    url: str
    tamanho_bytes: int


@router.post(
    "/upload-foto",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload e Validação de Foto Local (RF04, RNF08)",
    description="Recebe uma foto de PANC tirada pela câmera ou galeria, valida a extensão (JPG/PNG), tamanho máximo de 5MB e salva no servidor local com nome único."
)
def upload_foto(
    foto: UploadFile = File(..., description="Arquivo de imagem JPG ou PNG até 5MB")
):
    nome_arquivo, url_relativa, tamanho_bytes = salvar_e_validar_imagem(foto)

    return UploadResponse(
        mensagem="Foto enviada e armazenada com sucesso no servidor local.",
        filename=nome_arquivo,
        url=url_relativa,
        tamanho_bytes=tamanho_bytes
    )
