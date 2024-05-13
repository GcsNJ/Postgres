import psycopg2
from psycopg2 import Error

def conectar():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="12345678",
            host="localhost",
            port="5432",
            database="teste"
        )
        return connection
    except (Exception, Error) as error:
        print("Erro ao conectar ao PostgreSQL:", error)
        return None  # Retornar None em caso de falha na conexão

def criar_registro(connection):
    try:
        nome = input("Digite o nome: ")
        idade = int(input("Digite a idade: "))
        email = input("Digite o email: ")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO dados (nome, idade, email) VALUES (%s,%s,%s)"""
        record_to_insert = (nome, idade, email)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        print("Registro criado com sucesso")
    except (Exception, Error) as error:
        print("Erro ao inserir registro:", error)

def ler_registros(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dados")
        registros = cursor.fetchall()
        for row in registros:
            print("ID =", row[0])
            print("Nome =", row[1])
            print("Idade =", row[2])
            print("Email =", row[3], "\n")
    except (Exception, Error) as error:
        print("Erro ao ler registros:", error)

def atualizar_registro(connection):
    try:
        id = int(input("Digite o ID do registro que deseja atualizar: "))
        nome = input("Digite o novo nome: ")
        idade = int(input("Digite a nova idade: "))
        email = input("Digite o novo email: ")
        cursor = connection.cursor()
        postgres_update_query = """UPDATE dados SET nome = %s, idade = %s, email = %s WHERE id = %s"""
        cursor.execute(postgres_update_query, (nome, idade, email, id))
        connection.commit()
        print("Registro atualizado com sucesso")
    except (Exception, Error) as error:
        print("Erro ao atualizar registro:", error)

def excluir_registro(connection):
    try:
        id = int(input("Digite o ID do registro que deseja excluir: "))
        cursor = connection.cursor()
        postgres_delete_query = """DELETE FROM dados WHERE id = %s"""
        cursor.execute(postgres_delete_query, (id,))
        connection.commit()
        print("Registro excluído com sucesso")
    except (Exception, Error) as error:
        print("Erro ao excluir registro:", error)

def menu():
    print("\nMenu:")
    print("1. Criar novo registro")
    print("2. Ler registros")
    print("3. Atualizar registro")
    print("4. Excluir registro")
    print("5. Sair")

# Tentar estabelecer a conexão antes de entrar no loop
connection = conectar()

if connection:
    while True:
        menu()
        escolha = input("Digite a opção desejada: ")

        if escolha == "1":
            criar_registro(connection)
        elif escolha == "2":
            print("Registros atuais:")
            ler_registros(connection)
        elif escolha == "3":
            atualizar_registro(connection)
        elif escolha == "4":
            excluir_registro(connection)
        elif escolha == "5":
            break
        else:
            print("Opção inválida")

    # Fechar a conexão apenas se estiver aberta
    if connection:
        connection.close()
        print("Conexão com PostgreSQL fechada")
else:
    print("Não foi possível estabelecer conexão com o PostgreSQL. Verifique os detalhes de conexão.")
