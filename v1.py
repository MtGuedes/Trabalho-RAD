import tkinter
from tkinter import messagebox as mb
from tkinter import Tk
import sqlite3

#começar com tela com um botão e um entry (nome)- v1
#adicionar mais duas entrys (cpf e estado) e suas labels - v2
#mudar o fundo para uma imagem mais bonita, adicionar readme.txt explicando como usar - v3
#adicionar clicar no botão salva os 3 dados em um sqlite - v4
#Criar uma branch em que le um config.txt com uma lista de 5 estados possiveis separados por pular linha - x1
#Mudar o separador para ; e adicionar mais 5 estados - x2
#Voltar para main, criar outra branch e criar um dropdown com 3 opções (clt, mei, socio) - y1
#Voltar para main, Corrigir o bug da função de cpf - v5
#Merge de x com v - v6
#Adicionar verificação de CPF e de estado, com base na função cpf e na lista de estados .txt antes de adicionar no sqlite v7

#Cria conexção
def criar_conexao():
    return sqlite3.connect("teste.db")

#Cria o cursos e cria a tabela
def criar_tabela():
    connection = sqlite3.connect("teste.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Tabela1 
                    (nome TEXT, 
                    cpf TEXT,
                    estado TEXT)""")
    connection.commit()
    connection.close()

def ler_estados():
    try:
        with open("config.txt", "r") as file:
            opcoes = file.read().split(";")
            opcoes = [opcao.strip() for opcao in opcoes]
        return opcoes
    except FileNotFoundError:
        print("Arquivo config.txt não encontrado.")
        return []
    
opcoes = ler_estados()
print("Opções no config.txt:", opcoes)

def VerificarCPF(CPF):
    # Remove os pontos e o traço do CPF
    cpf_numeros = CPF.replace(".", "").replace("-", "")
    
    # Verificar se o CPF tem 11 dígitos
    if len(cpf_numeros) != 11:
        return False
    
    # Verificar se todos os caracteres são dígitos
    if not cpf_numeros.isdigit():
        return False
    
    # Verificar se há pelo menos dois dígitos diferentes
    if len(set(cpf_numeros)) == 1:
        return False
    
    # Verificar se o CPF é válido usando o algoritmo de validação
    soma = 0
    multiplicador = 10
    for i in range(9):
        soma += int(cpf_numeros[i]) * multiplicador
        multiplicador -= 1
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf_numeros[9]):
        return False
    
    soma = 0
    multiplicador = 11
    for i in range(10):
        soma += int(cpf_numeros[i]) * multiplicador
        multiplicador -= 1
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf_numeros[10]):
        return False
    
    return True


def inserevalores(cursor, Valor1, Valor2, Valor3):
    cursor.execute("INSERT INTO Tabela1 VALUES (?, ?, ?)", (Valor1, Valor2, Valor3))

connection = criar_conexao()
cursor = connection.cursor()

def pegavalores():
    #Pega valores da tabela
    rows = cursor.execute("SELECT * FROM Tabela1").fetchall()
    print(rows)

def salvar_dados():
    nome = textoNome.get()
    cpf = textoCPF.get()
    estado = textoEstado.get()
    
    connection = criar_conexao()
    cursor = connection.cursor()

    if VerificarCPF(cpf):
        inserevalores(cursor, nome, cpf, estado)
        print("Dados salvos com sucesso!")
    else:
        print("CPF inválido. Por favor, insira um CPF válido.")

    if nome.strip() == "" or cpf.strip() == "" or estado.strip() == "":
        print("Por favor, preencha todos os campos.")
        return

    connection.commit()
    connection.close()
    
import tkinter as ttk

def main():
    root = tkinter.Tk()
    root.title("Trabalho RAD")
    root.geometry("800x600")
    root.resizable(False, False)

    # Carrega as opções de Estados do arquivo config.txt
    opcoes = ler_estados()

    # Carrega a imagem de fundo
    imagem_fundo = tkinter.PhotoImage(file=r"C:\Users\Nina\Downloads\Trabalho Python\Trabalho-RAD\teste.png")

    # Cria um label para a imagem de fundo e exibe-a
    label_fundo = tkinter.Label(root, image=imagem_fundo)
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

    label_nome = tkinter.Label(root, text="Nome")
    label_nome.pack(pady=5)
    global textoNome
    textoNome = tkinter.StringVar()
    entry_nome = tkinter.Entry(root, textvariable=textoNome)
    entry_nome.pack()

    label_cpf = tkinter.Label(root, text="CPF")
    label_cpf.pack()
    global textoCPF
    textoCPF = tkinter.StringVar()
    entry_cpf = tkinter.Entry(root, textvariable=textoCPF)
    entry_cpf.pack(pady=5)

    label_estado = tkinter.Label(root, text="Estado")
    label_estado.pack()

    # Cria a variável para armazenar o Estado selecionado
    global textoEstado
    textoEstado = tkinter.StringVar(root)
    if opcoes:
        textoEstado.set(opcoes[0])
    
    # Cria o menu de opções de Estados
    menu_opcoes = tkinter.OptionMenu(root, textoEstado, *opcoes)
    menu_opcoes.pack(padx=5, pady=5)

    connection = criar_conexao()
    cursor = connection.cursor()

    # Cria o botão "Salvar" e o posiciona abaixo do menu de opções
    btn_salvar = ttk.Button(root, text="Salvar", command=salvar_dados)
    btn_salvar.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()