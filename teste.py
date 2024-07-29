import sqlite3
from typing import List, Optional, Tuple

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
    except sqlite3.Error as e:
        print(f"Erro ao deletar dados: {e}")
    finally:
        if conn:
            conn.close()
