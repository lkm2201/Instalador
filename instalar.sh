#!/bin/bash
cd "$(dirname "$0")"

echo "==========================================="
echo "   🔑 PISTONS HUB - INICIALIZADOR SEGURO  "
echo "==========================================="
echo "Garantindo dependências e permissões do sistema..."
echo ""

# 1. Libera o monitor de vídeo para evitar erros de tela com o sudo
xhost +local:root > /dev/null 2>&1

# 2. Pede a senha do sudo e instala TODAS as dependências necessárias para a interface abrir
if sudo -v; then
    echo "📦 Verificando e instalando dependências base (Git, Tkinter, Curl, Python3)..."
    
    # Atualiza a lista de pacotes e instala o Git e o Tkinter (essencial para o instalador abrir)
    sudo apt update && sudo apt install git python3-tk curl wget -y
    
    echo "✅ Tudo pronto! Iniciando interface gráfica..."
    # Executa a interface preservando o monitor do usuário
    sudo -E python3 interface_instalador.py
else
    echo "❌ Falha na autenticação. Instalação abortada."
    exit 1
fi
