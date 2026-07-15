# -*- coding: utf-8 -*-
"""Convierte todas las fotos referenciadas en productos.json a WebP, achicando
la resolucion a un maximo razonable para verse bien en la web (incluida la
version agrandada del modal). Esto es lo que explica que la pagina tardara
tanto: se estaban sirviendo PNGs de varios MB a resolucion original del PDF
para simplemente mostrar una miniatura de 360px.
"""
import json
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
productos_path = BASE / "productos.json"
productos = json.loads(productos_path.read_text(encoding="utf-8"))

MAX_DIM = 1800  # alcanza de sobra para el modal ampliado y pantallas retina
QUALITY = 78

convertidos = {}


def convertir(rel_path):
    if not rel_path:
        return rel_path
    if rel_path in convertidos:
        return convertidos[rel_path]

    src = BASE / rel_path
    if not src.exists():
        print(f"  AVISO: no encontrado, se deja igual -> {rel_path}")
        convertidos[rel_path] = rel_path
        return rel_path

    dest_rel = str(Path(rel_path).with_suffix(".webp")).replace("\\", "/")
    dest = BASE / dest_rel

    im = Image.open(src).convert("RGB")
    w, h = im.size
    scale = min(1.0, MAX_DIM / max(w, h))
    if scale < 1.0:
        im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    im.save(dest, "WEBP", quality=QUALITY, method=6)

    original_size = src.stat().st_size
    new_size = dest.stat().st_size
    print(f"  {rel_path}: {original_size/1024:.0f}KB -> {dest_rel}: {new_size/1024:.0f}KB")

    if src.resolve() != dest.resolve():
        src.unlink()

    convertidos[rel_path] = dest_rel
    return dest_rel


total_antes = 0
for p in productos:
    total_antes += 1

print(f"Convirtiendo fotos de {len(productos)} productos...")
for p in productos:
    p["foto_ambientacion"] = convertir(p.get("foto_ambientacion"))
    p["fotos_adicionales"] = [convertir(x) for x in p.get("fotos_adicionales", [])]
    p["iconos_extra"] = [convertir(x) for x in p.get("iconos_extra", [])]

productos_path.write_text(json.dumps(productos, ensure_ascii=False, indent=2), encoding="utf-8")
print("productos.json actualizado con las nuevas rutas .webp")
