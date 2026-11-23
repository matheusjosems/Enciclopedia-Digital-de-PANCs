"""
Script de Carga de Dados (Seed das 63 PANCs).
Lê o dataset consolidado data/pancs_seed.json e popula o banco de dados pancs.db
com todas as plantas, regiões, sazonalidades e receitas culinárias.
Possui suporte para execução idempotente (não duplica dados ao rodar novamente).
"""

import sys
import json
import argparse
from pathlib import Path

# Adiciona a raiz do projeto ao path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from database import engine, SessionLocal, Base
from models import Planta, Regiao, Receita, PlantaSazonalidade, planta_regiao
from sqlalchemy import select, func


DATA_FILE = ROOT_DIR / "data" / "pancs_seed.json"


def carregar_dados():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de dados '{DATA_FILE}' não encontrado! "
            "Execute primeiramente 'python scripts/extract_seed_data.py' para extrair os dados."
        )
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_database():
    print("🌱 Iniciando o processo de carga (seed) no banco pancs.db...")
    
    # Garante que as tabelas existam
    Base.metadata.create_all(bind=engine)
    
    dados = carregar_dados()
    print(f"📦 Total de plantas no arquivo seed: {len(dados)}")
    
    db = SessionLocal()
    try:
        novas_plantas = 0
        novas_regioes = 0
        novas_receitas = 0
        novas_sazonalidades = 0
        
        # Cache de regiões existentes em memória para performance
        regioes_db = {r.nome.lower(): r for r in db.query(Regiao).all()}
        
        for item in dados:
            nc = item["nome_cientifico"].strip()
            np = item["nome_popular"].strip()
            
            # 1. Verifica se a planta já existe pelo nome científico
            planta = db.query(Planta).filter(Planta.nome_cientifico == nc).first()
            if not planta:
                planta = Planta(
                    nome_popular=np,
                    nome_cientifico=nc,
                    familia=item.get("familia") or "Não informada",
                    descricao=item.get("descricao") or "",
                    partes_comestiveis=item.get("partes_comestiveis") or "Folhas e frutos",
                    cuidados=item.get("cuidados") or "Confirmar identificação botânica antes do consumo.",
                    sabor=item.get("sabor") or "Característico",
                    foto_url=item.get("foto_url") or ""
                )
                db.add(planta)
                db.flush()  # Gera o id_planta
                novas_plantas += 1
            else:
                # Atualiza campos se estavam vazios
                if not planta.foto_url and item.get("foto_url"):
                    planta.foto_url = item.get("foto_url")
                if not planta.sabor and item.get("sabor"):
                    planta.sabor = item.get("sabor")
                    
            # 2. Regiões e Associação planta_regiao
            for reg_info in item.get("regioes", []):
                r_nome = reg_info["nome"].strip()
                r_tipo = reg_info.get("tipo", "Bioma")
                
                reg_obj = regioes_db.get(r_nome.lower())
                if not reg_obj:
                    reg_obj = Regiao(nome=r_nome, tipo=r_tipo)
                    db.add(reg_obj)
                    db.flush()
                    regioes_db[r_nome.lower()] = reg_obj
                    novas_regioes += 1
                    
                if reg_obj not in planta.regioes:
                    planta.regioes.append(reg_obj)
                    
            # 3. Sazonalidade
            for mes in item.get("meses_sazonalidade", []):
                saz_existe = db.query(PlantaSazonalidade).filter_by(
                    id_planta=planta.id_planta,
                    mes=mes
                ).first()
                if not saz_existe:
                    saz = PlantaSazonalidade(id_planta=planta.id_planta, mes=mes)
                    db.add(saz)
                    novas_sazonalidades += 1
                    
            # 4. Receitas
            for rec_info in item.get("receitas", []):
                titulo = rec_info["titulo"].strip()
                rec_existe = db.query(Receita).filter_by(
                    id_planta=planta.id_planta,
                    titulo=titulo
                ).first()
                if not rec_existe:
                    rec = Receita(
                        id_planta=planta.id_planta,
                        titulo=titulo,
                        ingredientes=rec_info.get("ingredientes", "Ingredientes frescos a gosto."),
                        modo_preparo=rec_info.get("modo_preparo", "Higienizar e preparar refogado ou cozido."),
                        tempo_preparo=rec_info.get("tempo_preparo", "15 minutos"),
                        rendimento=rec_info.get("rendimento", "2 a 4 porções")
                    )
                    db.add(rec)
                    novas_receitas += 1
                    
        db.commit()
        
        # Estatísticas finais no banco
        total_plantas = db.query(func.count(Planta.id_planta)).scalar()
        total_receitas = db.query(func.count(Receita.id_receita)).scalar()
        total_regioes = db.query(func.count(Regiao.id_regiao)).scalar()
        total_sazonalidades = db.query(func.count(PlantaSazonalidade.id_planta)).scalar()
        
        print("\n" + "=" * 55)
        print("✅ CARGA DE DADOS CONCLUÍDA COM SUCESSO!")
        print("=" * 55)
        print(f"🌿 Novas plantas cadastradas nesta execução: {novas_plantas}")
        print(f"📖 Novas receitas cadastradas: {novas_receitas}")
        print(f"🗺️ Novas regiões cadastradas: {novas_regioes}")
        print(f"📅 Novas sazonalidades cadastradas: {novas_sazonalidades}")
        print("-" * 55)
        print("📊 TOTAIS NO BANCO pancs.db:")
        print(f"   🌿 Total de Plantas: {total_plantas}")
        print(f"   📖 Total de Receitas: {total_receitas}")
        print(f"   🗺️ Total de Regiões: {total_regioes}")
        print(f"   📅 Total de Vínculos de Sazonalidade: {total_sazonalidades}")
        print("=" * 55)
        
        # Verificação do critério de aceite
        assert total_plantas >= 60, f"Critério de aceite falhou: esperado >= 60 plantas, obtido {total_plantas}"
        print(f"🎯 Critério de Aceite Atendido: {total_plantas} plantas catalogadas (>= 60)!")
        
        # Teste de verificação das plantas clássicas
        ora = db.query(Planta).filter(Planta.nome_popular.ilike("%ora-pro-nóbis%")).first()
        peixinho = db.query(Planta).filter(Planta.nome_popular.ilike("%peixinho%")).first()
        
        if ora:
            print(f"   ⭐ Verificado: Ora-pro-nóbis ({ora.nome_cientifico}) - {len(ora.receitas)} receita(s)")
        if peixinho:
            print(f"   ⭐ Verificado: Peixinho ({peixinho.nome_cientifico}) - {len(peixinho.receitas)} receita(s)")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Erro durante o seed do banco de dados: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed do Banco de Dados de PANCs")
    parser.add_argument("--scrape", action="store_true", help="Força a raspagem online novamente antes do seed")
    args = parser.parse_args()
    
    if args.scrape:
        from scripts.extract_seed_data import scrape_all
        scrape_all()
        
    seed_database()
