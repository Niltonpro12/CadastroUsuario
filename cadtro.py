import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk
import bcrypt

# Função para conectar ao banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="Kally",  # Substitua pelo seu usuário do MySQL
        password="MANOvino17@",  # Substitua pela sua senha do MySQL
        database="Ncangaza"
    )

# Função para criptografar a senha usando bcrypt
def criptografar_senha(senha):
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode(), salt)
    return senha_hash

# Função para verificar a senha durante o login
def verificar_senha(senha_inserida, senha_armazenada):
    return bcrypt.checkpw(senha_inserida.encode(), senha_armazenada.encode())

# Função para cadastrar o usuário
def cadastrar_usuario():
    nome = entry_nome.get()
    funcao = combo_funcao.get()
    senha = entry_senha.get()

    # Verificação se os campos estão preenchidos
    if not nome or not funcao or not senha:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return

    senha_criptografada = criptografar_senha(senha)

    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        sql = "INSERT INTO Usuarios_nms (Nome, Funcao, Senha) VALUES (%s, %s, %s)"
        valores = (nome, funcao, senha_criptografada)
        cursor.execute(sql, valores)
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {err}")
    finally:
        cursor.close()
        conn.close()

# Função para limpar os campos
def limpar_campos():
    if entry_nome.get() or entry_senha.get() or combo_funcao.get():
        entry_nome.delete(0, tk.END)
        entry_senha.delete(0, tk.END)
        combo_funcao.set("")
        messagebox.showinfo("Limpar", "Campos limpos com sucesso!")
    else:
        messagebox.showwarning("Aviso", "Não há dados para limpar.")

# Função para apagar um usuário específico
def apagar_usuario():
    nome = entry_nome.get()
    if not nome:
        messagebox.showwarning("Aviso", "Por favor, insira o nome do usuário a ser apagado.")
        return

    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        sql = "DELETE FROM Usuarios_nms WHERE Nome = %s"
        cursor.execute(sql, (nome,))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Sucesso", "Usuário apagado com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum usuário encontrado com esse nome.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao apagar usuário: {err}")
    finally:
        cursor.close()
        conn.close()

# Função para limpar todos os dados da tabela
def limpar_tabela():
    if messagebox.askokcancel("Limpar Tabela", "Tem certeza de que deseja limpar todos os dados da tabela?"):
        try:
            conn = conectar_banco()
            cursor = conn.cursor()
            sql = "DELETE FROM Usuarios_nms"
            cursor.execute(sql)
            conn.commit()
            messagebox.showinfo("Sucesso", "Todos os dados foram apagados com sucesso!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao limpar a tabela: {err}")
        finally:
            cursor.close()
            conn.close()

# Função para mostrar dados registrados em uma tabela
def mostrar_dados():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios_nms")
        registros = cursor.fetchall()

        dados_janela = tk.Toplevel(root)
        dados_janela.title("Usuários Registrados")

        tree = ttk.Treeview(dados_janela, columns=("ID", "Nome", "Função", "Senha"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Função", text="Função")
        tree.heading("Senha", text="Senha")
        tree.pack(fill=tk.BOTH, expand=True)

        for registro in registros:
            tree.insert("", tk.END, values=registro)

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao buscar dados: {err}")

# Função para sair da aplicação
def sair_aplicacao():
    if messagebox.askokcancel("Sair", "Tem certeza de que deseja sair?"):
        root.destroy()

# Configurar a interface gráfica
root = tk.Tk()
root.title("Cadastro de Usuários")
root.geometry("400x400")

# Adicionar logotipo
logo_image = Image.open("C:/Users/NILTON RPN/Downloads/logo Nms.png")  # Atualize para o caminho correto
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photo)
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Nome da aplicação
tk.Label(root, text="Cadastro de Usuários", font=("Helvetica", 16)).grid(row=1, column=0, columnspan=2, pady=10)

# Campo para inserir o nome
tk.Label(root, text="Nome:").grid(row=2, column=0, padx=10, pady=10)
entry_nome = tk.Entry(root)
entry_nome.grid(row=2, column=1, padx=10, pady=10)

# Campo para selecionar a função
tk.Label(root, text="Função:").grid(row=3, column=0, padx=10, pady=10)
combo_funcao = ttk.Combobox(root, values=["Admin", "Operador", "Chefe"])
combo_funcao.grid(row=3, column=1, padx=10, pady=10)

# Campo para inserir a senha
tk.Label(root, text="Senha:").grid(row=4, column=0, padx=10, pady=10)
entry_senha = tk.Entry(root, show="*")
entry_senha.grid(row=4, column=1, padx=10, pady=10)

# Botões para as funcionalidades
tk.Button(root, text="Cadastrar", command=cadastrar_usuario).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Limpar Campos", command=limpar_campos).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Apagar Usuário", command=apagar_usuario).grid(row=6, column=0, padx=10, pady=10)
tk.Button(root, text="Limpar Tabela", command=limpar_tabela).grid(row=6, column=1, padx=10, pady=10)
tk.Button(root, text="Mostrar Dados", command=mostrar_dados).grid(row=7, column=0, padx=10, pady=10)
tk.Button(root, text="Sair", command=sair_aplicacao).grid(row=7, column=1, padx=10, pady=10)

root.mainloop()
