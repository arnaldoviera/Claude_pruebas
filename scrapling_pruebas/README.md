# Pruebas de Scrapling

[Scrapling](https://github.com/D4Vinci/Scrapling) (probado con v0.4.15) es una
librería de Python para extraer datos de páginas web.

```bash
pip install "scrapling[fetchers]"
scrapling install        # descarga los navegadores (para DynamicFetcher/StealthyFetcher)
```

| Script | Qué prueba |
|---|---|
| `prueba_fetcher.py` | `Fetcher` (HTTP que imita al navegador), selectores CSS/XPath, búsqueda por texto, `find_similar` y el modo **adaptive** |
| `prueba_dinamico.py` | `DynamicFetcher` (Chromium) contra una página que arma su contenido con JavaScript |

```bash
python prueba_fetcher.py
python prueba_dinamico.py
# si ya tenés un Chromium y no querés correr `scrapling install`:
CHROMIUM_PATH=/ruta/a/chrome python prueba_dinamico.py
```

## Qué observamos

- **Fetcher**: rápido y sin navegador; sirve para HTML estático. En la versión
  JavaScript de la página ve 0 citas, mientras que `DynamicFetcher` ve las 10.
- **Adaptive**: con `auto_save=True` guarda la "huella" de un elemento. Si el
  sitio se rediseña (cambian clases y etiquetas), `css(..., adaptive=True)`
  lo reencuentra aunque el selector viejo ya no matchee.
- **API 0.4.x**: no existe `css_first`; usar `.css(...).get()` / `.first`.
- **CLI**: `scrapling extract get URL salida.md --css-selector ".quote"` baja
  y convierte a Markdown sin escribir código. También trae `scrapling shell`
  (consola interactiva) y `scrapling mcp` (servidor MCP para usarlo desde Claude).
