from rich import print_json
from database.connection import get_db_connection
from services.image_service import get_solicitantes_images
from services.fraud_detection import get_blacklist_images, compare_images
from models.suspeita import insert_suspeita
from utils.graph import gerar_grafico
from utils.metrics import calcular_acuracia, calcular_precisao, calcular_recall, calcular_f1_score, calcular_auc_roc, plot_metrica
from services.overfitting_analysis import analisar_fitting
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

solicitantes_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Solicitantes'
homem_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Homem_Blacklist'
mulher_dir = r'C:\Users\joao.mendonca\Desktop\face_recognition\Mulher_Blacklist'

db_conn = get_db_connection()
cursor = db_conn.cursor()

solicitantes_images = get_solicitantes_images(solicitantes_dir)
blacklist_images = get_blacklist_images(cursor)

resultados_suspeitas = {'Homem': 0, 'Mulher': 0}

y_true = []
y_pred = []
y_scores = []

split_index = int(len(solicitantes_images) * 0.7)
solicitantes_train = solicitantes_images[:split_index]
solicitantes_val = solicitantes_images[split_index:]

for solicitante_image in solicitantes_train:
    fraudador_pesid = compare_images(solicitante_image, blacklist_images, homem_dir, cursor, db_conn, is_real_comparison=False)
    if fraudador_pesid:
        resultados_suspeitas['Homem'] += 1
        y_true.append(1)
        y_pred.append(1)
        y_scores.append(0.9)
    else:
        y_true.append(0)
        y_pred.append(0)
        y_scores.append(0.1)

    fraudador_pesid = compare_images(solicitante_image, blacklist_images, mulher_dir, cursor, db_conn, is_real_comparison=False)
    if fraudador_pesid:
        resultados_suspeitas['Mulher'] += 1
        y_true.append(1)
        y_pred.append(1)
        y_scores.append(0.9)
    else:
        y_true.append(0)
        y_pred.append(0)
        y_scores.append(0.1)

y_val_true = []
y_val_pred = []
y_val_scores = []

for solicitante_image in solicitantes_val:
    fraudador_pesid = compare_images(solicitante_image, blacklist_images, homem_dir, cursor, db_conn, is_real_comparison=True)
    if fraudador_pesid:
        y_val_true.append(1)
        y_val_pred.append(1)
        y_val_scores.append(0.9)
    else:
        y_val_true.append(0)
        y_val_pred.append(0)
        y_val_scores.append(0.1)

    fraudador_pesid = compare_images(solicitante_image, blacklist_images, mulher_dir, cursor, db_conn, is_real_comparison=True)
    if fraudador_pesid:
        y_val_true.append(1)
        y_val_pred.append(1)
        y_val_scores.append(0.9)
    else:
        y_val_true.append(0)
        y_val_pred.append(0)
        y_val_scores.append(0.1)

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

analisar_fitting(y_true, y_pred, y_scores, y_val_true, y_val_pred, y_val_scores)

plot_metrica(['Acurácia', 'Precisão', 'Recall', 'F1 Score', 'AUC-ROC'],
              [acuracia, precisao, recall, f1, auc],
              0.5)

total_solicitacoes = len(solicitantes_images)
gerar_grafico(resultados_suspeitas, total_solicitacoes)

observed = [[resultados_suspeitas['Homem'], resultados_suspeitas['Mulher']],
            [total_solicitacoes - resultados_suspeitas['Homem'], total_solicitacoes - resultados_suspeitas['Mulher']]]

categorias = ['Homens Suspeitos', 'Mulheres Suspeitas', 'Homens Não Suspeitos', 'Mulheres Não Suspeitas']
valores = [observed[0][0], observed[0][1], observed[1][0], observed[1][1]]

plt.bar(categorias, valores, color=['blue', 'pink', 'blue', 'pink'])

plt.title('Contagem de Suspeitas por Gênero')
plt.xlabel('Categoria')
plt.ylabel('Contagem')

plt.show()

cursor.close()
db_conn.close()
