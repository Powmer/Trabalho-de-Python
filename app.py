import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, PhotoImage
import openpyxl
import sqlite3
import pandas as pd

# CONFIGURAÇÕES
DB_NAME = "usuarios.db"
PASTA_CURSOS = "cursostxt"

# CRIAR PASTA E ARQUIVOS PADRÕES DOS CURSOS
def criar_pasta_cursos():
    if not os.path.exists(PASTA_CURSOS):
        os.makedirs(PASTA_CURSOS)

    cursos_default = {
        "panificacao.txt": "Conteúdo de Panificação...",
        "confeitaria.txt": "Conteúdo de Confeitaria...",
        "pizzas.txt": "Conteúdo de Pizzas...",
        "salgados.txt": "Conteúdo de Salgados...",
        "doces.txt": "Conteúdo de Doces...",
        "bolos.txt": "Conteúdo de Bolos...",
        "sorvetes.txt": "Conteúdo de Sorvetes..."
    }

    for nome_arquivo, conteudo in cursos_default.items():
        caminho = os.path.join(PASTA_CURSOS, nome_arquivo)
        if not os.path.exists(caminho):
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)

criar_pasta_cursos()

# CLASSE CURSO
class Curso:
    def __init__(self, titulo, arquivo_conteudo):
        self.titulo = titulo
        self.arquivo_conteudo = arquivo_conteudo

    def obter_conteudo(self):
        caminho = os.path.join(PASTA_CURSOS, self.arquivo_conteudo)
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "Conteúdo indisponível."

cursos_disponiveis = [
    Curso("Panificação", "panificacao.txt"),
    Curso("Confeitaria", "confeitaria.txt"),
    Curso("Pizzas", "pizzas.txt"),
    Curso("Salgados", "salgados.txt"),
    Curso("Doces", "doces.txt"),
    Curso("Bolos", "bolos.txt"),
    Curso("Sorvetes", "sorvetes.txt")
]

# BANCO DE DADOS
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
            senha TEXT NOT NULL,
            data_inscricao DATE DEFAULT (date('now'))
        )
    """)
    conexao.commit()

# RESETAR BANCO
def resetar_banco():
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja resetar o banco?"):
        if os.path.exists(DB_NAME):
            try:
                conexao.close()
            except:
                pass
            os.remove(DB_NAME)
        criar_tabela()
        messagebox.showinfo("Sucesso", "Banco resetado com sucesso!")

# CADASTRO DE USUÁRIO
def abrir_cadastro():
    cadastro_win = tk.Toplevel(janela)
    cadastro_win.title("Cadastro de Aluno")

    tk.Label(cadastro_win, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entry_nome = tk.Entry(cadastro_win)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(cadastro_win, text="Email:").grid(row=1, column=0, padx=5, pady=5)
    entry_email = tk.Entry(cadastro_win)
    entry_email.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(cadastro_win, text="Senha:").grid(row=2, column=0, padx=5, pady=5)
    entry_senha = tk.Entry(cadastro_win, show="*")
    entry_senha.grid(row=2, column=1, padx=5, pady=5)

    def confirmar_cadastro():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()

        if not nome or not email or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos.", parent=cadastro_win)
            return
        if any(char.isdigit() for char in nome):
            messagebox.showerror("Erro", "Nome inválido. Não use números.", parent=cadastro_win)
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Erro", "Email inválido.", parent=cadastro_win)
            return
        if len(senha) < 8 or not any(char.isdigit() for char in senha):
            messagebox.showerror("Erro", "A senha deve ter 8 caracteres e conter pelo menos um número.", parent=cadastro_win)
            return

        try:
            cursor.execute("INSERT INTO emails (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.", parent=cadastro_win)
            cadastro_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Email já cadastrado.", parent=cadastro_win)

    btn_confirmar = tk.Button(cadastro_win, text="Confirmar", command=confirmar_cadastro)
    btn_confirmar.grid(row=4, column=1, pady=10)

# LOGIN
def logar():
    global usuario_logado
    email = entry_email.get()
    senha = entry_senha.get()

    cursor.execute("SELECT * FROM emails WHERE email=? AND senha=?", (email, senha))
    usuario_logado = cursor.fetchone()

    if usuario_logado:
        messagebox.showinfo("Sucesso", f"Bem-vindo, {email}!")
        telaprincipalabrir()
    else:
        messagebox.showerror("Erro", "Email ou senha incorretos.")

# TELA PRINCIPAL
def telaprincipalabrir():
    janelaprincipal = tk.Toplevel(janela)
    janelaprincipal.title("Página Inicial")
    janelaprincipal.geometry("500x500")

    def telaprincipalfechar():
        if "janela_info" in globals() and janela_info.winfo_exists():
            janela_info.destroy()
        janelaprincipal.destroy()

    janelaprincipal.protocol("WM_DELETE_WINDOW", telaprincipalfechar)

    tk.Label(janelaprincipal, text="Lista de Cursos", font=("Arial", 14, "bold")).pack(pady=10)
    btn_info_usuario = tk.Button(janelaprincipal, text="Informações do Usuário", command=infowin)
    btn_info_usuario.pack(side="bottom", pady=5)

    frame_cursos = tk.Frame(janelaprincipal)
    frame_cursos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def abrir_conteudo_curso(curso):
        conteudo_win = tk.Toplevel(janelaprincipal)
        conteudo_win.title(curso.titulo)
        conteudo = curso.obter_conteudo()

        tk.Label(conteudo_win, text=curso.titulo, font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(conteudo_win, text=conteudo, wraplength=450, justify="left").pack(padx=10, pady=10)

        def marcar_como_lido():
            if not usuario_logado:
                messagebox.showerror("Erro", "Nenhum usuário logado.")
                return
            cadastro, nome, email, cursos, senha, data_inscricao = usuario_logado
            lista_cursos = cursos.split(",") if cursos else []
            if curso.titulo not in lista_cursos:
                lista_cursos.append(curso.titulo)
                novos_cursos = ",".join(lista_cursos)
                cursor.execute("UPDATE emails SET cursos=? WHERE cadastro=?", (novos_cursos, cadastro))
                conexao.commit()
                cursor.execute("SELECT * FROM emails WHERE cadastro=?", (cadastro,))
                globals()["usuario_logado"] = cursor.fetchone()
                messagebox.showinfo("Sucesso", f"Curso '{curso.titulo}' marcado como lido.")
                conteudo_win.destroy()
            else:
                messagebox.showinfo("Informação", "Curso já marcado como lido.")
                conteudo_win.destroy()

        tk.Button(conteudo_win, text="Marcar como Lido", command=marcar_como_lido).pack(pady=10)

    for curso in cursos_disponiveis:
        tk.Button(frame_cursos, text=curso.titulo, width=30,
                   command=lambda c=curso: abrir_conteudo_curso(c)).pack(pady=5)

# INFORMAÇÕES DO USUÁRIO
def infowin():
    global janela_info
    janela_info = tk.Toplevel(janela)
    janela_info.title("Informações do Usuário")
    janela_info.geometry("400x300")

    tk.Label(janela_info, text="Informações do Usuário", font=("Arial", 14, "bold")).pack(pady=10)

    if not usuario_logado:
        tk.Label(janela_info, text="Nenhum usuário logado.").pack(pady=10)
        return

    cadastro, nome, email, cursos, senha, data_inscricao = usuario_logado
    dados = {
        "Nome:": nome,
        "Email:": email,
        "Cursos Concluídos:": cursos,
        "Data de Inscrição:": data_inscricao
    }

    for i, (label, valor) in enumerate(dados.items()):
        tk.Label(janela_info, text=label, font=("Arial", 12, "bold")).grid(row=i, column=0, sticky="w", padx=10, pady=2)
        tk.Label(janela_info, text=valor, font=("Arial", 12)).grid(row=i, column=1, sticky="w", padx=10, pady=2)

# PLANILHA DE EMAILS (CRUD)
def abrir_planilha():
    root = tk.Toplevel(janela)
    root.title("Planilha de Emails")

    conn = sqlite3.connect(DB_NAME)
    cursor_local = conn.cursor()
    cursor_local.execute("SELECT nome, email, cadastro, cursos, data_inscricao FROM emails")
    rows = cursor_local.fetchall()

    treeview = ttk.Treeview(root, columns=("nome", "email", "cadastro", "cursos", "data_inscricao"), show="headings")
    for col in ("nome", "email", "cadastro", "cursos", "data_inscricao"):
        treeview.heading(col, text=col.capitalize())
        treeview.column(col, width=120, anchor="center")

    for row in rows:
        treeview.insert("", "end", values=row)

    treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def exportar_excel():
        dados = [treeview.item(item)["values"] for item in treeview.get_children()]
        df = pd.DataFrame(dados, columns=["Nome", "Email", "Cadastro", "Cursos", "Data de Inscrição"])
        caminho = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if caminho:
            df.to_excel(caminho, index=False)
            messagebox.showinfo("Sucesso", f"Planilha exportada para {caminho}", parent=root)

    def editar_registro():
        item = treeview.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um registro para editar.")
            return
        valores = treeview.item(item, "values")

        editar_win = tk.Toplevel(root)
        editar_win.title("Editar Registro")

        tk.Label(editar_win, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        entry_nome = tk.Entry(editar_win)
        entry_nome.insert(0, valores[0])
        entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(editar_win, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        entry_email = tk.Entry(editar_win)
        entry_email.insert(0, valores[1])
        entry_email.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(editar_win, text="Cursos:").grid(row=2, column=0, padx=5, pady=5)
        entry_cursos = tk.Entry(editar_win)
        entry_cursos.insert(0, valores[3])
        entry_cursos.grid(row=2, column=1, padx=5, pady=5)

        def salvar_edicao():
            novo_nome = entry_nome.get()
            novo_email = entry_email.get()
            novo_cursos = entry_cursos.get()
            cadastro_id = valores[2]

            # Verificar se existe outro usuário com o mesmo email
            cursor_local.execute("SELECT cadastro FROM emails WHERE email = ? AND cadastro != ?", (novo_email, cadastro_id))
            if cursor_local.fetchone():
                messagebox.showerror("Erro", "Email já cadastrado para outro usuário.", parent=editar_win)
                return

            cursor_local.execute("UPDATE emails SET nome=?, email=?, cursos=? WHERE cadastro=?", (novo_nome, novo_email, novo_cursos, cadastro_id))
            conn.commit()

            # Atualizar na Treeview
            treeview.item(item, values=(novo_nome, novo_email, cadastro_id, novo_cursos, valores[4]))
            editar_win.destroy()
            messagebox.showinfo("Sucesso", "Registro atualizado com sucesso.", parent=root)

        btn_salvar = tk.Button(editar_win, text="Salvar", command=salvar_edicao)
        btn_salvar.grid(row=3, column=1, pady=10)

    def excluir_registro():
        item = treeview.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um registro para excluir.")
            return
        valores = treeview.item(item, "values")
        if messagebox.askyesno("Confirmar", f"Deseja excluir o registro {valores[1]}?"):
            cadastro_id = valores[2]
            cursor_local.execute("DELETE FROM emails WHERE cadastro=?", (cadastro_id,))
            conn.commit()
            treeview.delete(item)
            messagebox.showinfo("Sucesso", "Registro excluído com sucesso.", parent=root)

    btn_exportar = tk.Button(root, text="Exportar para Excel", command=exportar_excel)
    btn_exportar.pack(pady=5)

    btn_editar = tk.Button(root, text="Editar", command=editar_registro)
    btn_editar.pack(pady=5)

    btn_excluir = tk.Button(root, text="Excluir", command=excluir_registro)
    btn_excluir.pack(pady=5)

    def fechar_planilha():
        conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", fechar_planilha)

# JANELA PRINCIPAL
janela = tk.Tk()
janela.title("Cadastro e Login de Email")
janela.geometry("600x400")
img = PhotoImage(file="Baking-Bread-Logo.png")
label_titulo = tk.Label(janela, image=img)
label_titulo.pack(pady=10)

tk.Label(janela, text="Login", font=("Arial", 14)).pack(pady=10)

frame_inputs = tk.Frame(janela)
frame_inputs.pack()

tk.Label(frame_inputs, text="Email:").grid(row=0, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_inputs)
entry_email.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
entry_senha = tk.Entry(frame_inputs, show="*")
entry_senha.grid(row=1, column=1, padx=5, pady=5)

tk.Button(janela, text="Entrar", command=logar).pack(pady=5)
tk.Button(janela, text="Cadastrar", command=abrir_cadastro).pack(pady=5)
tk.Button(janela, text="Ver Planilha", command=abrir_planilha).pack(pady=5)

usuario_logado = None
criar_tabela()
janela.mainloop()