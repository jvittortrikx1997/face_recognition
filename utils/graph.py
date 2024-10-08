import matplotlib.pyplot as plt

def gerar_grafico(resultados_suspeitas, total_solicitacoes):
    labels = list(resultados_suspeitas.keys())
    values = list(resultados_suspeitas.values())

    plt.bar(labels, values, color=['blue', 'orange'])
    plt.title('Número de Correspondências Suspeitas por Gênero')
    plt.xlabel('Gênero')
    plt.ylabel('Número de Correspondências')
    plt.axhline(y=total_solicitacoes/len(labels), color='r', linestyle='--', label='Média de Solicitações')
    plt.legend()
    plt.show()