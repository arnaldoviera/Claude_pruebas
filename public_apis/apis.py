#!/usr/bin/env python3
"""Catálogo local de github.com/public-apis/public-apis.

Sin dependencias: solo la biblioteca estándar de Python 3.8+.

Uso:
    python apis.py actualizar                 # baja el README y regenera catalogo.json
    python apis.py categorias                 # lista categorías con su cantidad
    python apis.py buscar clima               # busca en nombre y descripción
    python apis.py buscar --categoria Weather --sin-auth
    python apis.py llamar "https://api.agify.io/?name=arnaldo"
"""
import argparse
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

README_URL = "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md"
CATALOGO = Path(__file__).with_name("catalogo.json")
FILA = re.compile(r"^\|\s*\[(?P<nombre>[^\]]+)\]\((?P<url>[^)]+)\)\s*\|(?P<resto>.*)\|\s*$")


def _limpiar(valor):
    valor = valor.strip().strip("`")
    return "" if valor in ("", "–", "-") else valor


def parsear_readme(texto):
    apis, categoria = [], None
    for linea in texto.splitlines():
        if linea.startswith("### "):
            categoria = linea[4:].strip()
            continue
        m = FILA.match(linea)
        if not (m and categoria):
            continue
        celdas = [c.strip() for c in m["resto"].split("|")]
        if len(celdas) < 4:
            continue
        descripcion, auth, https, cors = celdas[:4]
        auth = _limpiar(auth)
        apis.append({
            "nombre": m["nombre"].strip(),
            "url": m["url"].strip(),
            "categoria": categoria,
            "descripcion": descripcion,
            "auth": "" if auth.lower() == "no" else auth,
            "https": _limpiar(https).lower() == "yes",
            "cors": _limpiar(cors).lower() or "unknown",
        })
    return apis


def cargar():
    if not CATALOGO.exists():
        sys.exit("No hay catalogo.json: corré `python apis.py actualizar` primero.")
    return json.loads(CATALOGO.read_text(encoding="utf-8"))


def cmd_actualizar(_):
    with urllib.request.urlopen(README_URL, timeout=30) as r:
        apis = parsear_readme(r.read().decode("utf-8"))
    CATALOGO.write_text(json.dumps(apis, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(apis)} APIs guardadas en {CATALOGO}")


def cmd_categorias(_):
    for cat, n in sorted(Counter(a["categoria"] for a in cargar()).items()):
        print(f"{n:4}  {cat}")


def cmd_buscar(args):
    texto = (args.texto or "").lower()
    res = [
        a for a in cargar()
        if (not texto or texto in a["nombre"].lower() or texto in a["descripcion"].lower())
        and (not args.categoria or args.categoria.lower() in a["categoria"].lower())
        and (not args.sin_auth or not a["auth"])
        and (not args.https or a["https"])
        and (not args.cors or a["cors"] == "yes")
    ]
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return
    for a in res[: args.limite]:
        auth = a["auth"] or "sin auth"
        print(f"- {a['nombre']} [{a['categoria']}] ({auth})\n    {a['descripcion']}\n    {a['url']}")
    print(f"\n{len(res)} resultado(s)" + (f", mostrando {args.limite}" if len(res) > args.limite else ""))


def cmd_llamar(args):
    req = urllib.request.Request(args.url, headers={"User-Agent": "catalogo-public-apis/1.0"})
    with urllib.request.urlopen(req, timeout=args.timeout) as r:
        cuerpo = r.read().decode("utf-8", errors="replace")
    try:
        print(json.dumps(json.loads(cuerpo), ensure_ascii=False, indent=2))
    except ValueError:
        print(cuerpo)


def main():
    p = argparse.ArgumentParser(description="Catálogo local de public-apis")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("actualizar", help="regenera catalogo.json desde GitHub").set_defaults(f=cmd_actualizar)
    sub.add_parser("categorias", help="lista categorías").set_defaults(f=cmd_categorias)
    b = sub.add_parser("buscar", help="busca APIs")
    b.add_argument("texto", nargs="?")
    b.add_argument("--categoria")
    b.add_argument("--sin-auth", action="store_true", help="solo APIs que no piden key")
    b.add_argument("--https", action="store_true", help="solo HTTPS")
    b.add_argument("--cors", action="store_true", help="solo con CORS (usables desde el navegador)")
    b.add_argument("--limite", type=int, default=25)
    b.add_argument("--json", action="store_true", help="salida en JSON")
    b.set_defaults(f=cmd_buscar)
    l = sub.add_parser("llamar", help="hace un GET y muestra la respuesta")
    l.add_argument("url")
    l.add_argument("--timeout", type=int, default=15)
    l.set_defaults(f=cmd_llamar)
    args = p.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
