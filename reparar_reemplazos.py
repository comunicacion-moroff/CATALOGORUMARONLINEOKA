# -*- coding: utf-8 -*-
"""Busca, para cada foto referenciada en productos.json, si el archivo .webp
esperado falta pero existe un reemplazo con el mismo nombre en otro formato
(.png/.jpg/.jpeg) -- typico de cuando alguien reemplaza una foto a mano sin
saber que ya estaban todas convertidas a webp -- y lo convierte in situ."""
import json
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
productos_path = BASE / "productos.json"
productos = json.loads(productos_path.read_text(encoding="utf-8"))

MAX_DIM = 1800
QUALITY = 78
EXTENSIONES_ALTERNATIVAS = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]

reparados = []
faltantes = []


def revisar(rel_path):
    if not rel_path:
        return
    dest = BASE / rel_path
    if dest.exists():
        return  # ya esta bien, nada que hacer

    stem = Path(rel_path).with_suffix("")
    for ext in EXTENSIONES_ALTERNATIVAS:
        candidato = BASE / (str(stem) + ext)
        if candidato.exists():
            im = Image.open(candidato).convert("RGB")
            w, h = im.size
            scale = min(1.0, MAX_DIM / max(w, h))
            if scale < 1.0:
                im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
            im.save(dest, "WEBP", quality=QUALITY, method=6)
            candidato.unlink()
            reparados.append(rel_path)
            return

    faltantes.append(rel_path)


for p in productos:
    revisar(p.get("foto_ambientacion"))
    for extra in p.get("fotos_adicionales", []):
        revisar(extra)
    for extra in p.get("iconos_extra", []):
        revisar(extra)

print(f"Reparadas: {len(reparados)}")
for r in reparados:
    print("  ", r)
if faltantes:
    print(f"\nSiguen faltando (ni .webp ni reemplazo encontrado): {len(faltantes)}")
    for f in faltantes:
        print("  ", f)
