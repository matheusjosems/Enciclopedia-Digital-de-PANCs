"""
Script de diagnóstico geral do sistema (Dia 12).
Verifica:
1. Existência e integridade do banco SQLite (pancs.db) com catálogo populado (>= 60 PANCs).
2. Carregamento e execução do motor de identificação por IA sem exceções (RF05, RF14, RNF07).
3. Presença das pastas e arquivos essenciais do front-end, uploads e dados semente.
"""

import sys
import tempfile
from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from database import SessionLocal  # noqa: E402
from models.planta import Planta  # noqa: E402
from models.receita import Receita  # noqa: E402
from services.ia_service import (  # noqa: E402
    identificar_planta_ia,
    avaliar_confianca,
    AVISO_SEGURANCA_OBRIGATORIO,
)


def verificar_sistema() -> int:
    print("🩺 Iniciando diagnóstico de saúde — Enciclopédia Digital de PANCs\n")
    erros = []

    # 1. Verificação de pastas e arquivos obrigatórios
    caminhos_obrigatorios = [
        ROOT_DIR / "pancs.db",
        ROOT_DIR / "uploads",
        ROOT_DIR / "data" / "pancs_seed.json",
        ROOT_DIR / "frontend" / "index.html",
        ROOT_DIR / "frontend" / "login.html",
        ROOT_DIR / "frontend" / "planta.html",
        ROOT_DIR / "frontend" / "identificar.html",
        ROOT_DIR / "frontend" / "colecao.html",
        ROOT_DIR / "frontend" / "perfil.html",
        ROOT_DIR / "frontend" / "app.js",
        ROOT_DIR / "frontend" / "styles.css",
    ]
    for caminho in caminhos_obrigatorios:
        if not caminho.exists():
            erros.append(f"Caminho ausente: {caminho.relative_to(ROOT_DIR)}")
    print("1️⃣ Estrutura de pastas e front-end:", "OK" if not erros else "FALHA")

    # 2. Verificação do banco SQLite
    db = SessionLocal()
    try:
        total_plantas = db.query(Planta).count()
        total_receitas = db.query(Receita).count()
        print(f"2️⃣ Banco SQLite (pancs.db): {total_plantas} planta(s), {total_receitas} receita(s)")
        if total_plantas < 60:
            erros.append(f"Catálogo incompleto: {total_plantas} plantas encontradas (esperado >= 60).")
        if total_receitas < 1:
            erros.append("Nenhuma receita cadastrada no banco de dados.")

        # 3. Verificação do módulo de IA
        if total_plantas > 0:
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                Image.new("RGB", (200, 200), color=(40, 110, 45)).save(tmp_path, format="JPEG")
                planta, confianca, alternativas = identificar_planta_ia(
                    caminho_imagem=tmp_path,
                    db=db,
                    nome_original_arquivo="ora_pro_nobis.jpg",
                )
                baixa_conf, _ = avaliar_confianca(confianca)
                assert planta.id_planta > 0
                assert "ATENÇÃO" in AVISO_SEGURANCA_OBRIGATORIO
                print(
                    f"3️⃣ Motor de IA: OK ({planta.nome_popular}, confiança {confianca}%, "
                    f"baixa_confiança={baixa_conf}, {len(alternativas)} alternativas)"
                )
            finally:
                tmp_path.unlink(missing_ok=True)
    except Exception as exc:
        erros.append(f"Erro ao validar banco ou IA: {exc}")
    finally:
        db.close()

    print()
    if erros:
        print("STATUS: ERRO - Pendências encontradas:")
        for e in erros:
            print(f"  - {e}")
        return 1

    print("STATUS: OK - Sistema 100% pronto para demonstração")
    return 0


if __name__ == "__main__":
    raise SystemExit(verificar_sistema())
