import tkinter as tk
from tkinter import ttk
import threading
import os
import subprocess
import time

class InstaladorPistonsHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Pistons Hub Setup")
        self.root.overrideredirect(True)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.configure(bg="#0d0d0e")
        
        self.caminho_home = os.path.expanduser("~")
        self.pasta_sistema_apps = "/opt/Pistons-App"
        # LINK DO ZIP DIRETO DO SEU REPOSITÓRIO PISTONS-
        self.url_zip = "https://github.com"
        
        self.estilo = ttk.Style()
        self.estilo.theme_use('default')
        self.estilo.configure("TProgressbar", thickness=6, troughcolor="#222224", background="#0071e3", borderwidth=0)
        
        self.progresso_alvo = 0
        self.progresso_atual = 0
        self.construir_interface()
        self.atualizar_animacoes_loop()

    def construir_interface(self):
        self.barra_superior = tk.Frame(self.root, bg="#161618", height=45)
        self.barra_superior.pack(fill="x", side="top")
        
        self.btn_fechar = tk.Button(self.barra_superior, text="✕", font=("Segoe UI", 11), bg="#161618", fg="#f5f5f7", bd=0, activebackground="#ff3b30", padx=20, command=self.root.destroy)
        self.btn_fechar.pack(fill="y", side="right")

        tk.Label(self.root, text="Pistons Hub", font=("Segoe UI", 32, "bold"), bg="#0d0d0e", fg="#f5f5f7").pack(pady=(120, 5))
        self.card = tk.Frame(self.root, bg="#161618", bd=0)
        self.card.pack(fill="both", expand=True, padx=250, pady=(0, 40))
        
        self.lbl_status = tk.Label(self.card, text="Pronto para baixar e configurar o Pistons Hub.", font=("Segoe UI", 14), bg="#161618", fg="#f5f5f7", wraplength=600)
        self.lbl_status.pack(expand=True, pady=40)
        
        self.progresso = ttk.Progressbar(self.root, mode="determinate", style="TProgressbar")
        self.progresso.pack(fill="x", padx=250, pady=(0, 40))
        
        self.btn_instalar = tk.Button(self.root, text="Iniciar Instalação", font=("Segoe UI", 12, "bold"), bg="#0071e3", fg="#f5f5f7", bd=0, padx=60, pady=16, command=self.iniciar_instalacao_thread)
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
        self.btn_instalar.config(state="disabled", bg="#2c2c2e", fg="#86868b")
        threading.Thread(target=self.executar_instalacao_core, daemon=True).start()

    def executar_instalacao_core(self):
        try:
            # ETAPA 1: Baixa o ZIP usando ferramentas nativas do sistema (Sem precisar do Git)
            self.atualizar_status("Baixando o pacote estável do Pistons Hub via HTTP...", 30)
            zip_temp = os.path.join(self.caminho_home, "pistons.zip")
            subprocess.run(["wget", "-q", self.url_zip, "-O", zip_temp], check=True)
            
            # ETAPA 2: Extração e Alocação em /opt
            self.atualizar_status("Extraindo e alocando arquivos no diretório /opt...", 60)
            if os.path.exists(self.pasta_sistema_apps):
                subprocess.run(["sudo", "rm", "-rf", self.pasta_sistema_apps], check=True)
            
            # Cria a pasta de destino e descompacta o arquivo lá dentro
            subprocess.run(["sudo", "mkdir", "-p", self.pasta_sistema_apps], check=True)
            subprocess.run(["sudo", "unzip", "-q", zip_temp, "-d", "/opt/"], check=True)
            # Ajusta o nome da pasta extraída pelo GitHub para o padrão do app
            subprocess.run(["sudo", "mv", "/opt/Pistons--main", "/opt/Pistons-App-temp"], shell=True)
            subprocess.run(["sudo", "mv", "/opt/Pistons-App-temp/*", self.pasta_sistema_apps], shell=True)
            
            # Limpa o arquivo zip temporário
            if os.path.exists(zip_temp):
                os.remove(zip_temp)
            
            # ETAPA 3: Cria o Ambiente Virtual isolado para rodar os pacotes gráficos
            self.atualizar_status("Configurando o venv e dependências de execução...", 85)
            venv_dir = os.path.join(self.pasta_sistema_apps, "env")
            subprocess.run(["sudo", "python3", "-m", "venv", venv_dir, "--system-site-packages"], check=True)
            
            # Instala apenas as bibliotecas gráficas essenciais necessárias para o launcher rodar
            pip_exec = os.path.join(venv_dir, "bin", "pip")
            subprocess.run(["sudo", pip_exec, "install", "--upgrade", "pip"], check=True)
            subprocess.run(["sudo", pip_exec, "install", "pywebview", "PyQt6", "PyQt6-WebEngine", "qtpy", "google-genai", "psutil"], check=True)
            
            self.atualizar_status("✨ Sucesso! Instalação concluída em /opt/Pistons-App.", 100)
            time.sleep(2.5)
            
            # Autoexclusão limpa da pasta do instalador temporário do usuário
            pasta_instalador_atual = os.path.dirname(os.path.abspath(__file__))
            subprocess.Popen(f"sleep 1 && rm -rf '{pasta_instalador_atual}'", shell=True)
            self.root.after(10, self.root.destroy)
        except Exception as e:
            self.atualizar_status(f"❌ Falha interna: {str(e)[:80]}", 0)
            self.btn_instalar.config(state="normal", bg="#0071e3", fg="#f5f5f7")

if __name__ == "__main__":
    root = tk.Tk()
    app = InstaladorPistonsHub(root)
    root.mainloop()
