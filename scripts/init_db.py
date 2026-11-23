"""
Script para inicializar e validar o banco de dados SQLite (pancs.db).
Cria todas as tabelas conforme o diagrama ER e os modelos SQLAlchemy.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path para importações locais
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import engine, Base
import models  # Garante que todos os modelos ORM sejam registrados nos metadados
from sqlalchemy import inspect


def init_database():
    print("🌿 Inicializando o banco de dados SQLite (pancs.db)...")
    
    # Cria todas as tabelas mapeadas em models
    Base.metadata.create_all(bind=engine)
    
    # Inspeciona as tabelas criadas no banco
    inspector = inspect(engine)
    tabelas = inspector.get_table_names()
    
    print("\n✅ Banco de dados criado com sucesso!")
    print(f"📊 Total de tabelas encontradas: {len(tabelas)}")
    print("-" * 50)
    
    for tabela in sorted(tabelas):
        colunas = [c["name"] for c in inspector.get_columns(tabela)]
        pk = inspector.get_pk_constraint(tabela)["constrained_columns"]
        fks = inspector.get_foreign_keys(tabela)
        
        fk_str = ", ".join([f"{fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}" for fk in fks])
        print(f"📁 Tabela: {tabela}")
        print(f"   🔑 Chave Primária (PK): {pk}")
        print(f"   📋 Colunas: {', '.join(colunas)}")
        if fk_str:
            print(f"   🔗 Chaves Estrangeiras (FK): {fk_str}")
        print("-" * 50)


if __name__ == "__main__":
    init_database()
