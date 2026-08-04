#!/bin/bash
cd "$(dirname "$0")"

echo "==========================================="
echo "   🔑 PISTONS HUB - INICIALIZADOR SEGURO  "
echo "==========================================="
echo "Para instalar o aplicativo no diretório do sistema (/opt),"
echo "por favor digite a sua senha do Ubuntu abaixo:"
echo ""

# Libera o servidor de vídeo X11 para o usuário root antes de abrir a janela
xhost +local:root > /dev/null 2>&1

if sudo -v; then
    echo "✅ Autenticado! Iniciando interface gráfica..."
    # O comando -E garante que as configurações de tela do seu monitor não sumam
    sudo -E python3 interface_instalador.py
else
    echo "❌ Falha na autenticação. Instalação abortada."
    exit 1
fi
