import mysql.connector
import face_recognition
import os
from datetime import datetime
import matplotlib.pyplot as plt

db_config = {
    'user': 'root',
    'password': '',
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
    return [(pesid, os.path.basename(caminho_imagem)) for pesid, caminho_imagem in cursor.fetchall()]

def compare_images(solicitante_image, blacklist_images, base_dir):
    solicitante_img = face_recognition.load_image_file(solicitante_image)
    solicitante_encoding = face_recognition.face_encodings(solicitante_img)

    if not solicitante_encoding:
        return None

    for pesid, fraud_image_name in blacklist_images:
        fraud_image_path = os.path.join(base_dir, fraud_image_name)
        if os.path.isfile(fraud_image_path):
            fraud_img = face_recognition.load_image_file(fraud_image_path)
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

def gerar_grafico(resultados_suspeitas):
    labels = list(resultados_suspeitas.keys())
    values = list(resultados_suspeitas.values())

    plt.bar(labels, values, color=['blue', 'orange'])
    plt.title('Número de Correspondências Suspeitas por Diretório')
    plt.xlabel('Diretórios')
    plt.ylabel('Número de Correspondências')

    plt.show()

solicitantes_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Solicitantes'
homem_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Homem'
mulher_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Mulher'

solicitantes_images = get_solicitantes_images(solicitantes_dir)

blacklist_images = get_blacklist_images()

resultados_suspeitas = {
    'Homem': 0,
    'Mulher': 0
}

for solicitante_image in solicitantes_images:
    fraudador_pesid = compare_images(solicitante_image, blacklist_images, homem_dir)
    if fraudador_pesid:
        insert_suspeita(fraudador_pesid)
        resultados_suspeitas['Homem'] += 1
        print(f"Fraudador identificado no diretório 'Homem': {fraudador_pesid}")

    fraudador_pesid = compare_images(solicitante_image, blacklist_images, mulher_dir)
    if fraudador_pesid:
        insert_suspeita(fraudador_pesid)
        resultados_suspeitas['Mulher'] += 1
        print(f"Fraudador identificado no diretório 'Mulher': {fraudador_pesid}")

gerar_grafico(resultados_suspeitas)

cursor.close()
db_conn.close()
