#!/usr/bin/env bash
set -e

BASE_URL="https://raw.githubusercontent.com/lkm2201/Instalador/main"
TMP_DIR="$(mktemp -d)"

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "=========================================="
echo "       PISTON HUB - INSTALADOR"
echo "=========================================="
echo

echo "[1/3] Baixando interface..."
curl -fsSL "$BASE_URL/interface_instalador.py" -o "$TMP_DIR/interface_instalador.py"

echo "[2/3] Verificando Python..."
command -v python3 >/dev/null || {
    echo "Python 3 não encontrado."
    exit 1
}

echo "[3/3] Abrindo Setup..."
exec python3 "$TMP_DIR/interface_instalador.py"
