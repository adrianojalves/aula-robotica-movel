import matplotlib.pyplot as plt

x = [0,1,2,3,4,5]
y = [0,1,4,9,16,25] #= x²
"""
marker
'o' → Círculo
's' → Quadrado
'x' → Letra "X"
'*' → Estrela
'd' → Losango
"""
plt.plot(x, y, marker='*', linestyle='-', color='b', label="x²")

plt.xlabel("X")
plt.ylabel("Y")

plt.title("Gráfico da função x²")
plt.legend()
plt.grid()
plt.show()