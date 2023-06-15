import matplotlib.pyplot as plt
import numpy as np
import os

def plot_concentration(inv_temp, result_n, n1, n2, n3, n4, n5, ni):
    plt.figure(figsize = (10, 10))
    change_index = 0
    for i in range(len(inv_temp)):
        if n2[i] < n1[i]:
            change_index = i
            break
    plt.ylim([10**13, 10**19])
    plt.xlim([0, inv_temp[i]+7])
    colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    plt.semilogy(inv_temp, result_n, label = 'Итоговая концентрация', linewidth = 5, color = '#1f77b4')
    random_color = np.random.randint(0, len(colors)-1)
    plt.semilogy(inv_temp, n1, label = 'Компенсация примеси', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.semilogy(inv_temp, n2, label = 'Ионизация примеси', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.semilogy(inv_temp, n3, label = 'Инонизация -> истощение примеси', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.semilogy(inv_temp, n4, label = 'Истощение примеси', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.semilogy(inv_temp, n5, label = 'Истощение -> собственная проводимость', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.semilogy(inv_temp, ni, label = 'Собственная проводимость', color = colors[random_color])
    plt.xlabel("1000/T, 1/К")
    plt.ylabel("p, см^(-3)")
    plt.legend()
    plt.grid()
    plt.title("Зависимость концентрации от обратной температуры")
    if not os.path.exists("results"):
        os.makedirs("results")
    plt.savefig("results\\concentration.png", dpi = 600)
    plt.close()

def plot_Fermi(temp, Ec, Ev, F, Fi, doping_level, mode):
    plt.figure(figsize = (10, 10))
    colors = ['#ff7f0e','#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    random_color = np.random.randint(0, len(colors)-1)
    plt.plot(temp, Ec, label = 'Ec', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.plot(temp, Ev, label ='Ev', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.plot(temp, F, label = 'F', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.plot(temp, Fi, label = 'Fi', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.plot(temp, doping_level, label = 'Ed' if mode == 'electron' else "Ea", color = colors[random_color])
    plt.xlim([0, temp[-1]])
    plt.legend()
    plt.grid()
    plt.title("Зависимость уровня Ферми от температуры")
    plt.xlabel("T, К")
    plt.ylabel("E, эВ")
    plt.savefig("results\\Fermi.png", dpi = 600)
    plt.close()

def plot_mobility(temp, mobility, mobility_tkr, mobility_KV, mode):
    plt.figure(figsize = (10, 10))
    colors = ['#ff7f0e','#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    random_color = np.random.randint(0, len(colors)-1)
    plt.loglog(temp, mobility, label = 'μ общ', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.loglog(temp, mobility_tkr, label = 'μ т.к.р.', color = colors[random_color])
    colors.remove(colors[random_color])
    random_color = np.random.randint(0, len(colors)-1)
    plt.loglog(temp, mobility_KV, label = 'μ и.п.', color = colors[random_color])
    plt.xlim([1, temp[-1]])
    plt.legend()
    plt.grid()
    plt.xlabel("T, К")
    plt.ylabel("μ общ")
    if mode == "electron":
        plt.title("Зависимость подвижности электронов от температуры")
        plt.savefig("results\\mobility_e.png", dpi = 600)
    else:
        plt.title("Зависимость подвижности дырок от температуры")
        plt.savefig("results\\mobility_p.png", dpi = 600)
    plt.close()

def plot_conductivity(inv_temp, conductivity):
    plt.figure(figsize = (10, 10))
    plt.semilogy(inv_temp, conductivity)
    plt.xlim([0.1, 20])
    plt.ylim([pow(10,-5), np.max(conductivity)*10])
    plt.grid()
    plt.title("Зависимость электропроводности от обратной температуры")
    plt.xlabel("1000/T, 1/К")
    plt.ylabel("σ, (Ом*см)^(-1)")
    plt.savefig("results\\conductivity.png", dpi = 600)
    plt.close()

def plot_TEDS(temp, alpha):
    plt.figure(figsize = (10, 10))
    plt.plot(temp, alpha)
    plt.xlim([0, temp[-1]])
    plt.grid()
    plt.savefig("results\\TEDS.png", dpi = 600)