#!/usr/bin/env python3
"""Verifica en vivo una muestra al azar de lo scrapeado.

Toma N variantes de datos/variantes.csv y, para cada una, consulta el sitio:
la página del producto responde, y coinciden nombre, marca, SKU y precio.
Un precio distinto no es necesariamente un error del scraper: puede haber
cambiado desde que se bajaron los datos, por eso se informa aparte.

Uso: python test_muestra.py [--n 4] [--semilla 123]
"""
import argparse
import csv
import json
import random
import sys
import urllib.request
from pathlib import Path

CSV = Path(__file__).parent / "datos" / "variantes.csv"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (catalogo-estudio)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", errors="replace")


def verificar(fila):
    problemas, avisos = [], []
    estado, html = get(fila["url"])
    if estado != 200:
        return [f"la página respondió {estado}"], avisos
    if fila["producto"] not in html.replace("&#39;", "'").replace("&amp;", "&"):
        problemas.append("el nombre no aparece en la página")

    _, crudo = get(fila["url"] + ".json")
    vivo = json.loads(crudo)["product"]
    if vivo["title"] != fila["producto"]:
        problemas.append(f"nombre distinto: {vivo['title']!r}")
    if vivo["vendor"] != fila["marca"]:
        problemas.append(f"marca distinta: {vivo['vendor']!r}")
    variante = next((v for v in vivo["variants"] if (v.get("sku") or "") == fila["sku"]), None)
    if variante is None:
        problemas.append(f"no existe la variante con SKU {fila['sku']}")
    elif float(variante["price"]) != float(fila["precio"]):
        avisos.append(f"precio cambió: {fila['precio']} -> {variante['price']}")
    return problemas, avisos


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=4)
    p.add_argument("--semilla", type=int)
    args = p.parse_args()

    filas = list(csv.DictReader(open(CSV, encoding="utf-8")))
    muestra = random.Random(args.semilla).sample(filas, min(args.n, len(filas)))
    fallas = 0
    for f in muestra:
        problemas, avisos = verificar(f)
        marca = "FALLA" if problemas else "OK   "
        print(f"{marca} {f['variante']} | {f['sku']} | ${f['precio']} | {f['url']}")
        for x in problemas + avisos:
            print(f"      - {x}")
        fallas += bool(problemas)
    print(f"\n{len(muestra) - fallas}/{len(muestra)} verificadas OK")
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
