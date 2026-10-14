---
name: preparar-entorno
description: Use when a task needs Scrapling (web scraping in Python), the Agency agents (specialist subagents like Frontend Developer or SEO Specialist), or the Playwright browser plugin, and it may not be installed in this session. Ask the user before installing anything.
---

# Preparar entorno a pedido

Algunas herramientas no viven en el repo y se pierden al cerrar cada sesión en la
nube. No se instalan solas: se ofrecen cuando una tarea las necesita.

1. Ver qué falta: `scripts/preparar_entorno.sh estado`
2. Si falta lo que la tarea necesita, **preguntar al usuario** antes de instalar,
   diciendo qué se instala y para qué. Con un sí, correr solo esa parte:
   - `scripts/preparar_entorno.sh scrapling`
   - `scripts/preparar_entorno.sh agentes` (o solo algunas divisiones:
     `scripts/preparar_entorno.sh agentes engineering,design`). Los agentes
     se cargan recién en la sesión siguiente: avisarlo.
   - `scripts/preparar_entorno.sh playwright` si el plugin falla con
     "Chromium distribution 'chrome' is not found" o con un error de sandbox.
3. Si el usuario dice que no, seguir con lo que se pueda hacer sin esa herramienta.
