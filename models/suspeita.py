from datetime import datetime

def insert_suspeita(cursor, pesid, image_path):
    now = datetime.now()
    query = "INSERT INTO solicitacao_suspeita (pesid, data, imagem) VALUES (%s, %s, %s)"
    cursor.execute(query, (pesid, now, image_path))