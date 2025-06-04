import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import openpyxl
from openpyxl import Workbook
from datetime import datetime
import os

# Conexão com banco de dados
conexao = sqlite3.connect("usuarios.db")
cursor = conexao.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        cadastro INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        cursos TEXT,
        senha TEXT NOT NULL
        
    )
""")

conexao.commit()
# variaveis globais
curso_list = ["panificação", "confeitaria", "pizzas", "salgados", "doces", "bolos", "sorvetes"]
def telaprincipalabrir():
    janelaprincipal = tk.Toplevel(janela)

def addtoarvere():
    root = tk.Toplevel(janela)
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, cadastro, cursos FROM emails")
    rows = cursor.fetchall()

    tree = ttk.Treeview(root, columns=("email", "cadastro", "cursos"), show="headings")
    tree.heading("email", text="email")
    tree.heading("cadastro", text="Matrícula")
    tree.heading("cursos", text="Cursos")

    for row in rows:
        tree.insert("", "end", values=row)

    tree.pack()
    conn.close()

def cadastrar():
    email = entry_email.get()
    senha = entry_senha.get()

    if not email or not senha:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    try:
        cursor.execute("INSERT INTO emails (email, senha) VALUES (?, ?)", (email, senha))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
        atualizar_lista()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "email já cadastrado.")
    abrir_cadastro()

def abrir_cadastro():
    cadastro_win = tk.Toplevel(janela)
    cadastro_win.title("Cadastro de Aluno")

    tk.Label(cadastro_win, text="Email:").grid(row=0, column=0, padx=5, pady=5)
    entry_email_local = tk.Entry(cadastro_win)
    entry_email_local.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(cadastro_win, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
    entry_senha_local = tk.Entry(cadastro_win, show="*")
    entry_senha_local.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(cadastro_win, text="Curso:").grid(row=2, column=0)
    curso_var = tk.StringVar()
    curso_combo = ttk.Combobox(cadastro_win, textvariable=curso_var, values=curso_list)
    curso_combo.grid(row=2, column=1)

    def confirmar_cadastro():
        email = entry_email_local.get()
        senha = entry_senha_local.get()
        curso = curso_var.get()

        if not email or not senha or not curso:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            cursor.execute("INSERT INTO emails (email, senha, cursos) VALUES (?, ?, ?)", (email, senha, curso))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
            atualizar_lista()
            cadastro_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Email já cadastrado.")

    btn_confirmar = tk.Button(cadastro_win, text="Confirmar", command=confirmar_cadastro)
    btn_confirmar.grid(row=3, column=1, pady=10)

def logar():
    email = entry_email.get()
    senha = entry_senha.get()

    cursor.execute("SELECT * FROM emails WHERE email = ? AND senha = ?", (email, senha))
    resultado = cursor.fetchone()

    if resultado:
        messagebox.showinfo("Sucesso", f"Bem-vindo, {email}!")
        telaprincipalabrir()
    else:
        messagebox.showerror("Erro", "email ou senha incorretos.")
def atualizar_lista():
    for i in tree.get_children():
        tree.delete(i)
    
    cursor.execute("SELECT email FROM emails")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)
    
# Janela principal
janela = tk.Tk()
janela.title("Cadastro e Login de email")
janela.geometry("500x400")

label_titulo = tk.Label(janela, text="Login", font=("Arial", 14))
label_titulo.pack(pady=10)

frame_inputs = tk.Frame(janela)
frame_inputs.pack()

label_senha = tk.Label(frame_inputs, text="Senha:")
label_senha.grid(row=1, column=0, padx=5, pady=5)
entry_senha = tk.Entry(frame_inputs, show="*")
entry_senha.grid(row=1, column=1, padx=5, pady=5)

label_email = tk.Label(frame_inputs, text="email:")
label_email.grid(row=0, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_inputs)
entry_email.grid(row=0, column=1, padx=5, pady=5)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=cadastrar)
btn_cadastrar.grid(row=0, column=0, padx=10)

btn_logar = tk.Button(frame_botoes, text="Login", command=logar)
btn_logar.grid(row=0, column=1, padx=10)

btn_arvere = tk.Button(frame_botoes, text="Arvere", command=addtoarvere)
btn_arvere.grid(row=2, column=1, padx=10)

# Exibição dos emails
frame_lista = tk.Frame(janela)
frame_lista.pack(pady=20)

tree = ttk.Treeview(frame_lista, columns=("email", "cadastro", "cursos"), show="headings")
tree.heading("email", text="email")
tree.heading("cadastro", text="Matrícula")
tree.heading("cursos", text="Cursos")
tree.pack()

# Atualizar lista de emails ao iniciar
atualizar_lista()

janela.mainloop()