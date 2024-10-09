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
