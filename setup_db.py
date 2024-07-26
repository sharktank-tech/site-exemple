import sqlite3


def tudo():
    conn = sqlite3.connect("databases/produtos.db")
    sql = "SELECT * FROM produtos WHERE nome == 'HyperX'"
    cursor = conn.execute(sql)
    for row in cursor:
        print(row)
    conn.close()
    print('\n---------------------\n')

tudo()