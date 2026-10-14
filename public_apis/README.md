# Catálogo local de Public APIs

Copia consultable de [public-apis/public-apis](https://github.com/public-apis/public-apis):
~2.000 APIs gratuitas en 52 categorías, guardadas en `catalogo.json`.

Las APIs no se "instalan": son servicios web. Esto te deja el índice a mano para
buscarlas y probarlas desde la terminal (o desde cualquier script que lea el JSON).

Solo necesita Python 3.8+, sin dependencias.

```bash
cd public_apis
python apis.py categorias                          # categorías y cantidad
python apis.py buscar weather --sin-auth --https   # buscar por texto y filtros
python apis.py buscar --categoria Animals --cors   # usables desde el navegador
python apis.py buscar crypto --json > crypto.json  # exportar resultados
python apis.py llamar "https://api.agify.io/?name=arnaldo"   # probar una API
python apis.py actualizar                          # refrescar desde GitHub
```

Campos de cada API en `catalogo.json`: `nombre`, `url` (documentación), `categoria`,
`descripcion`, `auth` (vacío = no pide key; si no, `apiKey`, `OAuth`, …),
`https` (bool) y `cors` (`yes`/`no`/`unknown`).
