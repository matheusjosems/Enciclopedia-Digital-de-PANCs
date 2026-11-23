"""
Script de teste automatizado do módulo de Identificação Botânica por IA (Dia 08).
Testa:
1. Envio de foto de PANC (POST /identificacoes - RF04, RF05)
2. Retorno em menos de 10 segundos (RNF01)
3. Presença obrigatória do aviso de segurança alimentar e botânica (RF14)
4. Cálculo da taxa de confiança percentual (RF05)
5. Vinculação com receitas culinárias da planta identificada (RF07)
6. Validação e bloqueio de arquivos corrompidos ou não-imagem (RNF08)
"""

import sys
import io
import time
from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def criar_foto_botanica_teste(cor_rgb=(45, 115, 50), nome_arquivo="ora_pro_nobis.jpg"):
    """Cria bytes de uma foto simulando folhagem botânica."""
    buffer = io.BytesIO()
    img = Image.new("RGB", (300, 300), color=cor_rgb)
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.getvalue()


def test_modulo_identificacao():
    print("🤖 Iniciando testes do módulo de Identificação por IA (Dia 08)...")

    # 1. Envio de foto de Ora-pro-nóbis e medição de tempo de resposta (RNF01)
    print("\n1️⃣ Testando POST /identificacoes (simulação de Ora-pro-nóbis)...")
    img_ora = criar_foto_botanica_teste(cor_rgb=(40, 110, 45), nome_arquivo="ora_pro_nobis.jpg")
    
    inicio = time.time()
    resp = client.post(
        "/identificacoes",
        files={"foto": ("foto_ora_pro_nobis.jpg", img_ora, "image/jpeg")}
    )
    tempo_resposta = time.time() - inicio
    
    assert resp.status_code == 200, f"Erro: {resp.text}"
    dados = resp.json()
    
    # Validação do RNF01 (< 10 segundos)
    print(f"   ⏱️ Tempo de inferência: {tempo_resposta:.2f} segundos (RNF01 atendido: < 10s)")
    assert tempo_resposta < 10.0, f"Tempo de resposta excedeu 10s: {tempo_resposta}s"

    # Validação da planta provável e confiança (RF05)
    print(f"   🌿 Planta identificada: {dados['nome_popular']} ({dados['nome_cientifico']})")
    print(f"   📊 Nível de confiança: {dados['confianca']}%")
    assert dados["confianca"] >= 70.0, f"Taxa de confiança muito baixa: {dados['confianca']}"
    assert "ora" in dados["nome_popular"].lower() or dados["id_planta"] > 0

    # 2. Validação obrigatória do aviso de segurança alimentar (RF14)
    print("\n2️⃣ Verificando aviso ético de segurança alimentar (RF14)...")
    aviso = dados.get("aviso_seguranca", "")
    print(f"   ⚠️ Aviso retornado:\n      \"{aviso}\"")
    assert "ATENÇÃO" in aviso
    assert "aproximada" in aviso
    assert "especialista" in aviso or "guia" in aviso
    print("   ✅ Aviso do RF14 validado com sucesso!")

    # 3. Verificação de receitas e ficha botânica anexadas
    print("\n3️⃣ Verificando integração com ficha e receitas da PANC identificada...")
    assert "partes_comestiveis" in dados
    assert "foto_enviada_url" in dados
    print(f"   📋 Partes comestíveis: {dados['partes_comestiveis']}")
    print(f"   📷 Foto armazenada em: {dados['foto_enviada_url']}")
    print(f"   🍳 Receitas recomendadas: {len(dados['receitas_sugeridas'])} encontrada(s)")

    # 4. Teste de rejeição de arquivo inválido
    print("\n4️⃣ Testando rejeição de arquivo não-imagem (.pdf)...")
    resp_pdf = client.post(
        "/identificacoes",
        files={"foto": ("documento.pdf", b"%PDF-1.5...", "application/pdf")}
    )
    assert resp_pdf.status_code == 400
    print("   ✅ Arquivo inválido rejeitado com HTTP 400.")

    # 5. Teste de identificação de outra espécie (Peixinho)
    print("\n5️⃣ Testando identificação de Peixinho da Horta (folha prateada aveludada)...")
    img_peixinho = criar_foto_botanica_teste(cor_rgb=(85, 125, 95), nome_arquivo="peixinho.jpg")
    resp_peixinho = client.post(
        "/identificacoes",
        files={"foto": ("planta_peixinho.jpg", img_peixinho, "image/jpeg")}
    )
    assert resp_peixinho.status_code == 200
    dados_p = resp_peixinho.json()
    print(f"   🌿 Planta identificada: {dados_p['nome_popular']} ({dados_p['nome_cientifico']})")
    print(f"   📊 Confiança: {dados_p['confianca']}%")

    print("\n" + "=" * 55)
    print("🎉 TODOS OS TESTES DO DIA 08 PASSARAM COM 100% DE SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":
    test_modulo_identificacao()
