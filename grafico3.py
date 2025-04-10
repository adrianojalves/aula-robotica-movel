import matplotlib.pyplot as plt

categorias = ['A', 'B', 'C', 'D']
valores = [10,25,7,15]

plt.bar(categorias, valores, color=['blue','green', 'red', 'purple'])

for i, valor in enumerate(valores):
    plt.text(i, valor+0.5, str(valor), ha="center", fontsize=12, fontweight='bold')

plt.xlabel("Categorias")
plt.ylabel("Valores")

plt.title("Gráfico de barras")
plt.show()