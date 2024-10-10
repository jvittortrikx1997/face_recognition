def get_pessoa_by_image_id(cursor, image_id):
    query = """
        SELECT p.pesid, p.nome, p.genero
        FROM pessoa p
        JOIN imagem i ON p.pesid = i.pesid
        WHERE i.image_id = %s
    """
    cursor.execute(query, (image_id,))
    return cursor.fetchone()