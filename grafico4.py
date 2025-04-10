import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-10, 10, 100)
#função x²
y = x**2

plt.figure(figsize=(8,6))
plt.plot(x, y, label="y=x²", color='k', linestyle='-', linewidth=2)

plt.xlabel("X")
plt.ylabel("Y")

plt.title("Gráfico função y=x²")
plt.legend()
plt.grid()
plt.show()