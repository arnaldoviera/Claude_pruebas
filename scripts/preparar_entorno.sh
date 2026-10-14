#!/usr/bin/env bash
# Instala a pedido las herramientas que no viven en el repo.
# Uso: scripts/preparar_entorno.sh scrapling | agentes [divisiones] | playwright | estado
#   agentes sin divisiones instala todo The Agency; p. ej.: agentes engineering,design
set -euo pipefail

estado() {
  python3 -c "import scrapling" 2>/dev/null && echo "scrapling: instalado" || echo "scrapling: falta"
  n=$(ls ~/.claude/agents 2>/dev/null | wc -l); echo "agentes: $n instalados"
  if [ -x /opt/google/chrome/chrome ] || ! [ -e /opt/pw-browsers/chromium ]; then
    echo "playwright: no necesita ajuste"
  else
    echo "playwright: falta ajuste de Chromium"
  fi
}

case "${1:-estado}" in
  scrapling)
    pip install -q "scrapling[fetchers]"
    echo "Scrapling $(pip show scrapling | sed -n 's/^Version: //p') instalado."
    echo "Para DynamicFetcher en la nube: CHROMIUM_PATH=/opt/pw-browsers/chromium" ;;
  agentes)
    dir=$(mktemp -d)
    git clone -q --depth 1 https://github.com/msitarzewski/agency-agents "$dir"
    if [ -n "${2:-}" ]; then
      "$dir/scripts/install.sh" --tool claude-code --division "$2" </dev/null
    else
      "$dir/scripts/install.sh" --tool claude-code </dev/null
    fi
    rm -rf "$dir"
    echo "Los agentes nuevos se cargan al iniciar la próxima sesión." ;;
  playwright)
    # Solo en el contenedor de la nube: el plugin busca Google Chrome y corre como root.
    if [ -e /opt/pw-browsers/chromium ] && ! [ -x /opt/google/chrome/chrome ]; then
      mkdir -p /opt/google/chrome
      printf '#!/bin/sh\nexec /opt/pw-browsers/chromium --no-sandbox "$@"\n' > /opt/google/chrome/chrome
      chmod +x /opt/google/chrome/chrome
      echo "Ajuste de Chromium aplicado."
    else
      echo "No hace falta ajuste (Chrome ya existe o no es el contenedor de la nube)."
    fi ;;
  estado) estado ;;
  *) echo "Opción desconocida: $1"; exit 1 ;;
esac
