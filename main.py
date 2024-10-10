from database.connection import get_db_connection
from services.image_service import get_solicitantes_images
from services.fraud_detection import get_blacklist_images, compare_images
from models.suspeita import insert_suspeita
from utils.graph import gerar_grafico
from utils.metrics import calcular_acuracia, calcular_precisao, calcular_recall, calcular_f1_score, calcular_auc_roc, plot_metrica
from scipy.stats import chi2_contingency

solicitantes_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Solicitantes'
homem_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Homem_Blacklist'
mulher_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Mulher_Blacklist'

db_conn = get_db_connection()
cursor = db_conn.cursor()

solicitantes_images = get_solicitantes_images(solicitantes_dir)
blacklist_images = get_blacklist_images(cursor)

resultados_suspeitas = {
    'Homem': 0,
    'Mulher': 0
}

y_true = []
y_pred = []
y_scores = []

for solicitante_image in solicitantes_images:
    fraudador_pesid = compare_images(solicitante_image, blacklist_images, homem_dir, cursor, db_conn)
    if fraudador_pesid:
        resultados_suspeitas['Homem'] += 1
        y_true.append(1)
        y_pred.append(1)
        y_scores.append(0.9)
        print(f"Fraudador identificado no diretório 'Homem': {fraudador_pesid}")
    else:
        y_true.append(0)
        y_pred.append(0)
        y_scores.append(0.1)

    fraudador_pesid = compare_images(solicitante_image, blacklist_images, mulher_dir, cursor, db_conn)
    if fraudador_pesid:
        resultados_suspeitas['Mulher'] += 1
        y_true.append(1)
        y_pred.append(1)
        y_scores.append(0.9)
        print(f"Fraudador identificado no diretório 'Mulher': {fraudador_pesid}")
    else:
        y_true.append(0)
        y_pred.append(0)
        y_scores.append(0.1)

acuracia = calcular_acuracia(y_true, y_pred)
precisao = calcular_precisao(y_true, y_pred)
recall = calcular_recall(y_true, y_pred)
f1 = calcular_f1_score(y_true, y_pred)
auc = calcular_auc_roc(y_true, y_scores)

print(f"Acurácia: {acuracia:.2f}")
print(f"Precisão: {precisao:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print(f"AUC-ROC: {auc:.2f}")

plot_metrica(['Acurácia', 'Precisão', 'Recall', 'F1 Score', 'AUC-ROC'],
              [acuracia, precisao, recall, f1, auc],
              0.5)

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