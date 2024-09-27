import os
import mysql.connector
import face_recognition
from datetime import datetime

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'tcc'
}


def connect_to_database(config):
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None


def get_images_from_directory(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)
            if file.endswith(('jpg', 'jpeg', 'png'))]


def get_blacklist_images(cursor):
    query = """
        SELECT blacklist.pesid, imagem.caminho_imagem 
        FROM blacklist
        INNER JOIN imagem ON blacklist.pesid = imagem.pesid
    """
    cursor.execute(query)
    return [(pesid, os.path.basename(caminho_imagem)) for pesid, caminho_imagem in cursor.fetchall()]


def compare_images(solicitante_image, blacklist_images, blacklist_dir):
    try:
        solicitante_img = face_recognition.load_image_file(solicitante_image)
        solicitante_encoding = face_recognition.face_encodings(solicitante_img)

        if not solicitante_encoding:
            print(f"Falha ao codificar a imagem: {solicitante_image}")
            return None

        for pesid, blacklist_image in blacklist_images:
            blacklist_image_path = os.path.join(blacklist_dir, blacklist_image)
            if os.path.isfile(blacklist_image_path):
                fraud_img = face_recognition.load_image_file(blacklist_image_path)
                fraud_encoding = face_recognition.face_encodings(fraud_img)

                if fraud_encoding and face_recognition.compare_faces([fraud_encoding[0]], solicitante_encoding[0])[0]:
                    return pesid

    except Exception as e:
        print(f"Erro ao comparar imagens: {e}")
    return None


def insert_suspeita(cursor, pesid):
    """Insere um registro de suspeita no banco de dados."""
    try:
        now = datetime.now()
        query = "INSERT INTO solicitacao_suspeita (pesid, data) VALUES (%s, %s)"
        cursor.execute(query, (pesid, now))
        print(f"Suspeita registrada para pesid: {pesid}")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir suspeita: {err}")


def process_images(db_conn, solicitantes_images, blacklist_images, blacklist_dir):
    cursor = db_conn.cursor()

    for solicitante_image in solicitantes_images:
        print(f"Processando imagem: {solicitante_image}")

        pesid = compare_images(solicitante_image, blacklist_images, blacklist_dir)

        if pesid:
            insert_suspeita(cursor, pesid)

    db_conn.commit()
    cursor.close()


def main():
    db_conn = connect_to_database(db_config)
    if not db_conn:
        return

    solicitantes_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Solicitantes'
    blacklist_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\blacklist'

    try:
        solicitantes_images = get_images_from_directory(solicitantes_dir)

        cursor = db_conn.cursor()
        blacklist_images = get_blacklist_images(cursor)

        if not solicitantes_images:
            print("Nenhuma imagem de solicitante encontrada.")
        else:
            process_images(db_conn, solicitantes_images, blacklist_images, blacklist_dir)

    finally:
        db_conn.close()


if __name__ == "__main__":
    main()
