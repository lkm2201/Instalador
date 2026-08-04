#!/bin/bash
cd "$(dirname "$0")"

echo "==========================================="
echo "   🔑 PISTONS HUB - INICIALIZADOR SEGURO  "
echo "==========================================="
echo "Garantindo dependências e permissões do sistema..."
echo ""

# Libera a tela para o Root abrir a interface sem dar erro de X11 ou MESA
xhost +local:root > /dev/null 2>&1

if sudo -v; then
    echo "✅ Autenticado! Iniciando interface gráfica..."
    # Abre a interface gráfica com o python3 nativo preservando as variáveis visuais
    sudo -E python3 interface_instalador.py
else
    echo "❌ Falha na autenticação. Instalação abortada."
    exit 1
fi
