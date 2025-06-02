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
CREATE TABLE IF NOT EXISTS alunos (
    aluno TEXT PRIMARY KEY,
    cadastro INTEGER PRIMARY KEY AUTOINCREMENT,
    cursos INTEGER,
    senha TEXT NOT NULL
)
""")
conexao.commit()

def telaprincipalabrir():
    janelaprincipal = tk.Toplevel(janela)

def addtoarvere():
    root = tk.Toplevel(janela)
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT aluno, cadastro, cursos FROM alunos")
    rows = cursor.fetchall()

    tree = ttk.Treeview(root, columns=("aluno", "cadastro", "cursos"), show="headings")
    tree.heading("aluno", text="Aluno")
    tree.heading("cadastro", text="Matrícula")
    tree.heading("cursos", text="Cursos")

    for row in rows:
        tree.insert("", "end", values=row)

    tree.pack()
    conn.close()

def cadastrar():
    aluno = entry_aluno.get()
    senha = entry_senha.get()

    if not aluno or not senha:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    try:
        cursor.execute("INSERT INTO alunos (aluno, senha) VALUES (?, ?)", (aluno, senha))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
        atualizar_lista()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Aluno já cadastrado.")

def logar():
    aluno = entry_aluno.get()
    senha = entry_senha.get()

    cursor.execute("SELECT * FROM alunos WHERE aluno = ? AND senha = ?", (aluno, senha))
    resultado = cursor.fetchone()

    if resultado:
        messagebox.showinfo("Sucesso", f"Bem-vindo, {aluno}!")
        telaprincipalabrir()
    else:
        messagebox.showerror("Erro", "Aluno ou senha incorretos.")

def atualizar_lista():
    for i in tree.get_children():
        tree.delete(i)
    
    cursor.execute("SELECT aluno FROM alunos")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

# Janela principal
janela = tk.Tk()
janela.title("Cadastro e Login de Aluno")
janela.geometry("500x400")

label_titulo = tk.Label(janela, text="Cadastro/Login", font=("Arial", 14))
label_titulo.pack(pady=10)

frame_inputs = tk.Frame(janela)
frame_inputs.pack()

label_aluno = tk.Label(frame_inputs, text="Aluno:")
label_aluno.grid(row=0, column=0, padx=5, pady=5)
entry_aluno = tk.Entry(frame_inputs)
entry_aluno.grid(row=0, column=1, padx=5, pady=5)

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

btn_arvere = tk.Button(frame_botoes, text="Arvere", command=addtoarvere)
btn_arvere.grid(row=2, column=1, padx=10)

# Exibição dos alunos
frame_lista = tk.Frame(janela)
frame_lista.pack(pady=20)

tree = ttk.Treeview(frame_lista, columns=("aluno", "cadastro", "cursos"), show="headings")
tree.heading("aluno", text="Aluno")
tree.heading("cadastro", text="Matrícula")
tree.heading("cursos", text="Cursos")
tree.pack()

# Atualizar lista de alunos ao iniciar
atualizar_lista()

janela.mainloop()
