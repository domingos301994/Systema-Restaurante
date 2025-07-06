import tkinter as tk
from tkinter import ttk, messagebox

# Classe para a árvore binária (menu de pratos)
class Menu:
    def __init__(self, prato, preco):
        self.esquerdo = None
        self.direito = None
        self.prato = prato
        self.preco = preco

def inserir(raiz, prato, preco):
    if raiz is None:
        return Menu(prato, preco)
    elif prato < raiz.prato:
        raiz.esquerdo = inserir(raiz.esquerdo, prato, preco)
    else:
        raiz.direito = inserir(raiz.direito, prato, preco)
    return raiz

def emOrdem(raiz, resultado):
    if raiz is not None:
        emOrdem(raiz.esquerdo, resultado)
        resultado.append(f"{raiz.prato}: R$ {raiz.preco:.2f}")
        emOrdem(raiz.direito, resultado)

def buscar(raiz, prato):
    if raiz is None:
        return False
    elif raiz.prato == prato:
        return True
    elif prato < raiz.prato:
        return buscar(raiz.esquerdo, prato)
    else:
        return buscar(raiz.direito, prato)

# Classe para a fila de pedidos
class Fila:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

def alocar(inicio, prato):
    if inicio is None:
        return Fila(prato)
    temp = inicio
    while temp.proximo is not None:
        temp = temp.proximo
    temp.proximo = Fila(prato)
    return inicio

def remove(inicio):
    if inicio is None:
        return None
    return inicio.proximo

def imprimir_fila(inicio):
    temp = inicio
    resultado = []
    while temp is not None:
        resultado.append(temp.valor)
        temp = temp.proximo
    return resultado

# Classe para a pilha de pedidos prontos
class Pilha:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

def push(topo, dado):
    novo = Pilha(dado)
    novo.proximo = topo
    return novo

def pop(topo):
    if topo is None:
        return None
    return topo.proximo

# Variáveis globais
raiz = None
inicio_fila = None
topo_pilha = None

# Funções para a interface

def adicionar_prato():
    global raiz
    prato = entrada_prato.get()
    preco = entrada_preco.get()
    try:
        preco = float(preco)
        raiz = inserir(raiz, prato, preco)
        messagebox.showinfo("Sucesso", f"Prato '{prato}' adicionado com sucesso!")
        entrada_prato.delete(0, tk.END)
        entrada_preco.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um preço válido.")

def mostrar_menu():
    resultado = []
    emOrdem(raiz, resultado)
    lista_menu.delete(0, tk.END)
    for item in resultado:
        lista_menu.insert(tk.END, item)

def fazer_pedido():
    global inicio_fila
    prato = entrada_pedido.get()
    if buscar(raiz, prato):
        inicio_fila = alocar(inicio_fila, prato)
        messagebox.showinfo("Sucesso", f"Pedido do prato '{prato}' foi adicionado à fila!")
        entrada_pedido.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", f"Prato '{prato}' não encontrado no menu.")

def acompanhar_pedidos():
    resultado = imprimir_fila(inicio_fila)
    lista_fila.delete(0, tk.END)
    for idx, prato in enumerate(resultado, 1):
        lista_fila.insert(tk.END, f"{idx}º: {prato}")

def processar_pedido():
    global inicio_fila, topo_pilha
    if inicio_fila is not None:
        topo_pilha = push(topo_pilha, inicio_fila.valor)
        inicio_fila = remove(inicio_fila)
        messagebox.showinfo("Sucesso", "Pedido processado e pronto para entrega!")
        acompanhar_pedidos()
    else:
        messagebox.showerror("Erro", "Não há pedidos na fila para processar.")

def entregar_pedido():
    global topo_pilha
    if topo_pilha is not None:
        messagebox.showinfo("Sucesso", f"O prato '{topo_pilha.dado}' foi entregue!")
        topo_pilha = pop(topo_pilha)
    else:
        messagebox.showerror("Erro", "Não há pedidos prontos para entregar.")

# Configuração da interface
root = tk.Tk()
root.title("Sistema de Restaurante")
root.geometry("600x800")  # Definindo um tamanho inicial
root.configure(bg="#FFC0CB")  # Cor de fundo para a janela principal

# Configuração para responsividade
for i in range(13):
    root.rowconfigure(i, weight=1)
for i in range(3):
    root.columnconfigure(i, weight=1)

# Configurando estilos com ttk.Style
style = ttk.Style()
style.configure("relief", 
                font=("Times New Roman", 12), 
                padding=15, 
                relief="raised",
                background="#6600ff", 
                foreground="Grey")
style.map("TButton",
          background=[("active", "#FF0000"),  # Vermelho ao passar o mouse
                      ("pressed", "#00FF00")])  # Verde ao clicar
  # Cor quando o botão é pressionado

# Adicionar pratos ao menu
tk.Label(root, text="Adicionar Prato ao Menu", bg="#6600ff", fg="Grey", font=("Times New Roman", 16), bd=2, relief="solid").grid(row=0, column=0, columnspan=3, sticky="ew")
entrada_prato = tk.Entry(root, font=("Times New Roman", 12), bd=2, relief="solid")
entrada_prato.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
entrada_preco = tk.Entry(root, font=("Times New Roman", 12),bd=2, relief="solid")
entrada_preco.grid(row=1, column=2, sticky="ew", padx=15, pady=10)
btn_adicionar = ttk.Button(root, text="Adicionar",command=adicionar_prato)
btn_adicionar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

# Mostrar menu
tk.Label(root, text="Menu de Pratos", bg="#6600ff", fg="Grey", font=("Arial", 14),bd=2, relief="solid").grid(row=3, column=0, columnspan=3, sticky="ew")
lista_menu = tk.Listbox(root, font=("Arial", 12), height=10)
lista_menu.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
btn_mostrar_menu = ttk.Button(root, text="Mostrar Menu", command=mostrar_menu)
btn_mostrar_menu.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

# Fazer pedidos
tk.Label(root, text="Fazer Pedido", bg="#6600ff", fg="Grey", font=("Arial", 14),bd=2, relief="solid").grid(row=6, column=0, columnspan=3, sticky="ew")
entrada_pedido = tk.Entry(root, font=("Arial", 12))
entrada_pedido.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
btn_pedido = ttk.Button(root, text="Fazer Pedido", command=fazer_pedido)
btn_pedido.grid(row=7, column=2, sticky="ew", padx=10, pady=5)

# Acompanhar pedidos
tk.Label(root, text="Fila de Pedidos", bg="#6600ff", fg="Grey", font=("Arial", 14),bd=2, relief="solid").grid(row=8, column=0, columnspan=3, sticky="ew")
lista_fila = tk.Listbox(root, font=("Arial", 12), height=10)
lista_fila.grid(row=9, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
btn_acompanhar = ttk.Button(root, text="Acompanhar Pedidos", command=acompanhar_pedidos)
btn_acompanhar.grid(row=10, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

# Definir o estilo para os botões
style = ttk.Style()
style.configure("TButton", 
                borderwidth=2, 
                relief="solid", 
                padding=5)

# Botões com o estilo personalizado
btn_processar = ttk.Button(root, text="Processar Pedido", command=processar_pedido, style="TButton")
btn_processar.grid(row=11, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

btn_entregar = ttk.Button(root, text="Entregar Pedido", command=entregar_pedido, style="TButton")
btn_entregar.grid(row=12, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

# Rodar a interface gráfica

root.mainloop()