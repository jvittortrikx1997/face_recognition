from database.connection import get_db_connection
from services.image_service import get_solicitantes_images
from services.fraud_detection import get_blacklist_images, compare_images
from models.suspeita import insert_suspeita
from utils.graph import gerar_grafico
from scipy.stats import chi2_contingency

solicitantes_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Solicitantes'
homem_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Homem'
mulher_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Mulher'

db_conn = get_db_connection()
cursor = db_conn.cursor()

solicitantes_images = get_solicitantes_images(solicitantes_dir)
blacklist_images = get_blacklist_images(cursor)

resultados_suspeitas = {
    'Homem': 0,
    'Mulher': 0
}

for solicitante_image in solicitantes_images:
    fraudador_pesid = compare_images(solicitante_image, blacklist_images, homem_dir, cursor, db_conn)
    if fraudador_pesid:
        resultados_suspeitas['Homem'] += 1
        print(f"Fraudador identificado no diretório 'Homem': {fraudador_pesid}")

    fraudador_pesid = compare_images(solicitante_image, blacklist_images, mulher_dir, cursor, db_conn)
    if fraudador_pesid:
        resultados_suspeitas['Mulher'] += 1
        print(f"Fraudador identificado no diretório 'Mulher': {fraudador_pesid}")


total_solicitacoes = len(solicitantes_images)
gerar_grafico(resultados_suspeitas, total_solicitacoes)

observed = [[resultados_suspeitas['Homem'], resultados_suspeitas['Mulher']],
            [total_solicitacoes - resultados_suspeitas['Homem'], total_solicitacoes - resultados_suspeitas['Mulher']]]
chi2, p, dof, expected = chi2_contingency(observed)

print(f"Chi2: {chi2}, p-valor: {p}")

if p < 0.05:
    print("Há evidências suficientes para rejeitar a hipótese nula: existe uma relação significativa entre gênero e correspondências suspeitas.")
else:
    print("Não há evidências suficientes para rejeitar a hipótese nula: não existe uma relação significativa entre gênero e correspondências suspeitas.")

cursor.close()
db_conn.close()