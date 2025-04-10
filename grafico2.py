import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(20) * 10 #20 numeros entre 0 e 10
y = np.random.rand(20) * 10

plt.scatter(x, y, c='red', marker='x', label="Pontos aleatórios")
plt.xlabel("X")
plt.ylabel("Y")

plt.title("Gráfico de dispersão")
plt.legend()
plt.grid()
plt.show()