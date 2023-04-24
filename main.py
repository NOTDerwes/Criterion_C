import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt


class Text:
    def __init__(self, list_text, row, buttons=False, num_buttons=0, button_commands=[], error_is_possible=False, entry_is_blocked=False):
        self.label = tk.Label(window, text=list_text[0])
        self.entry = tk.Entry(window)
        change_text(self.entry, list_text[1], entry_is_blocked)
        if error_is_possible:
            self.error_text = tk.Label(window, text=list_text[-1], fg="red")
        if buttons:
            self.buttons = []
            for i in range(num_buttons):
                button = tk.Button(window, text=list_text[2 + i], command=button_commands[i])
                button.grid(row=row, column=i+2)
                self.buttons.append(button)
        self.label.grid(row=row, column=0)
        self.entry.grid(row=row, column=1)


def create_graph():
    num_nodes = int(nodes.entry.get())
    num_edges = int(edges.entry.get())
    type = graph_type.entry.get()
    connected = int(connection_components.entry.get())

    if type == "Полный":
        G = nx.complete_graph(num_nodes)
    elif type == "Сетка":
        G = nx.grid_2d_graph(num_nodes, num_nodes)
    elif type == "Дерево":
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
    nx.draw(G, pos, with_labels=labels)
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
    num_edges = int(edges.entry.get())
    num_nodes = int(nodes.entry.get())
    connects = int(connection_components.entry.get())
    type = graph_type.entry.get()
    if type == "Случайный":
        difference = num_nodes - connects + 1
        if difference * (difference - 1) // 2 < num_edges:
            impossible = True
        elif num_nodes - connects > num_edges:
            impossible = True
        elif connects > num_nodes:
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
    change_text(graph_type.entry, "Полный", True)
    n = nodes.entry.get()
    if n.isdigit():
        n = int(n)
        s = str(n * (n - 1) // 2)
    else:
        s = "0"

    change_text(edges.entry, s, True)
    change_text(connection_components.entry, "1", True)


def select_random():
    change_text(graph_type.entry, "Случайный", True)


def select_grid():
    num_nodes = int(nodes.entry.get())
    change_text(graph_type.entry, "Сетка", True)
    change_text(edges.entry, str(2 * num_nodes * (num_nodes - 1)), True)
    change_text(connection_components.entry, "1", True)


def select_tree():
    change_text(graph_type.entry, "Дерево", True)
    change_text(edges.entry, str(int(nodes.entry.get()) - 1), True)
    change_text(connection_components.entry, "1", True)


def select_with_labels():
    global labels
    change_text(graph_with_labels.entry, "Да", True)
    labels = True


def select_without_labels():
    global labels
    change_text(graph_with_labels.entry, "Нет", True)
    labels = False


def select_directed():
    global graph_is_directed
    change_text(directed_graph.entry, "Да", True)
    graph_is_directed = True


def select_not_directed():
    global graph_is_directed
    change_text(directed_graph.entry, "Нет", True)
    graph_is_directed = False


def update():
    if error_check(nodes.entry, nodes.error_text, 0, 1, False) and error_check(edges.entry, edges.error_text, 1, 1) and error_check(connection_components.entry, connection_components.error_text, 3, 1, False):
        type = graph_type.entry.get()
        if type == "Полный":
            select_complete()
        elif type == "Дерево":
            select_tree()
        elif type == "Сетка":
            select_grid()
        else:
            unblock(edges.entry)
            unblock(connection_components.entry)
        possible_to_draw()

    window.after(500, update)

labels = False
graph_is_directed = False

# Создать окно
window = tk.Tk()
window.title("Визуализация графа")

nodes = Text(["Количество вершин:", "10", "Введите натуральное число"], 0, error_is_possible=True)

edges = Text(["Количество ребер:", "20", "Введите целое неотрицательное число"], 1, error_is_possible=True)

graph_type = Text(["Тип графа:", "Случайный", "Случайный", "Полный", "Сетка", "Дерево"], 2, True, 4, [select_random, select_complete, select_grid, select_tree], False, True)

connection_components = Text(["Компонент связности:", "1", "Введите натуральное число"], 3, error_is_possible=True)

graph_with_labels = Text(["Вершины пронумерованы:", "Нет", "Да", "Нет"], 4, True, 2, [select_with_labels, select_without_labels], entry_is_blocked=True)

directed_graph = Text(["Граф ориентирован:", "Нет", "Да", "Нет"], 5, True, 2, [select_directed, select_not_directed], entry_is_blocked=True)

create_button = tk.Button(window, text="Создать граф", command=create_graph)
impossible_to_draw = tk.Label(window, text="Невозможно нарисовать данный граф", fg="red")
create_button.grid(row=6, column=1)


window.after(500, update)
window.mainloop()
