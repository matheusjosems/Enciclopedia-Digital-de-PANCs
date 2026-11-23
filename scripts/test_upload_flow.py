"""
Script de teste automatizado do serviço de Upload e Armazenamento Local de Imagens (Dia 07).
Testa:
1. Upload de imagem JPG válida (RF04, RNF08)
2. Acesso à imagem estática em /uploads/<nome>.jpg
3. Bloqueio de arquivo com extensão inválida (ex: .pdf, .txt)
4. Bloqueio de imagem corrompida / arquivo falso renomeado
5. Bloqueio de arquivo que excede o limite de 5MB (RNF08)
"""

import sys
import io
from pathlib import Path
from PIL import Image

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def gerar_imagem_em_memoria(formato="JPEG", largura=200, altura=200, cor=(34, 139, 34)):
    """Gera bytes de uma imagem real válida para testes."""
    buffer = io.BytesIO()
    img = Image.new("RGB", (largura, altura), color=cor)
    img.save(buffer, format=formato)
    buffer.seek(0)
    return buffer.getvalue()


def test_modulo_upload():
    print("📸 Iniciando testes do módulo de Upload e Armazenamento Local (Dia 07)...")

    # 1. Upload de imagem JPG válida
    print("\n1️⃣ Testando upload de imagem JPG válida (POST /upload-foto)...")
    img_bytes = gerar_imagem_em_memoria("JPEG")
    resp_valido = client.post(
        "/upload-foto",
        files={"foto": ("minha_planta.jpg", img_bytes, "image/jpeg")}
    )
    assert resp_valido.status_code == 201, f"Erro: {resp_valido.text}"
    dados_upload = resp_valido.json()
    assert "filename" in dados_upload
    assert dados_upload["url"].startswith("/uploads/")
    filename = dados_upload["filename"]
    print(f"   ✅ Foto salva com sucesso com UUID: {filename} ({dados_upload['tamanho_bytes']} bytes)")

    # 2. Servir imagem estática via /uploads
    print(f"\n2️⃣ Testando servidor estático GET {dados_upload['url']}...")
    resp_estatico = client.get(dados_upload["url"])
    assert resp_estatico.status_code == 200
    assert resp_estatico.headers["content-type"] in ["image/jpeg", "image/jpg"]
    assert len(resp_estatico.content) > 0
    print("   ✅ Imagem estática acessível no navegador via HTTP 200.")

    # 3. Bloqueio de extensão inválida (.pdf)
    print("\n3️⃣ Testando bloqueio de arquivo não permitido (.pdf)...")
    resp_pdf = client.post(
        "/upload-foto",
        files={"foto": ("documento.pdf", b"%PDF-1.4...", "application/pdf")}
    )
    assert resp_pdf.status_code == 400
    assert "Extensão de arquivo inválida" in resp_pdf.json()["detail"] or "permitidas" in resp_pdf.json()["detail"]
    print("   ✅ Arquivo PDF rejeitado corretamente (HTTP 400).")

    # 4. Bloqueio de arquivo falso / imagem corrompida (ex: texto renomeado para .jpg)
    print("\n4️⃣ Testando bloqueio de imagem corrompida / arquivo falso renomeado...")
    resp_falso = client.post(
        "/upload-foto",
        files={"foto": ("virus.jpg", b"Este texto nao eh uma imagem", "image/jpeg")}
    )
    assert resp_falso.status_code == 400
    assert "corrompido" in resp_falso.json()["detail"].lower() or "inválido" in resp_falso.json()["detail"].lower()
    print("   ✅ Imagem corrompida/falsa detectada e bloqueada pelo Pillow (HTTP 400).")

    # 5. Bloqueio de arquivo maior que 5 MB (RNF08)
    print("\n5️⃣ Testando bloqueio de imagem que ultrapassa o limite de 5 MB (RNF08)...")
    # Cria bytes de 5.2 MB
    arquivo_gigante = b"X" * int(5.2 * 1024 * 1024)
    resp_oversize = client.post(
        "/upload-foto",
        files={"foto": ("foto_muito_pesada.jpg", arquivo_gigante, "image/jpeg")}
    )
    assert resp_oversize.status_code == 400
    assert "5 MB" in resp_oversize.json()["detail"] or "limite" in resp_oversize.json()["detail"].lower()
    print("   ✅ Arquivo de 5.2 MB bloqueado pelo limite de tamanho (HTTP 400).")

    # Limpeza do arquivo de teste criado
    caminho_teste = ROOT_DIR / "uploads" / filename
    if caminho_teste.exists():
        caminho_teste.unlink()
        print(f"\n🧹 Arquivo temporário de teste ({filename}) limpo da pasta uploads/.")

    print("\n" + "=" * 55)
    print("🎉 TODOS OS TESTES DO DIA 07 PASSARAM COM 100% DE SUCESSO!")
    print("=" * 55)


if __name__ == "__main__":
    test_modulo_upload()
