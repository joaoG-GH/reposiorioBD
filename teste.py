import customtkinter as ctk
from tkinter import messagebox
from pymongo import MongoClient
import hashlib

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

MONGO_URI = "mongodb+srv://root:123@cluster0.uluij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['projeto4bim']
usuarios_collection = db['usuarios']
registros_collection = db['registros']  # Coleção para armazenar registros de pacientes

def abrir_tela_principal():
    for widget in root.winfo_children():
        widget.destroy()

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(pady=20)

    tabview = ctk.CTkTabview(main_frame)
    tabview.pack(pady=20, fill="both", expand=True)

    tabview.add("Criar Registros")
    tabview.add("Alterar Registros")
    tabview.add("Excluir Registros")
    tabview.add("Mostrar Registros")

    criar_frame = ctk.CTkFrame(tabview.tab("Criar Registros"))
    criar_frame.pack(pady=20, padx=20)

    paciente_label = ctk.CTkLabel(criar_frame, text="Nome do Paciente:", font=("Roboto", 14))
    paciente_label.pack(pady=5)
    paciente_entry = ctk.CTkEntry(criar_frame, placeholder_text="Nome do Paciente", width=300)
    paciente_entry.pack(pady=5)

    historico_label = ctk.CTkLabel(criar_frame, text="Histórico Médico:", font=("Roboto", 14))
    historico_label.pack(pady=5)
    historico_entry = ctk.CTkEntry(criar_frame, placeholder_text="Histórico Médico", width=300)
    historico_entry.pack(pady=5)

    tratamento_label = ctk.CTkLabel(criar_frame, text="Tratamento:", font=("Roboto", 14))
    tratamento_label.pack(pady=5)
    tratamento_entry = ctk.CTkEntry(criar_frame, placeholder_text="Tratamento", width=300)
    tratamento_entry.pack(pady=5)

    def salvar_registro():
        nome_paciente = paciente_entry.get()
        historico_medico = historico_entry.get()
        tratamento = tratamento_entry.get()

        if nome_paciente and historico_medico and tratamento:
            registros_collection.insert_one({
                "nome_paciente": nome_paciente,
                "historico_medico": historico_medico,
                "tratamento": tratamento
            })
            messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")
            paciente_entry.delete(0, 'end')
            historico_entry.delete(0, 'end')
            tratamento_entry.delete(0, 'end')
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    salvar_btn = ctk.CTkButton(criar_frame, text="Salvar Registro", command=salvar_registro, width=300)
    salvar_btn.pack(pady=10)

    def mostrar_registros(mostrar_frame):
        for widget in mostrar_frame.winfo_children():
            widget.destroy()

        registros = registros_collection.find()
        for registro in registros:
            registro_label = ctk.CTkLabel(mostrar_frame, text=f"Paciente: {registro['nome_paciente']}, "
                                                               f"Histórico: {registro['historico_medico']}, "
                                                               f"Tratamento: {registro['tratamento']}", font=("Roboto", 12))
            registro_label.pack(pady=5)

    def alterar_registro(registro_id):
        registro = registros_collection.find_one({"_id": registro_id})

        def salvar_alteracoes():
            novo_nome = nome_entry.get()
            novo_historico = historico_entry.get()
            novo_tratamento = tratamento_entry.get()

            if novo_nome and novo_historico and novo_tratamento:
                registros_collection.update_one(
                    {"_id": registro_id},
                    {"$set": {
                        "nome_paciente": novo_nome,
                        "historico_medico": novo_historico,
                        "tratamento": novo_tratamento
                    }}
                )
                messagebox.showinfo("Sucesso", "Registro alterado com sucesso!")
                alterar_window.destroy()
                mostrar_registros_para_alterar()
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

        alterar_window = ctk.CTkToplevel(root)
        alterar_window.title("Alterar Registro")

        nome_label = ctk.CTkLabel(alterar_window, text="Nome do Paciente:", font=("Roboto", 14))
        nome_label.pack(pady=5)
        nome_entry = ctk.CTkEntry(alterar_window, placeholder_text="Nome do Paciente", width=300)
        nome_entry.insert(0, registro['nome_paciente'])
        nome_entry.pack(pady=5)

        historico_label = ctk.CTkLabel(alterar_window, text="Histórico Médico:", font=("Roboto", 14))
        historico_label.pack(pady=5)
        historico_entry = ctk.CTkEntry(alterar_window, placeholder_text="Histórico Médico", width=300)
        historico_entry.insert(0, registro['historico_medico'])
        historico_entry.pack(pady=5)

        tratamento_label = ctk.CTkLabel(alterar_window, text="Tratamento:", font=("Roboto", 14))
        tratamento_label.pack(pady=5)
        tratamento_entry = ctk.CTkEntry(alterar_window, placeholder_text="Tratamento", width=300)
        tratamento_entry.insert(0, registro['tratamento'])
        tratamento_entry.pack(pady=5)

        salvar_btn = ctk.CTkButton(alterar_window, text="Salvar Alterações", command=salvar_alteracoes, width=300)
        salvar_btn.pack(pady=10)

    def excluir_registro(registro_id):
        registros_collection.delete_one({"_id": registro_id})
        messagebox.showinfo("Sucesso", "Registro excluído com sucesso!")
        mostrar_registros_para_excluir()

    alterar_frame = ctk.CTkFrame(tabview.tab("Alterar Registros"))
    alterar_frame.pack(pady=20, padx=20)

    def mostrar_registros_para_alterar():
        mostrar_registros(alterar_frame)

        for registro in registros_collection.find():
            alterar_btn = ctk.CTkButton(alterar_frame, text="Alterar", command=lambda reg_id=registro['_id']: alterar_registro(reg_id))
            alterar_btn.pack(pady=5)

    mostrar_registros_para_alterar()

    excluir_frame = ctk.CTkFrame(tabview.tab("Excluir Registros"))
    excluir_frame.pack(pady=20, padx=20)

    def mostrar_registros_para_excluir():
        mostrar_registros(excluir_frame)

        for registro in registros_collection.find():
            excluir_btn = ctk.CTkButton(excluir_frame, text="Excluir", command=lambda reg_id=registro['_id']: excluir_registro(reg_id))
            excluir_btn.pack(pady=5)

    mostrar_registros_para_excluir()

    mostrar_frame = ctk.CTkFrame(tabview.tab("Mostrar Registros"))
    mostrar_frame.pack(pady=20, padx=20)

    mostrar_registros(mostrar_frame)

    logout_btn = ctk.CTkButton(main_frame, text="Sair", command=root.quit, width=300)
    logout_btn.pack(pady=10)

def realizar_login():
    usuario = login_usuario_entry.get()
    senha = login_senha_entry.get()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    usuario_encontrado = usuarios_collection.find_one({
        "usuario": usuario,
        "senha": senha_hash
    })

    if usuario_encontrado:
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        abrir_tela_principal()  # Chama a função para abrir a tela principal
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

def realizar_cadastro():
    usuario = cadastro_usuario_entry.get()
    senha = cadastro_senha_entry.get()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    usuario_encontrado = usuarios_collection.find_one({"usuario": usuario})

    if usuario_encontrado:
        messagebox.showerror("Atenção!", "Este usuário já está cadastrado no BD!")
    else:
        usuarios_collection.insert_one({"usuario": usuario, "senha": senha_hash})
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        cadastro_usuario_entry.delete(0, 'end')
        cadastro_senha_entry.delete(0, 'end')
        mostrar_login()

def mostrar_login():
    login_frame.pack(pady=20)
    cadastro_frame.pack_forget()

def mostrar_cadastro():
    cadastro_frame.pack(pady=20)
    login_frame.pack_forget()

root = ctk.CTk()
root.title("Sistema de Login")
root.geometry("400x300")

login_frame = ctk.CTkFrame(root)
login_frame.pack(pady=20)

login_title = ctk.CTkLabel(login_frame, text="Login", font=("Roboto", 24, "bold"))
login_title.pack(pady=10)

login_usuario_entry = ctk.CTkEntry(login_frame, placeholder_text="Usuário", width=300)
login_usuario_entry.pack(pady=10)

login_senha_entry = ctk.CTkEntry(login_frame, placeholder_text="Senha", show="*", width=300)
login_senha_entry.pack(pady=10)

login_btn = ctk.CTkButton(login_frame, text="Entrar", command=realizar_login, width=300)
login_btn.pack(pady=10)

cadastro_link = ctk.CTkButton(login_frame, text="Não tem uma conta? Cadastre-se", command=mostrar_cadastro, width=300)
cadastro_link.pack(pady=10)

cadastro_frame = ctk.CTkFrame(root)

cadastro_title = ctk.CTkLabel(cadastro_frame, text="Cadastro", font=("Roboto", 24, "bold"))
cadastro_title.pack(pady=10)

cadastro_usuario_entry = ctk.CTkEntry(cadastro_frame, placeholder_text="Usuário", width=300)
cadastro_usuario_entry.pack(pady=10)

cadastro_senha_entry = ctk.CTkEntry(cadastro_frame, placeholder_text="Senha", show="*", width=300)
cadastro_senha_entry.pack(pady=10)

cadastro_btn = ctk.CTkButton(cadastro_frame, text="Cadastrar", command=realizar_cadastro, width=300)
cadastro_btn.pack(pady=10)

login_link = ctk.CTkButton(cadastro_frame, text="Já tem uma conta? Faça login", command=mostrar_login, width=300)
login_link.pack(pady=10)

mostrar_login()
root.mainloop()