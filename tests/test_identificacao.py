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


def test_identificacao_baixa_confianca_rnf07(client):
    """Imagem sem características botânicas deve sinalizar baixa confiança (RNF07) mantendo aviso RF14."""
    img_bytes = criar_imagem_rgb((10, 10, 10))
    resp = client.post(
        "/identificacoes",
        files={"foto": ("IMG_escura.jpg", img_bytes, "image/jpeg")}
    )
    assert resp.status_code == 200
    dados = resp.json()
    assert dados["baixa_confianca"] is True
    assert dados["confianca"] < 60.0
    assert dados["aviso_confianca"]
    assert "ATENÇÃO" in dados["aviso_seguranca"]


def test_identificacao_png_e_arquivo_estatico(client):
    """Aceita PNG válido (RNF08) e serve a imagem salva na rota estática /uploads."""
    buffer = io.BytesIO()
    Image.new("RGBA", (200, 200), color=(40, 120, 45, 255)).save(buffer, format="PNG")
    buffer.seek(0)

    resp = client.post(
        "/identificacoes",
        files={"foto": ("folha.png", buffer.getvalue(), "image/png")}
    )
    assert resp.status_code == 200
    url_foto = resp.json()["foto_enviada_url"]
    assert url_foto.startswith("/uploads/")

    resp_img = client.get(url_foto)
    assert resp_img.status_code == 200
    assert resp_img.headers["content-type"].startswith("image/")


def test_identificacao_arquivo_acima_5mb_bloqueado_400(client):
    """Arquivo acima de 5 MB deve ser rejeitado com HTTP 400 (RNF08)."""
    conteudo_grande = b"\xff\xd8\xff" + (b"0" * (5 * 1024 * 1024 + 100))
    resp = client.post(
        "/identificacoes",
        files={"foto": ("gigante.jpg", conteudo_grande, "image/jpeg")}
    )
    assert resp.status_code == 400
    assert "5 mb" in resp.json()["detail"].lower()


def test_upload_foto_endpoint_auxiliar(client):
    """Endpoint auxiliar POST /upload-foto deve validar e salvar imagem local."""
    img_bytes = criar_imagem_rgb((50, 130, 55))
    resp = client.post(
        "/upload-foto",
        files={"foto": ("amostra.jpg", img_bytes, "image/jpeg")}
    )
    assert resp.status_code == 201
    dados = resp.json()
    assert dados["url"].startswith("/uploads/")
    assert dados["tamanho_bytes"] > 0
    assert client.get(dados["url"]).status_code == 200
