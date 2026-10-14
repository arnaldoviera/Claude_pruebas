# Catálogo Xerjoff de FragFlex

Datos públicos de [fragflex.com](https://fragflex.com) (tienda Shopify), bajados del
endpoint `/products.json` de la colección `xerjoff`.

- `datos/variantes.csv`: una fila por variante (tamaño / tester / boxed) con precio,
  precio de lista, % de descuento, stock, ml, SKU y link.
- `datos/productos.json`: respuesta cruda de Shopify (descripciones, imágenes, etc.).

```bash
python scrape_fragflex.py --coleccion xerjoff   # refrescar (otra marca: cambiar el handle)
python test_muestra.py                           # verifica 4 variantes al azar contra el sitio en vivo
python test_muestra.py --n 10 --semilla 1        # muestra más grande y reproducible
```

Solo biblioteca estándar de Python. El script pausa 1 s entre páginas.
Un aviso de "precio cambió" en el test no es un error: el sitio actualiza precios.
