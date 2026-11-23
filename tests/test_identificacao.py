"""
Testes automatizados do grupo de Identificação por IA & Uploads (API 4).
Requisitos: RF04, RF05, RF14, RNF01, RNF07, RNF08.
"""

import io
from PIL import Image


def criar_imagem_rgb(cor=(40, 110, 45)):
    buffer = io.BytesIO()
    img = Image.new("RGB", (250, 250), color=cor)
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.getvalue()


def test_identificacao_foto_valida(client):
    img_bytes = criar_imagem_rgb((40, 110, 45))
    resp = client.post(
        "/identificacoes",
        files={"foto": ("foto_planta_teste.jpg", img_bytes, "image/jpeg")}
    )
    assert resp.status_code == 200
    dados = resp.json()
    assert dados["id_planta"] > 0
    assert dados["nome_popular"]
    assert dados["nome_cientifico"]
    assert dados["confianca"] >= 50.0
    assert dados["foto_enviada_url"].startswith("/uploads/")


def test_identificacao_aviso_seguranca_rf14(client):
    img_bytes = criar_imagem_rgb((80, 120, 90))
    resp = client.post(
        "/identificacoes",
        files={"foto": ("peixinho_teste.jpg", img_bytes, "image/jpeg")}
    )
    assert resp.status_code == 200
    dados = resp.json()
    aviso = dados.get("aviso_seguranca", "")
    assert "ATENÇÃO" in aviso
    assert "aproximada" in aviso
    assert "especialista" in aviso or "guia" in aviso


def test_identificacao_arquivo_invalido_pdf(client):
    resp = client.post(
        "/identificacoes",
        files={"foto": ("manual.pdf", b"%PDF-1.4...", "application/pdf")}
    )
    assert resp.status_code == 400
    assert "extensão" in resp.json()["detail"].lower() or "jpg" in resp.json()["detail"].lower()


def test_identificacao_imagem_corrompida(client):
    resp = client.post(
        "/identificacoes",
        files={"foto": ("falsa.jpg", b"arquivo que nao e imagem", "image/jpeg")}
    )
    assert resp.status_code == 400
    assert "corrompido" in resp.json()["detail"].lower() or "inválido" in resp.json()["detail"].lower()
