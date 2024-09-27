import mysql.connector
import face_recognition
import os
from datetime import datetime

db_config = {
    'user': 'root',
    'password': '040498',
    'host': 'localhost',
    'database': 'tcc'
}

db_conn = mysql.connector.connect(**db_config)
cursor = db_conn.cursor()

def get_solicitantes_images(directory):
    images = []
    for file in os.listdir(directory):
        if file.endswith(('jpg', 'jpeg', 'png')):
            images.append(os.path.join(directory, file))
    return images

def get_blacklist_images():
    query = """
        SELECT blacklist.pesid, imagem.caminho_imagem 
        FROM blacklist
        INNER JOIN imagem ON blacklist.pesid = imagem.pesid
    """
    cursor.execute(query)
    return cursor.fetchall()

def compare_images(solicitante_image, blacklist_images):
    solicitante_img = face_recognition.load_image_file(solicitante_image)
    solicitante_encoding = face_recognition.face_encodings(solicitante_img)

    if not solicitante_encoding:
        return None

    for pesid, fraud_image in blacklist_images:
        fraud_img = face_recognition.load_image_file(fraud_image)
        fraud_encoding = face_recognition.face_encodings(fraud_img)

        if not fraud_encoding:
            continue

        match = face_recognition.compare_faces([fraud_encoding[0]], solicitante_encoding[0])
        if match[0]:
            return pesid
    return None

def insert_suspeita(pesid):
    now = datetime.now()
    query = "INSERT INTO solicitacao_suspeita (pesid, data) VALUES (%s, %s)"
    cursor.execute(query, (pesid, now))
    db_conn.commit()

solicitantes_dir = r'C:\Users\vitor\PycharmProjects\face_recognition\Solicitantes'

solicitantes_images = get_solicitantes_images(solicitantes_dir)

blacklist_images = get_blacklist_images()

for solicitante_image in solicitantes_images:
    fraudador_pesid = compare_images(solicitante_image, blacklist_images)
    if fraudador_pesid:

        insert_suspeita(fraudador_pesid)
        print(f"Fraudador identificado: {fraudador_pesid}")

cursor.close()
db_conn.close()
