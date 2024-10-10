import datetime

def insert_suspeita(cursor, db_conn, pesid, imagem_caminho):
    data_atual = datetime.datetime.now()
    query = """
        INSERT INTO solicitacao_suspeita (pesid, data, imagem)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (pesid, data_atual, imagem_caminho))
    db_conn.commit()