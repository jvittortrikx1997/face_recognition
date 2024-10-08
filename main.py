import mysql.connector
import face_recognition
import os
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Configuração do banco de dados
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

def gerar_grafico(resultados_suspeitas, total_solicitacoes):
    labels = list(resultados_suspeitas.keys())
    values = list(resultados_suspeitas.values())

    # Gráfico de barras
    plt.bar(labels, values, color=['blue', 'orange'])
    plt.title('Número de Correspondências Suspeitas por Gênero')
    plt.xlabel('Gênero')
    plt.ylabel('Número de Correspondências')
    plt.axhline(y=total_solicitacoes/len(labels), color='r', linestyle='--', label='Média de Solicitações')
    plt.legend()
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

# Gera o gráfico
total_solicitacoes = len(solicitantes_images)
gerar_grafico(resultados_suspeitas, total_solicitacoes)

# Teste Qui-Quadrado
observed = [[resultados_suspeitas['Homem'], resultados_suspeitas['Mulher']],
            [total_solicitacoes - resultados_suspeitas['Homem'], total_solicitacoes - resultados_suspeitas['Mulher']]]
chi2, p, dof, expected = chi2_contingency(observed)

print(f"Chi2: {chi2}, p-valor: {p}")

# Discussão
if p < 0.05:
    print("Há evidências suficientes para rejeitar a hipótese nula: existe uma relação significativa entre gênero e correspondências suspeitas.")
else:
    print("Não há evidências suficientes para rejeitar a hipótese nula: não existe uma relação significativa entre gênero e correspondências suspeitas.")

cursor.close()
db_conn.close()
