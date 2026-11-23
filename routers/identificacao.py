from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.receita import Receita
from schemas.identificacao import IdentificacaoResponse, IdentificacaoAlternativa
from schemas.receita import ReceitaResponse
from utils.image_uploader import salvar_e_validar_imagem, UPLOADS_DIR
from services.ia_service import identificar_planta_ia, AVISO_SEGURANCA_OBRIGATORIO

router = APIRouter(tags=["Identificação por IA"])


@router.post(
    "/identificacoes",
    response_model=IdentificacaoResponse,
    summary="Identificação Botânica de PANC por Foto (RF04, RF05, RF14, RNF01, RNF07)",
    description=(
        "Recebe uma foto de planta, valida o arquivo (JPG/PNG até 5MB), executa a inferência de IA "
        "para identificar a espécie do catálogo de PANCs mais provável, calcula o nível de confiança (%) "
        "e retorna a ficha completa com sugestões culinárias e o aviso ético de segurança botânica (RF14)."
    )
)
def identificar_planta(
    foto: UploadFile = File(..., description="Foto da planta enviada pela câmera ou galeria (JPG/PNG até 5MB)"),
    db: Session = Depends(get_db)
):
    # 1. Valida e salva a imagem localmente (RF04, RNF08)
    nome_arquivo, url_foto_salva, _ = salvar_e_validar_imagem(foto)
    caminho_imagem = UPLOADS_DIR / nome_arquivo

    try:
        # 2. Executa a inferência pela IA (RF05, RNF01)
        planta, confianca, outras_alternativas = identificar_planta_ia(
            caminho_imagem=caminho_imagem,
            db=db,
            nome_original_arquivo=foto.filename or ""
        )

        # 3. Busca receitas recomendadas para a espécie identificada (RF07)
        receitas_orm = db.query(Receita).filter(Receita.id_planta == planta.id_planta).all()
        receitas_resp = [ReceitaResponse.model_validate(r) for r in receitas_orm]

        alternativas_resp = [
            IdentificacaoAlternativa(
                id_planta=alt["id_planta"],
                nome_popular=alt["nome_popular"],
                nome_cientifico=alt["nome_cientifico"],
                confianca=alt["confianca"]
            )
            for alt in outras_alternativas
        ]

        # 4. Retorna a resposta completa com o aviso obrigatório do RF14
        return IdentificacaoResponse(
            id_planta=planta.id_planta,
            nome_popular=planta.nome_popular,
            nome_cientifico=planta.nome_cientifico,
            familia=planta.familia,
            confianca=confianca,
            foto_enviada_url=url_foto_salva,
            aviso_seguranca=AVISO_SEGURANCA_OBRIGATORIO,
            descricao=planta.descricao,
            partes_comestiveis=planta.partes_comestiveis,
            cuidados=planta.cuidados,
            receitas_sugeridas=receitas_resp,
            outras_possibilidades=alternativas_resp
        )

    except Exception as err:
        # Fallback de Confiabilidade (RNF07): caso ocorra qualquer instabilidade no processamento
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Não foi possível processar a imagem da planta no momento: {str(err)}. Tente novamente com outra foto."
        )
