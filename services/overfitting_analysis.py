import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.metrics import calcular_acuracia, calcular_precisao, calcular_recall, calcular_f1_score, calcular_auc_roc
import matplotlib.pyplot as plt


def plot_fitting_analysis(metrics_train, metrics_val, metric_names):
    plt.figure(figsize=(10, 6))

    bar_width = 0.35
    index = range(len(metric_names))

    plt.bar(index, metrics_train, bar_width, label='Treinamento', color='blue')
    plt.bar([i + bar_width for i in index], metrics_val, bar_width, label='Validação', color='orange')

    plt.xlabel('Métricas')
    plt.ylabel('Valores')
    plt.title('Análise de Overfitting/Underfitting')
    plt.xticks([i + bar_width / 2 for i in index], metric_names)
    plt.legend()

    plt.tight_layout()
    plt.show()


def analisar_fitting(y_true, y_pred, y_scores, y_val_true, y_val_pred, y_val_scores):
    acuracia_train = calcular_acuracia(y_true, y_pred)
    precisao_train = calcular_precisao(y_true, y_pred)
    recall_train = calcular_recall(y_true, y_pred)
    f1_train = calcular_f1_score(y_true, y_pred)
    auc_train = calcular_auc_roc(y_true, y_scores)

    acuracia_val = calcular_acuracia(y_val_true, y_val_pred)
    precisao_val = calcular_precisao(y_val_true, y_val_pred)
    recall_val = calcular_recall(y_val_true, y_val_pred)
    f1_val = calcular_f1_score(y_val_true, y_val_pred)
    auc_val = calcular_auc_roc(y_val_true, y_val_scores)

    metric_names = ['Acurácia', 'Precisão', 'Recall', 'F1 Score', 'AUC-ROC']
    metrics_train = [acuracia_train, precisao_train, recall_train, f1_train, auc_train]
    metrics_val = [acuracia_val, precisao_val, recall_val, f1_val, auc_val]

    plot_fitting_analysis(metrics_train, metrics_val, metric_names)

    print("Métricas do Conjunto de Treinamento:")
    print(f"Acurácia: {acuracia_train:.2f}")
    print(f"Precisão: {precisao_train:.2f}")
    print(f"Recall: {recall_train:.2f}")
    print(f"F1 Score: {f1_train:.2f}")
    print(f"AUC-ROC: {auc_train:.2f}\n")

    print("Métricas do Conjunto de Validação:")
    print(f"Acurácia: {acuracia_val:.2f}")
    print(f"Precisão: {precisao_val:.2f}")
    print(f"Recall: {recall_val:.2f}")
    print(f"F1 Score: {f1_val:.2f}")
    print(f"AUC-ROC: {auc_val:.2f}\n")

    if acuracia_train > acuracia_val + 0.05 or f1_train > f1_val + 0.05:
        print("Possível overfitting detectado!")
    else:
        print("Não há sinais de overfitting.")
