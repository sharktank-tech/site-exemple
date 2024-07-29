import sqlite3
from typing import List, Optional
from random import randint

def criar():
    conn = sqlite3.connect("databases/produtos.db")
    sql = """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        preco TEXT,
        link TEXT,
        imagem BLOB,
        imagem_ext TEXT
    )
    """
    conn.execute(sql)
    conn.close()
    print("\nTabela criada com sucesso\n")

def tudo() -> List[dict]:
    conn = sqlite3.connect("databases/produtos.db")
    sql = "SELECT * FROM produtos"
    cursor = conn.execute(sql)
    produtos = []
    for row in cursor:
        produto = {
            'id': row[0],
            'nome': row[1],
            'descricao': row[2],
            'preco': row[3],
            'link': row[4],
            'imagem': row[5],
            'imagem_ext': row[6]
        }
        produtos.append(produto)
    conn.close()
    return produtos

def inserir(id: Optional[int], nome: str, descricao: str, preco: str, link: str, imagem: Optional[bytes], imagem_ext: str):
    conn = None
    try:
        conn = sqlite3.connect("databases/produtos.db")
        sql = "INSERT INTO produtos (id, nome, descricao, preco, link, imagem, imagem_ext) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn.execute(sql, (id, nome, descricao, preco, link, imagem, imagem_ext))
        conn.commit()
        print("\nRegistro inserido com sucesso\n")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e}")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        if conn:
            conn.close()

def atualizar(id: int, nome: str, descricao: str, preco: str, link: str, imagem: Optional[bytes], imagem_ext: str):
    conn = None
    try:
        conn = sqlite3.connect("databases/produtos.db")
        sql = "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, link = ?, imagem = ?, imagem_ext = ? WHERE id = ?"
        conn.execute(sql, (nome, descricao, preco, link, imagem, imagem_ext, id))
        conn.commit()
        print("\nRegistro atualizado com sucesso\n")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade: {e}")
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e}")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar dados: {e}")
    finally:
        if conn:
            conn.close()

def deletar(id: int):
    conn = None
    try:
        conn = sqlite3.connect("databases/produtos.db")
        sql = "DELETE FROM produtos WHERE id = ?"
        conn.execute(sql, (id,))
        conn.commit()
        print("Registro deletado com sucesso")
    except sqlite3.Error as e:
        print(f"Erro ao deletar dados: {e}")
    finally:
        if conn:
            conn.close()

def menu():
    print("Digite o que deseja fazer\n1 - Selecionar tudo\n2 - Criar tabela\n3 - Inserir dados\n4 - Atualizar dados\n5 - Deletar dados\n6 - Sair")
    entrada = input(': ')

    if entrada == "1" or entrada.lower() == "tudo":
        produtos = tudo()
        for produto in produtos:
            print(produto)

    elif entrada == "2" or entrada.lower() == "criar":
        criar()

    elif entrada == "3" or entrada.lower() == "inserir":
        id = randint(1, 10000)
        nome = input("Digite o nome: ")
        descricao = input("Digite a descrição: ")
        preco = input("Digite o preço: ")
        link = input("Digite o link: ")
        imagem_path = input("Digite o caminho da imagem: ")
        imagem_ext = imagem_path.rsplit('.', 1)[-1].lower() if imagem_path else ''
        imagem_blob = None
        if imagem_path:
            with open(imagem_path, 'rb') as f:
                imagem_blob = f.read()
        inserir(id, nome, descricao, preco, link, imagem_blob, imagem_ext)

    elif entrada == "4" or entrada.lower() == "atualizar":
        id = int(input("Digite o id: "))
        nome = input("Digite o nome: ")
        descricao = input("Digite a descrição: ")
        preco = input("Digite o preço: ")
        link = input("Digite o link: ")
        imagem_path = input("Digite o caminho da nova imagem (deixe em branco para não alterar): ")
        imagem_blob = None
        imagem_ext = ''
        if imagem_path:
            imagem_ext = imagem_path.rsplit('.', 1)[-1].lower()
            with open(imagem_path, 'rb') as f:
                imagem_blob = f.read()
        atualizar(id, nome, descricao, preco, link, imagem_blob, imagem_ext)

    elif entrada == "5" or entrada.lower() == "deletar":
        id = int(input("Digite o id: "))
        deletar(id)

    elif entrada == "6" or entrada.lower() == "sair":
        print("\nSaindo do programa...\n")

    else:
        print("Opção inválida. Tente novamente.")

# Código principal que executa o menu
if __name__ == "__main__":
    menu()
