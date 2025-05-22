import matplotlib.pyplot as plt

def plotar_trajeto(posicoes, pos_base, pos_vitima, nome_arquivo="trajeto.png"):
    posicoes = list(posicoes)
    if not posicoes:
        return
    xs, ys = zip(*posicoes)
    plt.figure(figsize=(8, 6))
    plt.plot(xs, ys, 'b-', label='Trajetória do robô')
    plt.plot(pos_base[0], pos_base[1], 'go', label='Base')
    plt.plot(pos_vitima[0], pos_vitima[1], 'ro', label='Vítima')
    plt.legend()
    plt.title("Missão de Resgate - Trajetória do Robô")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid()
    plt.axis("equal")
    plt.savefig(nome_arquivo)
    plt.show()