import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt

def create_graph():
    num_nodes = int(num_nodes_input.get())
    num_edges = int(num_edges_input.get())
    graph_type = graph_type_input.get()
    connected = int(connected_input.get())

    if graph_type == "Полный":
        G = nx.complete_graph(num_nodes)
    elif graph_type == "Сетка":
        G = nx.grid_2d_graph(num_nodes, num_nodes)
    elif graph_type == "Дерево":
        G = nx.random_tree(num_nodes)
    else:
        G = nx.Graph()
        G.add_nodes_from(range(1, num_nodes + 1))
        for i in range(1, num_nodes - connected + 1):
            for j in range(i + 1, num_nodes - connected + 2):
                if num_edges:
                    G.add_edge(i, j)
                    num_edges -= 1
                else:
                    break

    if graph_is_directed:
        G = G.to_directed()

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=with_labels)
    plt.show()

def error_check(obj, label, row, column, withzero=True):
    txt = obj.get()
    error = False
    if txt.isdigit():
        if withzero:
            if int(txt) >= 0:
                error = True
        else:
            if int(txt) > 0:
                error = True
    if not error:
        label.grid(row=row, column=column + 1)
        create_button.grid_forget()
        impossible_to_draw.grid(row=6, column=1)
        return error
    label.grid_forget()
    return error

def change_text(entry, text, blocked=False):
    unblock(entry)
    entry.delete(0, tk.END)
    entry.insert(0, text)
    if blocked:
        block(entry)


def possible_to_draw():
    impossible = False
    edges = int(num_edges_input.get())
    nodes = int(num_nodes_input.get())
    connects = int(connected_input.get())
    graph_type = graph_type_input.get()
    if graph_type == "Случайный":
        difference = nodes - connects + 1
        if difference * (difference - 1) // 2 < edges:
            impossible = True
        elif nodes - connects > edges:
            impossible = True
        elif connects > nodes:
            impossible = True

    if impossible:
        create_button.grid_forget()
        impossible_to_draw.grid(row=6, column=1)
    else:
        impossible_to_draw.grid_forget()
        create_button.grid(row=6, column=1)
def block(obj):
    obj.configure(state="disabled")

def unblock(obj):
    obj.configure(state="normal")

def select_complete():
    change_text(graph_type_input, "Полный", True)
    n = num_nodes_input.get()
    if n.isdigit():
        n = int(n)
        s = str(n * (n - 1) // 2)
    else:
        s = "0"

    change_text(num_edges_input, s, True)
    change_text(connected_input, "1", True)

def select_random():
    change_text(graph_type_input, "Случайный", True)

def select_grid():
    num_nodes = int(num_nodes_input.get())
    change_text(graph_type_input, "Сетка", True)
    change_text(num_edges_input, str(2 * num_nodes * (num_nodes - 1)), True)
    change_text(connected_input, "1", True)


def select_tree():
    change_text(graph_type_input, "Дерево", True)
    change_text(num_edges_input, str(int(num_nodes_input.get()) - 1), True)
    change_text(connected_input, "1", True)

def select_with_labels():
    global with_labels
    change_text(graph_with_labels_input, "Да", True)
    with_labels = True

def select_without_labels():
    global with_labels
    change_text(graph_with_labels_input, "Нет", True)
    with_labels = False

def select_directed():
    global graph_is_directed
    change_text(is_directed_input, "Да", True)
    graph_is_directed = True

def select_not_directed():
    global graph_is_directed
    change_text(is_directed_input, "Нет", True)
    graph_is_directed = False

def update():
    if error_check(num_nodes_input, num_nodes_error, 0, 1, False) and error_check(num_edges_input, num_edges_error, 1, 1) and error_check(connected_input, connected_input_error, 3, 1, False):
        graph_type = graph_type_input.get()
        if graph_type == "Полный":
            select_complete()
        elif graph_type == "Дерево":
            select_tree()
        elif graph_type == "Сетка":
            select_grid()
        else:
            unblock(num_edges_input)
            unblock(connected_input)
        possible_to_draw()

    window.after(500, update)

with_labels = False
graph_is_directed = False

# Создать окно
window = tk.Tk()
window.title("Визуализация графа")

# Создать элементы меню
num_nodes_label = tk.Label(window, text="Количество вершин:")
num_nodes_input = tk.Entry(window)
num_nodes_input.insert(0, "10")
num_nodes_error = tk.Label(window, text="Введите натуральное число", fg="red")

num_edges_label = tk.Label(window, text="Количество ребер:")
num_edges_input = tk.Entry(window)
num_edges_input.insert(0, "20")
num_edges_error = tk.Label(window, text="Введите целое неотрицательное число", fg="red")

graph_type_label = tk.Label(window, text="Тип графа:")
graph_type_input = tk.Entry(window)
graph_type_button_complete = tk.Button(window, text="Полный", command=select_complete)
graph_type_button_random = tk.Button(window, text="Случайный", command=select_random)
graph_type_button_grid = tk.Button(window, text="Сетка", command=select_grid)
graph_type_button_tree = tk.Button(window, text="Дерево", command=select_tree)
change_text(graph_type_input, "Случайный", True)

graph_with_labels_label = tk.Label(window, text="Вершины пронумерованы:")
graph_with_labels_input = tk.Entry(window)
graph_with_labels_button = tk.Button(window, text="Да", command=select_with_labels)
graph_without_labels_button = tk.Button(window, text="Нет", command=select_without_labels)
change_text(graph_with_labels_input, "Нет", True)

connected_label = tk.Label(window, text="Компонент связности:")
connected_input = tk.Entry(window)
connected_input.insert(0, "1")
connected_input_error = tk.Label(window, text="Введите натуральное число", fg="red")

is_directed_label = tk.Label(window, text="Граф ориентирован:")
is_directed_input = tk.Entry(window)
is_directed_button = tk.Button(window, text="Да", command=select_directed)
not_directed_button = tk.Button(window, text="Нет", command=select_not_directed)
change_text(is_directed_input, "Нет", True)

create_button = tk.Button(window, text="Создать граф", command=create_graph)
impossible_to_draw = tk.Label(window, text="Невозможно нарисовать данный граф", fg="red")

# Разместить элементы меню на окне
num_nodes_label.grid(row=0, column=0)
num_nodes_input.grid(row=0, column=1)

num_edges_label.grid(row=1, column=0)
num_edges_input.grid(row=1, column=1)

graph_type_label.grid(row=2, column=0)
graph_type_input.grid(row=2, column=1)

graph_type_button_complete.grid(row=2, column=2)
graph_type_button_random.grid(row=2, column=3)
graph_type_button_grid.grid(row=2, column=4)
graph_type_button_tree.grid(row=2, column=5)

connected_label.grid(row=3, column=0)
connected_input.grid(row=3, column=1)

graph_with_labels_label.grid(row=4, column=0)
graph_with_labels_input.grid(row=4, column=1)
graph_with_labels_button.grid(row=4, column=2)
graph_without_labels_button.grid(row=4, column=3)

is_directed_label.grid(row=5, column=0)
is_directed_input.grid(row=5, column=1)
is_directed_button.grid(row=5, column=2)
not_directed_button.grid(row=5, column=3)

create_button.grid(row=6, column=1)


window.after(500, update)
window.mainloop()