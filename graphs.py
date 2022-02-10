import matplotlib.pyplot as plt
from math import log10

def plot_times(x, t_1, t_2, name_1="MRL98", name_2="Munro-Paterson"):
    x = [log10(elem) for elem in x]
    plt.plot(x, t_1, label=name_1)
    plt.plot(x, t_2, label=name_2)
    plt.xlabel('Dataset size, lg(N)')
    plt.ylabel('Time, s')
    plt.title('Execution time - {} vs {}'.format(name_1, name_2))
    plt.legend()
    plt.savefig('time.png')
    plt.show()


def plot_memory_consumption(x, mem_1, mem_2, name_1="MRL98", name_2="Munro-Paterson"):
    x = [log10(elem) for elem in x]
    plt.plot(x, mem_1, label=name_1)
    plt.plot(x, mem_2, label=name_2)
    plt.xlabel('Dataset size, lg(N)')
    plt.ylabel('Memory, bytes')
    plt.title('Memory consumption - {} vs {}'.format(name_1, name_2))
    plt.legend()
    plt.savefig('memory.png')
    plt.show()


