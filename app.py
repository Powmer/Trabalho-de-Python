import os
import tkinter as tk
from tkinter import Image, messagebox, PhotoImage
import sqlite3
from tkinter import ttk

DB_NAME = "usuarios.db"

def criar_tabela():
    global conexao, cursor
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            cadastro INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT UNIQUE,
            cursos TEXT,
            senha TEXT NOT NULL
        )
    """)
    conexao.commit()

def resetar_banco():
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar todos os dados e resetar o banco?"):
        if os.path.exists(DB_NAME):
            try:
                conexao.close()
            except:
                pass
            os.remove(DB_NAME)
        criar_tabela()
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Banco de dados resetado com sucesso!")

curso_list = ["panificação", "confeitaria", "pizzas", "salgados", "doces", "bolos", "sorvetes"]

def telaprincipalabrir():
    janelaprincipal = tk.Toplevel(janela)
    janelaprincipal.title("Tela Principal")
    janelaprincipal.geometry("400x300")
    tk.Label(janelaprincipal, text="Bem-vindo!").pack()

def abrir_planilha():
    root = tk.Toplevel(janela)
    root.title("Planilha de Emails")

    conn = sqlite3.connect(DB_NAME)
    cursor_local = conn.cursor()
    cursor_local.execute("SELECT nome, email, cadastro, cursos FROM emails")
    rows = cursor_local.fetchall()

    treeview = ttk.Treeview(root, columns=("nome", "email", "cadastro", "cursos"), show="headings")
    treeview.heading("nome", text="nome")
    treeview.heading("email", text="email")
    treeview.heading("cadastro", text="Matrícula")
    treeview.heading("cursos", text="Cursos")

    for row in rows:
        treeview.insert("", "end", values=row)

    treeview.pack(fill=tk.BOTH, expand=True)
    conn.close()

def cadastrar():
    abrir_cadastro()

def abrir_cadastro():
    cadastro_win = tk.Toplevel(janela)
    cadastro_win.title("Cadastro de Aluno")

    tk.Label(cadastro_win, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entry_nome_local = tk.Entry(cadastro_win)
    entry_nome_local.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(cadastro_win, text="Email:").grid(row=1, column=0, padx=5, pady=5)
    entry_email_local = tk.Entry(cadastro_win)
    entry_email_local.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(cadastro_win, text="Senha:").grid(row=2, column=0, padx=5, pady=5)
    entry_senha_local = tk.Entry(cadastro_win, show="*")
    entry_senha_local.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(cadastro_win, text="Curso:").grid(row=3, column=0)
    curso_var = tk.StringVar()
    curso_combo = ttk.Combobox(cadastro_win, textvariable=curso_var, values=curso_list)
    curso_combo.grid(row=3, column=1)

    def confirmar_cadastro():
        nome = entry_nome_local.get()
        email = entry_email_local.get()
        senha = entry_senha_local.get()
        curso = curso_var.get()
     # Validação simples sem regex(Obs: Integrar dps ta no commit DE REGEX)
        if not nome or not email or not senha or not curso:
            messagebox.showwarning("Aviso", "Preencha todos os campos.", parent=cadastro_win)
            return

        if any(char.isdigit() for char in nome):
            messagebox.showerror("Erro", "Nome inválido. Não use números.", parent=cadastro_win)
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Erro", "Email inválido.", parent=cadastro_win)
            return

        if len(senha) < 8 or not any(char.isdigit() for char in senha):
            messagebox.showerror("Erro", "A senha deve ter pelo menos 8 caracteres e conter pelo menos um número.", parent=cadastro_win)
            return

        try:
            cursor.execute("INSERT INTO emails (nome, email, senha, cursos) VALUES (?, ?, ?, ?)",
                           (nome, email, senha, curso))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.", parent=cadastro_win)
            atualizar_lista()
            cadastro_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Email já cadastrado.", parent=cadastro_win)

    btn_confirmar = tk.Button(cadastro_win, text="Confirmar", command=confirmar_cadastro)
    btn_confirmar.grid(row=4, column=1, pady=10)

def logar():
    email = entry_email.get()
    senha = entry_senha.get()

    cursor.execute("SELECT * FROM emails WHERE email = ? AND senha = ?", (email, senha))
    resultado = cursor.fetchone()

    if resultado:
        messagebox.showinfo("Sucesso", f"Bem-vindo, {email}!")
        telaprincipalabrir()
    else:
        messagebox.showerror("Erro", "Email ou senha incorretos.")

def atualizar_lista():
    for i in tree.get_children():
        tree.delete(i)

    cursor.execute("SELECT nome, email, cadastro, cursos FROM emails")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)
#INTEFACE PRINCIPAL]s
janela = tk.Tk()
janela.title("Cadastro e Login de Email")
janela.geometry("500x400")

img = PhotoImage(file="D:\Documentos\Trabalhos Faculdade\RadPy\Trabalho-de-Python\Baking-Bread-Logo.png")
label_titulo = tk.Label(janela, image=img)
label_titulo.pack(pady=10)

frame_inputs = tk.Frame(janela)
frame_inputs.pack()

label_email = tk.Label(frame_inputs, text="Email:")
label_email.grid(row=0, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_inputs)
entry_email.grid(row=0, column=1, padx=5, pady=5)

label_senha = tk.Label(frame_inputs, text="Senha:")
label_senha.grid(row=1, column=0, padx=5, pady=5)
entry_senha = tk.Entry(frame_inputs, show="*")
entry_senha.grid(row=1, column=1, padx=5, pady=5)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=cadastrar)
btn_cadastrar.grid(row=0, column=0, padx=10)

btn_logar = tk.Button(frame_botoes, text="Login", command=logar)
btn_logar.grid(row=0, column=1, padx=10)

btn_arvore = tk.Button(frame_botoes, text="Árvore", command=abrir_planilha)
btn_arvore.grid(row=0, column=2, padx=10)

btn_resetar = tk.Button(frame_botoes, text="Resetar Banco", command=resetar_banco)
btn_resetar.grid(row=0, column=3, padx=10)

frame_lista = tk.Frame(janela)
frame_lista.pack(pady=20, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame_lista, columns=('nome', "email", "cadastro", "cursos"), show="headings")
tree.heading("nome", text="nome")
tree.heading("email", text="email")
tree.heading("cadastro", text="Matrícula")
tree.heading("cursos", text="Cursos")
tree.pack(fill=tk.BOTH, expand=True)

criar_tabela()
atualizar_lista()

janela.mainloop()
