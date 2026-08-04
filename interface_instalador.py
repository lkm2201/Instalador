import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import os
import subprocess
import time
import shutil

class InstaladorPistonsHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Pistons Hub Framework Setup")
        self.root.overrideredirect(True)
        self.largura = self.root.winfo_screenwidth()
        self.altura = self.root.winfo_screenheight()
        self.root.geometry(f"{self.largura}x{self.altura}+0+0")
        
        self.bg_principal = "#0d0d0e"
        self.bg_card = "#161618"
        self.txt_claro = "#f5f5f7"
        self.txt_mutado = "#86868b"
        self.cor_acento = "#0071e3"
        self.cor_hover = "#1484ff"
        
        self.root.configure(bg=self.bg_principal)
        self.caminho_home = os.path.expanduser("~")
        self.pasta_provisoria = os.path.join(self.caminho_home, "Pistons-Baixando")
        self.pasta_sistema_apps = "/opt/Pistons-App"
        self.caminho_icone = os.path.join(self.caminho_home, "Downloads", "imagem.png")
        self.url_repositorio = "https://github.com"
        
        self.estilo = ttk.Style()
        self.estilo.theme_use('default')
        self.estilo.configure("TProgressbar", thickness=6, troughcolor="#222224", background=self.cor_acento, borderwidth=0)
        self.progresso_alvo = 0
        self.progresso_atual = 0
        
        self.construir_interface()
        self.atualizar_animacoes_loop()

    def construir_interface(self):
        self.barra_superior = tk.Frame(self.root, bg="#161618", height=45)
        self.barra_superior.pack(fill="x", side="top")
        
        self.btn_fechar = tk.Button(self.barra_superior, text="✕", font=("Segoe UI", 11), bg="#161618", fg=self.txt_claro, bd=0, activebackground="#ff3b30", padx=20, command=self.root.destroy)
        self.btn_fechar.pack(fill="y", side="right")

        self.lbl_titulo = tk.Label(self.root, text="Pistons Hub", font=("Segoe UI", 32, "bold"), bg=self.bg_principal, fg=self.txt_claro)
        self.lbl_titulo.pack(pady=(120, 5))
        
        self.card = tk.Frame(self.root, bg=self.bg_card, bd=0)
        self.card.pack(fill="both", expand=True, padx=250, pady=(0, 40))
        
        self.lbl_status = tk.Label(self.card, text="Pronto para implantar o Pistons Hub no diretório do sistema.", font=("Segoe UI", 14), bg=self.bg_card, fg=self.txt_claro, wraplength=600, justify="center")
        self.lbl_status.pack(expand=True, pady=40)
        
        self.progresso = ttk.Progressbar(self.root, mode="determinate", style="TProgressbar")
        self.progresso.pack(fill="x", padx=250, pady=(0, 40))
        
        self.btn_instalar = tk.Button(self.root, text="Iniciar Instalação", font=("Segoe UI", 12, "bold"), bg=self.cor_acento, fg=self.txt_claro, bd=0, padx=60, pady=16, command=self.iniciar_instalacao_thread)
        self.btn_instalar.pack(pady=(0, 80))

    def atualizar_status(self, texto, valor_progresso):
        self.lbl_status.config(text=texto)
        self.progresso_alvo = valor_progresso
        self.root.update_idletasks()

    def atualizar_animacoes_loop(self):
        if self.progresso_atual < self.progresso_alvo:
            self.progresso_atual += 0.5
            self.progresso['value'] = self.progresso_atual
        self.root.after(8, self.atualizar_animacoes_loop)

    def iniciar_instalacao_thread(self):
        self.btn_instalar.config(state="disabled", bg="#2c2c2e", fg=self.txt_mutado)
        threading.Thread(target=self.executar_instalacao_core, daemon=True).start()

    def executar_instalacao_core(self):
        try:
            # Remove travas antigas
            if os.path.exists(self.pasta_provisoria):
                subprocess.run(["rm", "-rf", self.pasta_provisoria])

            # ETAPA 1: Download Remoto
            self.atualizar_status("Baixando os arquivos estáveis do Pistons Hub...", 25)
            resultado = subprocess.run(["git", "clone", self.url_repositorio, self.pasta_provisoria], capture_output=True, text=True)
            if resultado.returncode != 0: raise Exception(f"Erro Git: {resultado.stderr}")

            # ETAPA 2: Alocação no diretório global do sistema (/opt)
            self.atualizar_status("Alocando o Pistons Hub na pasta global de aplicativos (/opt)...", 50)
            subprocess.run(["sudo", "rm", "-rf", self.pasta_sistema_apps], check=True)
            subprocess.run(["sudo", "mv", self.pasta_provisoria, self.pasta_sistema_apps], check=True)

            # ETAPA 3: Ambiente Sandbox e Bibliotecas no local definitivo
            self.atualizar_status("Configurando as dependências internas e venv em /opt...", 75)
            venv_dir = os.path.join(self.pasta_sistema_apps, "env")
            subprocess.run(["sudo", "python3", "-m", "venv", venv_dir, "--system-site-packages"], check=True)
            
            pip_exec = os.path.join(venv_dir, "bin", "pip")
            subprocess.run(["sudo", pip_exec, "install", "--upgrade", "pip"], check=True)
            subprocess.run(["sudo", pip_exec, "install", "pywebview", "PyQt6", "PyQt6-WebEngine", "qtpy", "google-genai", "psutil"], check=True)

            # ETAPA 4: Lógica de Autoexclusão Programada do instalador físico
            self.atualizar_status("✨ Sucesso! Aplicativo implantado. Removendo instalador temporário...", 100)
            time.sleep(2.5)
            
            # Script em segundo plano para apagar a pasta do instalador após o fechamento da janela
            pasta_instalador_atual = os.path.dirname(os.path.abspath(__file__))
            subprocess.Popen(f"sleep 1 && sudo rm -rf '{pasta_instalador_atual}'", shell=True)
            
            self.root.after(10, self.root.destroy)
            
        except Exception as e:
            self.atualizar_status(f"❌ Falha na implantação:\n{str(e)[:120]}", 0)
            self.btn_instalar.config(state="normal", bg=self.cor_acento, fg=self.txt_claro)

if __name__ == "__main__":
    root = tk.Tk()
    app = InstaladorPistonsHub(root)
    root.mainloop()
