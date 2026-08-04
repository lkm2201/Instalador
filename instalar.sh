#!/bin/bash
cd "$(dirname "$0")"

echo "==========================================="
echo "   🔑 VALIDAÇÃO DE ADMINISTRADOR (SUDO)    "
echo "==========================================="
sudo -v

# Passa a URL exata protegida por aspas simples rígidas para o Python
URL_BLINDADA='https://github.com'
python3 interface_instalador.py "$URL_BLINDADA"
