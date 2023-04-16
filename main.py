import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
import pygame

def create_graph():
    num_nodes = int(num_nodes_input.get())
    num_edges = int(num_edges_input.get())
    graph_type = graph_type_input.get()
    connected = int(connected_input.get())

    # Создать граф с заданными параметрами
    if graph_type == "Полный":
        G = nx.complete_graph(num_nodes)
    elif graph_type == "Сетка":
        G = nx.grid_2d_graph(num_nodes, num_nodes)
    else:
        diff_nodes_connect = num_nodes - connected + 1
        G = nx.gnm_random_graph(diff_nodes_connect, num_edges)
        if connected > 1:
            max_edges = diff_nodes_connect * (diff_nodes_connect - 1) // 2
            edges_per_ones = (num_edges - max_edges) // (connected - 1)
            for i in range(connected-1):
                G.add_node(diff_nodes_connect + i)
                if i:
                    for _ in range(edges_per_ones):
                        G.add_edge(diff_nodes_connect+i, diff_nodes_connect+i)
                else:
                    for _ in range(num_edges - max_edges - (connected - 2) * edges_per_ones):
                        G.add_edge(diff_nodes_connect+i, diff_nodes_connect+i)

    # Отобразить граф на экране
    nx.draw(G, with_labels=True)
    plt.show()

def select_complete():
    graph_type_input.delete(0, tk.END)
    graph_type_input.insert(0, "Полный")

def select_random():
    graph_type_input.delete(0, tk.END)
    graph_type_input.insert(0, "Случайный")

def select_grid():
    graph_type_input.delete(0, tk.END)
    graph_type_input.insert(0, "Сетка")

def select_connected():
    connected_input.delete(0, tk.END)
    connected_input.insert(0, "Связный")

def update():
    # Получить текущее значение выбранного типа графа

    graph_type = graph_type_input.get()

    # Если выбран тип "Полный", заблокировать поле ввода количества ребер
    if graph_type == "Полный":
        n = int(num_nodes_input.get())
        num_edges_input.delete(0, tk.END)
        num_edges_input.insert(0, str(n * (n - 1) // 2))
        num_edges_input.configure(state='disabled')

    else:
        num_edges_input.configure(state="normal")

    window.after(500, update)

# Создать окно
window = tk.Tk()
window.title("Визуализация графа")

# Создать элементы меню
num_nodes_label = tk.Label(window, text="Количество вершин:")
num_nodes_input = tk.Entry(window)
num_nodes_input.insert(0, "10")

num_edges_label = tk.Label(window, text="Количество ребер:")
num_edges_input = tk.Entry(window)
num_edges_input.insert(0, "20")

graph_type_label = tk.Label(window, text="Тип графа:")
graph_type_input = tk.Entry(window)
graph_type_input.insert(0, "Случайный")
graph_type_button1 = tk.Button(window, text="Полный", command=select_complete)
graph_type_button2 = tk.Button(window, text="Случайный", command=select_random)
graph_type_button3 = tk.Button(window, text="Сетка", command=select_grid)

connected_label = tk.Label(window, text="Компонент связности:")
connected_input = tk.Entry(window)
connected_input.insert(0, "1")

create_button = tk.Button(window, text="Создать граф", command=create_graph)

# Разместить элементы меню на окне
num_nodes_label.grid(row=0, column=0)
num_nodes_input.grid(row=0, column=1)

num_edges_label.grid(row=1, column=0)
num_edges_input.grid(row=1, column=1)

graph_type_label.grid(row=2, column=0)
graph_type_input.grid(row=2, column=1)

graph_type_button1.grid(row=2, column=2)
graph_type_button2.grid(row=2, column=3)
graph_type_button3.grid(row=2, column=4)

connected_label.grid(row=3, column=0)
connected_input.grid(row=3, column=1)

create_button.grid(row=4, column=1)

window.after(500, update)
window.mainloop()