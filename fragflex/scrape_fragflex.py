#!/usr/bin/env python3
"""Baja el catálogo público de una tienda Shopify (por defecto fragflex.com).

Usa el endpoint público /products.json, de a 250 productos por página y con una
pausa entre páginas para no cargar el sitio. Solo biblioteca estándar.

Uso:
    python scrape_fragflex.py                      # fragflex.com
    python scrape_fragflex.py --coleccion xerjoff  # solo una colección/marca
    python scrape_fragflex.py --tienda otra.com    # cualquier tienda Shopify
Genera productos.json (crudo) y variantes.csv (una fila por variante).
"""
import argparse
import csv
import json
import re
import time
import urllib.request
from pathlib import Path

CAMPOS = ["producto", "marca", "tipo", "variante", "sku", "precio", "precio_lista",
          "descuento_pct", "disponible", "ml", "tags", "creado", "url"]


def bajar_pagina(tienda, pagina, coleccion=None):
    base = f"https://{tienda}/collections/{coleccion}" if coleccion else f"https://{tienda}"
    url = f"{base}/products.json?limit=250&page={pagina}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (catalogo-estudio)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["products"]


def filas(producto, tienda):
    for v in producto["variants"]:
        precio = float(v["price"])
        lista = float(v["compare_at_price"]) if v.get("compare_at_price") else None
        ml = re.search(r"(\d+(?:\.\d+)?)\s*ml", v["title"], re.I)
        yield {
            "producto": producto["title"],
            "marca": producto["vendor"],
            "tipo": producto["product_type"],
            "variante": v["title"],
            "sku": v.get("sku") or "",
            "precio": precio,
            "precio_lista": lista or "",
            "descuento_pct": round(100 * (1 - precio / lista)) if lista and lista > precio else "",
            "disponible": v["available"],
            "ml": ml.group(1) if ml else "",
            "tags": ", ".join(producto.get("tags", [])),
            "creado": producto["created_at"][:10],
            "url": f"https://{tienda}/products/{producto['handle']}",
        }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tienda", default="fragflex.com")
    p.add_argument("--coleccion", help="handle de la colección, p. ej. xerjoff (vacío = todo)")
    p.add_argument("--pausa", type=float, default=1.0, help="segundos entre páginas")
    p.add_argument("--salida", default=str(Path(__file__).parent / "datos"))
    args = p.parse_args()

    productos, pagina = [], 1
    while True:
        lote = bajar_pagina(args.tienda, pagina, args.coleccion)
        if not lote:
            break
        productos += lote
        print(f"página {pagina}: {len(lote)} productos (total {len(productos)})")
        pagina += 1
        time.sleep(args.pausa)

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "productos.json").write_text(json.dumps(productos, ensure_ascii=False), encoding="utf-8")
    with open(salida / "variantes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for prod in productos:
            w.writerows(filas(prod, args.tienda))
    print(f"Listo: {len(productos)} productos en {salida}/")


if __name__ == "__main__":
    main()
