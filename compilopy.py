import tkinter as tk
from tkinter import ttk, messagebox

# Constantes fundamentais
PI = 3.141592653589793
E = 2.718281828459045

# --- PARTE 1: CLASSE DO MINI COMPILADOR (CÓDIGO JÁ EXISTENTE) ---
# Esta classe constrói a interface e a lógica do compilador.
class MiniCompilador:
    def __init__(self, root, janela_principal):
        self.root = root
        self.janela_principal = janela_principal # Guardamos a referência da janela anterior
        self.root.title("Compilo Python - Interpretador")
        self.root.geometry("600x500")

        # Área de código
        self.codigo_area = tk.Text(root, height=15, font=("Consolas", 10))
        # ALTERAÇÃO: Removida a linha "msg Bem-vindo ao compilador!" do texto padrão
        self.codigo_area.insert("1.0",
"""print Hello World
sqrt 9
cbrt 27
pow 2 5
sin 3.14159
cos 3.14159
tan 0.785
ceil 4.3
floor 4.7
max 10 20
min 10 20
fabs -42
pi""")
        self.codigo_area.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame para agrupar os botões
        botoes_frame = ttk.Frame(root)
        botoes_frame.pack(pady=5)

        # Botão Executar
        self.executar_btn = ttk.Button(botoes_frame, text="Executar", command=self.iniciar_execucao)
        self.executar_btn.pack(side="left", padx=5)

        # Botão "Voltar"
        self.voltar_btn = ttk.Button(botoes_frame, text="Voltar", command=self.voltar_para_inicio)
        self.voltar_btn.pack(side="left", padx=5)

        # Área de saída
        self.saida_area = tk.Text(root, height=15, state="disabled", bg="#f0f0f0", font=("Consolas", 10))
        self.saida_area.pack(fill="both", expand=True, padx=10, pady=5)

    def voltar_para_inicio(self):
        # Destrói a janela atual (do compilador)
        self.root.destroy()
        # Reexibe a janela de boas-vindas que estava escondida
        self.janela_principal.deiconify()
        
    def iniciar_execucao(self):
        # Cria a janela de carregamento
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Aguarde")
        loading_window.geometry("250x100")
        loading_window.transient(self.root)  # Mantém a janela sobre a principal
        loading_window.grab_set()  # Bloqueia interação com a janela principal
        loading_window.resizable(False, False)

        # Centraliza a janela de carregamento
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        pos_x = root_x + (root_width // 2) - (250 // 2)
        pos_y = root_y + (root_height // 2) - (100 // 2)
        loading_window.geometry(f"+{pos_x}+{pos_y}")

        ttk.Label(loading_window, text="Executando código...", font=("Arial", 14)).pack(expand=True)

        # Desabilita botões para evitar cliques múltiplos
        self.executar_btn.config(state="disabled")
        self.voltar_btn.config(state="disabled")

        # Força a atualização da UI para mostrar a janela de "loading"
        self.root.update_idletasks()

        # Agenda a execução do código para que a UI não congele
        self.root.after(200, self.processar_codigo, loading_window)

    # Funções matemáticas implementadas sem 'math'
    def sqrt(self, x):
        return x ** 0.5
    
    def cbrt(self, x):
        return x ** (1/3)

    def pow(self, x, y):
        return x ** y

    def fabs(self, x):
        return x if x >= 0 else -x

    def floor(self, x):
        return int(x) if x >= 0 else int(x) - 1 if x != int(x) else int(x)

    def ceil(self, x):
        return int(x) if x == int(x) else int(x) + 1 if x > 0 else int(x)

    def sin(self, x):
        return x - (x**3)/6 + (x**5)/120 - (x**7)/5040 + (x**9)/362880

    def cos(self, x):
        return 1 - (x**2)/2 + (x**4)/24 - (x**6)/720 + (x**8)/40320

    def tan(self, x):
        cos_val = self.cos(x)
        if cos_val == 0:
            return float('inf') # Retorna infinito se o cosseno for zero
        return self.sin(x) / cos_val

    def processar_codigo(self, loading_window):
        self.saida_area.config(state="normal")
        self.saida_area.delete("1.0", tk.END)
        linhas = self.codigo_area.get("1.0", tk.END).strip().split("\n")

        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue

            partes = linha.split()
            cmd = partes[0]

            try:
                if cmd == "print":
                    self.saida_area.insert(tk.END, " ".join(partes[1:]) + "\n")
                elif cmd == "msg":
                    messagebox.showinfo("Mensagem", " ".join(partes[1:]), parent=self.root)
                elif cmd == "sqrt":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{self.sqrt(x)}\n")
                elif cmd == "cbrt":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{self.cbrt(x)}\n")
                elif cmd == "pow":
                    x, y = float(partes[1]), float(partes[2])
                    self.saida_area.insert(tk.END, f"{self.pow(x, y)}\n")
                elif cmd == "sin":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{self.sin(x)}\n")
                elif cmd == "cos":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{self.cos(x)}\n")
                elif cmd == "tan":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{self.tan(x)}\n")
                elif cmd == "ceil":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{self.ceil(x)}\n")
                elif cmd == "floor":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{self.floor(x)}\n")
                elif cmd == "max":
                    x, y = float(partes[1]), float(partes[2])
                    self.saida_area.insert(tk.END, f"{x if x > y else y}\n")
                elif cmd == "min":
                    x, y = float(partes[1]), float(partes[2])
                    self.saida_area.insert(tk.END, f"{x if x < y else y}\n")
                elif cmd == "fabs":
                    x = float(partes[1])
                    self.saida_area.insert(tk.END, f"{self.fabs(x)}\n")
                elif cmd == "pi":
                    self.saida_area.insert(tk.END, f"{PI}\n")
                else:
                    self.saida_area.insert(tk.END, f"Comando não reconhecido: {linha}\n")
            except Exception as e:
                self.saida_area.insert(tk.END, f"Erro ao executar '{linha}': {e}\n")
        
        self.saida_area.config(state="disabled")

        # Ao final do processo, reabilita os botões e fecha a janela de carregamento
        self.executar_btn.config(state="normal")
        self.voltar_btn.config(state="normal")
        loading_window.destroy()

# --- PARTE 2: CLASSE DA TELA DE BOAS-VINDAS ---
class TelaBoasVindas:
    def __init__(self, root):
        self.root = root
        self.root.title("Boas-Vindas ao Compilo Python")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))

        top_frame = ttk.Frame(root)
        top_frame.pack(side="top", fill="x", pady=10, padx=10)

        # Título centralizado
        title_label = ttk.Label(top_frame, text="Bem-vindo ao Compilo Python!", font=("Arial", 18, "bold"))
        title_label.pack(pady=5)

        content_frame = ttk.Frame(root)
        content_frame.pack(fill="both", expand=True, pady=20, padx=20)

        welcome_text = (
            "Este compilador foi desenvolvido pelo grupo:\n"
            "Aaron, Walisson, Jonathan, Marcos e Victor.\n\n"
            "Aqui você poderá utilizar diversos comandos para aprender e praticar programação.\n"
            "Clique nos botões abaixo para conhecer mais sobre o compilador."
        )
        welcome_label = ttk.Label(content_frame, text=welcome_text, justify="center", font=("Arial", 14), anchor="center")
        welcome_label.pack(pady=20, fill="x", expand=True)

        explicacao_btn = ttk.Button(content_frame, text="Sobre o Compilador", command=self.mostrar_explicacao)
        explicacao_btn.pack(pady=10)

        avancar_btn = ttk.Button(content_frame, text="Avançar para o Compilador", command=self.avancar_para_compilador)
        avancar_btn.pack(pady=10)

        footer_label = ttk.Label(root, text="Integrantes: Aaron, Walisson, Jonathan, Marcos e Victor", font=("Arial", 10))
        footer_label.pack(side="bottom", pady=10)
    
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

# --- PONTO DE ENTRADA DO PROGRAMA ---
if __name__ == "__main__":
    main_root = tk.Tk()
    app = TelaBoasVindas(main_root)
    main_root.mainloop()

