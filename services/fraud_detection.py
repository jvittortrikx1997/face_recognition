import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import face_recognition
from services.image_service import load_and_encode_image
from models.suspeita import insert_suspeita

def get_blacklist_images(cursor):
    query = """
        SELECT blacklist.pesid, imagem.caminho_imagem 
        FROM blacklist
        INNER JOIN imagem ON blacklist.pesid = imagem.pesid
    """
    cursor.execute(query)
    return [(pesid, os.path.basename(caminho_imagem)) for pesid, caminho_imagem in cursor.fetchall()]

def compare_images(solicitante_image, blacklist_images, base_dir, cursor, db_conn):
    solicitante_encoding = load_and_encode_image(solicitante_image)

    if solicitante_encoding is None:
        return None

    for pesid, fraud_image_name in blacklist_images:
        fraud_image_path = os.path.join(base_dir, fraud_image_name)
        if os.path.isfile(fraud_image_path):
            fraud_encoding = load_and_encode_image(fraud_image_path)

            if fraud_encoding is None:
                continue

            match = face_recognition.compare_faces([fraud_encoding], solicitante_encoding)
            if match[0]:
                insert_suspeita(cursor, db_conn, pesid, solicitante_image)
                return pesid
    return None