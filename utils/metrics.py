import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def calcular_acuracia(y_true, y_pred):
    return accuracy_score(y_true, y_pred)

def calcular_precisao(y_true, y_pred):
    return precision_score(y_true, y_pred)

def calcular_recall(y_true, y_pred):
    return recall_score(y_true, y_pred)

def calcular_f1_score(y_true, y_pred):
    return f1_score(y_true, y_pred)

def calcular_auc_roc(y_true, y_scores):
    return roc_auc_score(y_true, y_scores)

def plot_metrica(metrica_nome, valores, metrica_valor):
    plt.figure(figsize=(10, 5))
    plt.bar(metrica_nome, valores, color=['blue', 'orange', 'green', 'red'])
    plt.axhline(y=metrica_valor, color='grey', linestyle='--', label='Valor Métrica')
    plt.title('Métricas de Desempenho')
    plt.xlabel('Métricas')
    plt.ylabel('Valor')
    plt.ylim(0, max(valores) + 0.1)
    plt.legend()
    plt.grid(axis='y')
    plt.show()