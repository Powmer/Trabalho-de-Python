import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from datetime import datetime
import os
import re

#CONEXÃO COM O BANCO DE DADOS
conexao = sqlite3.connect("usuarios.db")
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

    def validar_email(email):
        padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(padrao_email, email)

    def validar_senha(senha):
        padrao_senha = r'^(?=.*\d).{8,}$'
        return re.match(padrao_senha, senha)

    def validar_nome(nome):
        padrao_nome = r"^[A-Za-zÀ-ÖØ-öø-ÿ' ]+$"
        return re.match(padrao_nome, nome)

    def confirmar_cadastro():
        nome = entry_nome_local.get()
        email = entry_email_local.get()
        senha = entry_senha_local.get()
        curso = curso_var.get()

        if not nome or not email or not senha or not curso:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        if not validar_nome(nome):
            messagebox.showerror("Erro", "Nome inválido. Use apenas letras e espaços.")
            return

        if not validar_email(email):
            messagebox.showerror("Erro", "Email inválido.")
            return

        if not validar_senha(senha):
            messagebox.showerror("Erro", "A senha deve ter pelo menos 8 caracteres e conter pelo menos um número.")
            return

        try:
            cursor.execute("INSERT INTO emails (nome, email, senha, cursos) VALUES (?, ?, ?, ?)", (nome, email, senha, curso))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
            atualizar_lista()
            cadastro_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Email já cadastrado.")

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
        messagebox.showerror("Erro", "email ou senha incorretos.")

def atualizar_lista():
    for i in tree.get_children():
        tree.delete(i)
    
    cursor.execute("SELECT email FROM emails")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

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

frame_lista = tk.Frame(janela)
frame_lista.pack(pady=20)

tree = ttk.Treeview(frame_lista, columns=("email", "cadastro", "cursos"), show="headings")
tree.heading("email", text="email")
tree.heading("cadastro", text="Matrícula")
tree.heading("cursos", text="Cursos")
tree.pack()

atualizar_lista()

janela.mainloop()
