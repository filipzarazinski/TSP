import matplotlib.pyplot as plt
import networkx as nx

# Stworzenie grafu za pomocą NetworkX
G = nx.Graph()
with open('5_19.txt', 'r') as file:
    file_contents = file.read()

    distance_matrix = []
    for line in file_contents.strip().split('\n'):
        row = [int(x) for x in line.split()]
        distance_matrix.append(row)
        
# Dodanie wierzchołków i krawędzi do grafu
for i, row in enumerate(distance_matrix):
    for j, weight in enumerate(row):
        if i != j:  # Zapobiegamy dodaniu pętli (połączeń wierzchołka ze sobą)
            G.add_edge(i, j, weight=weight)

# Rysowanie grafu
pos = nx.spring_layout(G)  # Wybór układu grafu (spring layout daje zazwyczaj czytelne wyniki)
labels = nx.get_edge_attributes(G, 'weight')  # Pobranie etykiet krawędzi (wag)

nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='black', linewidths=1, font_size=15)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)  # Dodanie etykiet krawędzi

# Wyświetlenie grafu
plt.show()