import sys
import os

# --- INÍCIO DA MODIFICAÇÃO ---
# Este bloco de código adiciona a pasta 'libs' ao caminho de busca para verificar as bibliotecas, não coloquei uma env pq tinha preguiça.
script_dir = os.path.dirname(os.path.abspath(__file__))
libs_dir = os.path.join(script_dir, 'libs')
sys.path.insert(0, libs_dir)
# --- FIM ---

import tkinter as tk
from tkinter import ttk, messagebox
import math
from PIL import Image, ImageTk

class MiniCompilador:
    def __init__(self, root, janela_principal):
        self.root = root
        self.janela_principal = janela_principal
        self.root.title("Compilo Python - Interpretador")
        self.root.geometry("700x600")

        self.codigo_area = tk.Text(root, height=18, font=("Consolas", 10))
        self.codigo_area.insert("1.0",
"""# Comandos de exemplo (válidos)
-Constantes
pi
e

-Potencia e logaritmo
pow 2 8
log 100
log10 1000
exp 2

-Trigonometria e Conversão
sin 1.57
cos 3.14
degrees 1.5708
radians 90

-Funções hiperbolicas
sinh 1
cosh 0

-Arredondamento e valor
trunc 3.99
factorial 5

-Funções númericas
gcd 54 24
comb 5 2

-Checagem de tipos
isfinite 999
isinf inf
isnan nan
"""
        )
        self.codigo_area.pack(fill="both", expand=True, padx=10, pady=5)
        
        botoes_frame = ttk.Frame(root)
        botoes_frame.pack(pady=5)

        self.executar_btn = ttk.Button(botoes_frame, text="Executar", command=self.iniciar_execucao)
        self.executar_btn.pack(side="left", padx=5)

        self.voltar_btn = ttk.Button(botoes_frame, text="Voltar", command=self.voltar_para_inicio)
        self.voltar_btn.pack(side="left", padx=5)

        self.saida_area = tk.Text(root, height=18, state="disabled", bg="#f0f0f0", font=("Consolas", 10))
        self.saida_area.pack(fill="both", expand=True, padx=10, pady=5)

    def voltar_para_inicio(self):
        self.root.destroy()
        self.janela_principal.deiconify()
        
    def iniciar_execucao(self):
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Executando")
        loading_window.geometry("200x150")
        loading_window.transient(self.root)
        loading_window.grab_set()
        loading_window.resizable(False, False)

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        pos_x = root_x + (root_width // 2) - (200 // 2)
        pos_y = root_y + (root_height // 2) - (150 // 2)
        loading_window.geometry(f"+{pos_x}+{pos_y}")

        try:
            logo_img = Image.open("assets/imagen_logo.png")
            logo_img = logo_img.resize((80, 80))
            logo_photo = ImageTk.PhotoImage(logo_img)
            
            logo_label = ttk.Label(loading_window, image=logo_photo)
            logo_label.image = logo_photo 
            logo_label.pack(pady=10)
            
            ttk.Label(loading_window, text="Executando...", font=("Arial", 10)).pack()

        except Exception as e:
            print(f"Erro ao carregar imagem de execução: {e}")
            ttk.Label(loading_window, text="Executando código...", font=("Arial", 14)).pack(expand=True)

        self.executar_btn.config(state="disabled")
        self.voltar_btn.config(state="disabled")
        self.root.update_idletasks()
        self.root.after(200, self.processar_codigo, loading_window)

    def processar_codigo(self, loading_window):
        self.saida_area.config(state="normal")
        self.saida_area.delete("1.0", tk.END)
        linhas = self.codigo_area.get("1.0", tk.END).strip().split("\n")

        for linha in linhas:
            linha = linha.strip()
            if not linha or linha.startswith("-") or linha.startswith("#"):
                continue

            partes = linha.split()
            cmd = partes[0]

            try:
                if cmd == "print":
                    self.saida_area.insert(tk.END, " ".join(partes[1:]) + "\n")
                elif cmd == "msg":
                    messagebox.showinfo("Mensagem", " ".join(partes[1:]), parent=self.root)

                elif cmd == "pi":
                    self.saida_area.insert(tk.END, f"{math.pi}\n")
                elif cmd == "e":
                    self.saida_area.insert(tk.END, f"{math.e}\n")
                elif cmd == "inf":
                    self.saida_area.insert(tk.END, f"{math.inf}\n")
                elif cmd == "nan":
                    self.saida_area.insert(tk.END, f"{math.nan}\n")

                elif cmd == "sqrt":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.sqrt(x)}\n")
                elif cmd == "cbrt":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{x ** (1/3)}\n")
                elif cmd == "pow":
                    x, y = float(partes[1]), float(partes[2])
                    self.saida_area.insert(tk.END, f"{math.pow(x, y)}\n")
                elif cmd == "exp":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.exp(x)}\n")
                elif cmd == "log":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.log(x)}\n")
                elif cmd == "log10":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.log10(x)}\n")
                elif cmd == "log2":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.log2(x)}\n")
                
                elif cmd == "sin":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.sin(x)}\n")
                elif cmd == "cos":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.cos(x)}\n")
                elif cmd == "tan":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.tan(x)}\n")
                elif cmd == "asin":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.asin(x)}\n")
                elif cmd == "acos":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.acos(x)}\n")
                elif cmd == "atan":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.atan(x)}\n")

                elif cmd == "degrees":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.degrees(x)}\n")
                elif cmd == "radians":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.radians(x)}\n")

                elif cmd == "sinh":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.sinh(x)}\n")
                elif cmd == "cosh":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.cosh(x)}\n")
                elif cmd == "tanh":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.tanh(x)}\n")

                elif cmd == "ceil":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.ceil(x)}\n")
                elif cmd == "floor":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.floor(x)}\n")
                elif cmd == "fabs":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.fabs(x)}\n")
                elif cmd == "trunc":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.trunc(x)}\n")

                elif cmd == "factorial":
                    x = int(partes[1])
                    self.saida_area.insert(tk.END, f"{math.factorial(x)}\n")
                elif cmd == "gcd":
                    x, y = int(partes[1]), int(partes[2])
                    self.saida_area.insert(tk.END, f"{math.gcd(x, y)}\n")
                elif cmd == "lcm":
                    x, y = int(partes[1]), int(partes[2])
                    self.saida_area.insert(tk.END, f"{math.lcm(x, y)}\n")
                elif cmd == "comb":
                    n, k = int(partes[1]), int(partes[2])
                    self.saida_area.insert(tk.END, f"{math.comb(n, k)}\n")
                elif cmd == "perm":
                    n, k = int(partes[1]), int(partes[2])
                    self.saida_area.insert(tk.END, f"{math.perm(n, k)}\n")

                elif cmd == "isfinite":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.isfinite(x)}\n")
                elif cmd == "isinf":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.isinf(x)}\n")
                elif cmd == "isnan":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{math.isnan(x)}\n")

                elif cmd == "max":
                    nums = [float(n) for n in partes[1:]]
                    self.saida_area.insert(tk.END, f"{max(nums)}\n")
                elif cmd == "min":
                    nums = [float(n) for n in partes[1:]]
                    self.saida_area.insert(tk.END, f"{min(nums)}\n")
                
                else:
                    self.saida_area.insert(tk.END, f"Comando não reconhecido: {linha}\n")
            except Exception as e:
                self.saida_area.insert(tk.END, f"Erro ao executar '{linha}': {e}\n")
        
        num_linhas = int(self.saida_area.index('end-1c').split('.')[0])
        altura_final = max(1, min(num_linhas, 20))
        self.saida_area.config(height=altura_final)
        
        self.saida_area.config(state="disabled")
        self.executar_btn.config(state="normal")
        self.voltar_btn.config(state="normal")
        loading_window.destroy()

class TelaBoasVindas:
    def __init__(self, root):
        self.root = root
        self.root.title("Boas-Vindas ao Compilo Python")
        self.root.geometry("700x500")
        self.root.resizable(True, True) 
        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))

        top_frame = ttk.Frame(root)
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        title_label = ttk.Label(top_frame, text="Bem-vindo ao Compilo Python!", font=("Arial", 18, "bold"))
        title_label.pack(pady=5)

        self.content_frame = ttk.Frame(root)
        self.content_frame.pack(fill="both", expand=True, pady=20, padx=20)

        welcome_text = (
            "Este compilador foi desenvolvido pelo grupo:\n"
            "Aaron, Walisson, Jonathan, Marcos e Victor.\n\n"
            "Aqui você poderá utilizar diversos comandos para aprender e praticar programação.\n"
            "Clique nos botões abaixo para conhecer mais sobre o compilador."
        )
        self.welcome_label = ttk.Label(self.content_frame, text=welcome_text, justify="center", font=("Arial", 14), anchor="center")
        self.welcome_label.pack(pady=20, fill="x", expand=True)

        explicacao_btn = ttk.Button(self.content_frame, text="Sobre o Compilador", command=self.mostrar_explicacao)
        explicacao_btn.pack(pady=10)

        avancar_btn = ttk.Button(self.content_frame, text="Avançar para o Compilador", command=self.avancar_para_compilador)
        avancar_btn.pack(pady=10)

        footer_label = ttk.Label(root, text="Integrantes: Aaron, Walisson, Jonathan, Marcos e Victor", font=("Arial", 10))
        footer_label.pack(side="bottom", pady=10)

        self.content_frame.bind('<Configure>', self._on_resize)

    def _on_resize(self, event):
        nova_largura = event.width - 20 
        self.welcome_label.config(wraplength=nova_largura)
    
    def mostrar_explicacao(self):
        messagebox.showinfo(
            "Sobre o Compilador",
            "Nosso compilador possui no mínimo 30 comandos que permitem criar e executar programas de forma eficiente. "
            "Ele foi desenvolvido para facilitar a programação e otimizar o aprendizado dos conceitos fundamentais.",
            parent=self.root
        )

    def avancar_para_compilador(self):
        self.root.withdraw()
        compilador_window = tk.Toplevel(self.root)
        app_compilador = MiniCompilador(compilador_window, self.root)
        compilador_window.protocol("WM_DELETE_WINDOW", self.root.destroy)

if __name__ == "__main__":
    main_root = tk.Tk()
    app = TelaBoasVindas(main_root)
    main_root.mainloop()

