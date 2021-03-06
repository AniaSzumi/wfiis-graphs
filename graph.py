import random
from re import S
from tkinter import N
from tkinter.messagebox import RETRY
from edge import *
from functions import check_graphic_sequence
from node import *
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, nodes=[], edges=[]):
        self.nodes = [n for n in nodes]
        self.edges = [e for e in edges]

    def add_node(self, node):
        self.nodes.append(node)

    def delete_node(self, node_idx):
        del self.nodes[node_idx]

    def add_edge(self, start, end):
        if start == end or self.edge_exists(start, end):
            return False
        self.edges.append(Edge(start, end))
        return True

    def add_nodes(self, amount):
        for i in range(amount):
            self.add_node(Node(i))

    def add_neighbour(self, node_index, neighbour):
        if node_index == neighbour or neighbour in self.nodes[node_index].neighbours:
            return False
        self.nodes[node_index].neighbours.append(neighbour)
        return True

    def add_neighbours(self, node1, node2):
        res = self.add_neighbour(node1, node2)
        res2 = self.add_neighbour(node2, node1)
        return res and res2

    def find_edge(self, idx1, idx2):
        for i, edge in enumerate(self.edges):
            if (edge.start == idx1 and edge.end == idx2) or (edge.start == idx2 and edge.end == idx1):
                return edge, i
        return None, -1

    def edge_exists(self, index1, index2):
        _, index =  self.find_edge(index1, index2)
        return index >= 0

    def delete_edge(self, idx1, idx2):
        _, index = self.find_edge(idx1, idx2)
        if index >= 0:
            del self.edges[index]
            return True
        return False

    def delete_all(self):
        self.nodes = []
        self.edges = []

    ############################# PROJECT1 ################################

    ##### ex 1 #####
    def fill_from_adjacency_list(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        rows = len(lines)
        self.add_nodes(rows)
        for i in range(rows):
            line = lines[i].split(' ')
            for j in range(len(line)):
                self.add_neighbour(i, int(line[j])-1)
                self.add_edge(i, int(line[j])-1)

    def fill_from_adjacency_matrix(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        rows = len(lines)
        self.add_nodes(rows)
        for i in range(rows):
            line = lines[i].split(' ')
            for j in range(len(line)):
                if int(line[j]) == 1:
                    self.add_neighbour(i, j)
                    if j < i:
                        self.add_edge(i, j)

    def fill_from_incidence_matrix(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        line = lines[0].split(' ')
        cols = len(line)
        self.add_nodes(cols)
        for i in range(len(lines)):
            line = lines[i].split(' ')
            ones = 0
            for j in range(len(line)):
                if int(line[j]) == 1 and ones == 0:
                    start = j
                    ones += 1
                elif int(line[j]) == 1 and ones == 1:
                    end = j
                    ones += 1
            self.add_edge(start, end)
            self.add_neighbours(start, end)

    def print_adjacency_list(self):
        print('Lista s??siedztwa:')
        for node in self.nodes:
            node.print_neighbours_list()

    def print_adjacency_matrix(self):
        print('Macierz s??siedztwa:')
        for node in self.nodes:
            node.print_neighbours_vector(len(self.nodes))

    def print_incidence_matrix(self):
        print('Macierz incydencji:')
        for edge in self.edges:
            edge.print_nodes_vector(len(self.nodes))

    def print_all_representations(self):
        self.print_adjacency_list()
        self.print_adjacency_matrix()
        self.print_incidence_matrix()

    ##### ex 2 #####
    def create_nx_graph(self):
        G = nx.Graph()
        for node in self.nodes:
            G.add_node(node.number+1)
        for edge in self.edges:
            G.add_edge(edge.start+1, edge.end+1)
        return G

    def draw_nx_graph(self):
        G = self.create_nx_graph()
        nx.draw_circular(G, with_labels=True, font_weight='bold')
        plt.show()

    ##### ex 3 #####
    def fill_random_NL(self, n, l):
        if l > (n*(n-1))/2:
            print("Z??a ilo???? kraw??dzi")
            return False
        self.add_nodes(n)
        while len(self.edges) < l:
            index1 = random.randint(0,n-1)
            index2 = random.randint(0,n-1)
            self.add_edge(index1, index2)
            self.add_neighbours(index1, index2)
        return True

    def fill_random_NP(self, n, p):
        self.add_nodes(n)
        for i in self.nodes:
            for j in self.nodes:
                probability = random.random()
                if probability <= p:
                    self.add_edge(i.number, j.number)
                    self.add_neighbours(i.number, j.number)

    ############################# PROJECT2 ################################

    ##### ex 1 #####
    def fill_from_graphic_sequence(self, sequence):
        if not check_graphic_sequence(sequence):
            print("Ci??g nie jest graficzny")
            return False
        seq = [[idx, deg] for idx, deg in enumerate(sequence)]
        self.add_nodes(len(sequence))

        while True:
            seq.sort(reverse=True, key=itemgetter(1))
            if all(el[1] == 0 for el in seq):
                break
            for i in range(1, seq[0][1]+1):
                seq[i][1] -= 1
                self.add_edge(seq[0][0], seq[i][0])
                self.add_neighbours(seq[0][0], seq[i][0])
            seq[0][1] = 0

    ##### ex 2 #####
    def swap_edges(self, edge1, edge2):
        a = edge1.start
        b = edge1.end
        c = edge2.start
        d = edge2.end

        if a == d or b == c:
            return False

        if self.edge_exists(a,d) or self.edge_exists(b,c):
            return False

        edge1.end = d
        edge2.end = b
        self.nodes[a].delete_neighbour(b)
        self.nodes[b].delete_neighbour(a)
        self.nodes[c].delete_neighbour(d)
        self.nodes[d].delete_neighbour(c)

        self.add_neighbours(a,d)
        self.add_neighbours(c,b)
        return True


    def randomize_edges(self, n, seq):
        self.fill_from_graphic_sequence(seq)
        for _ in range(n):
            while True:
                idx1 = random.randint(0, len(self.edges)-1)
                idx2 = random.randint(0, len(self.edges)-1)
                if idx1 != idx2:
                    res = self.swap_edges(self.edges[idx1], self.edges[idx2])
                    if res:
                        break

    ##### ex 3 #####
    def components_R(self, nr, v, comp):
        for u in self.nodes[v].neighbours:
            if comp[u] == -1:
                comp[u] = nr
                self.components_R(nr, u, comp)

    def components(self):
        nr = 0
        comp = [-1 for _ in range(len(self.nodes))]
        for v in range(len(self.nodes)):
            if comp[v] == -1:
                nr += 1
                comp[v] = nr
                self.components_R(nr, v, comp)
        return comp

    def largest_consistent_component(self):
        comp = list(self.components())
        comp.sort()
        largest = -1
        max_count = 0
        prev = -1
        for c in comp:
            if c != prev:
                prev = c
                count = 0
            count += 1
            if count > max_count:
                max_count = count
                largest = c
        return max_count

    ##### ex 4 #####
    def generate_even_sequence(self, n):
        seq = []
        for _ in range(n):
            a = 1
            b = int(n * (n-1) / 4)
            value = random.randint(a, b) * 2

            seq.append(value)
        return seq

    def is_coherent(self):
        max_count = self.largest_consistent_component()
        return max_count == len(self.nodes)

    def fill_random_euler(self, n):
        seq = self.generate_even_sequence(n)
        self.fill_from_graphic_sequence(seq)
        while True:
            is_coherent = self.is_coherent()
            is_graphic = check_graphic_sequence(seq)
            if is_coherent and is_graphic:
                break
            seq = self.generate_even_sequence(n)
            self.fill_from_graphic_sequence(seq)


    def create_copy(self):
        copy = Graph()
        copy.nodes = [Node.create_copy(n) for n in self.nodes]
        copy.edges = [e for e in self.edges]
        return copy

    def is_bridge(self, start, end):
        self.delete_edge(start, end)
        res = not self.is_coherent()
        self.add_edge(start, end)
        return res

    def find_euler_cycle(self):
        copy = self.create_copy()
        euler_cycle = []
        self.print_adjacency_list()
        copy.euler_R(copy.nodes[0], euler_cycle)
        self.print_adjacency_list()
        return euler_cycle

    def euler_R(self, v, s):
        for u in v.neighbours:
            self.delete_edge(v.number, u)
            v.delete_neighbour(u)
            u_node = self.nodes[u]
            u_node.delete_neighbour(v.number)
            self.euler_R(u_node, s)
        s.append(v.number+1)

    ##### ex 5 #####
    def fill_k_regular(self, n, k):
        seq = [k for _ in range(n)]
        self.fill_from_graphic_sequence(seq)

    ##### ex 6 #####
    def find_hamilton_cycle(self):
        coherent = self.is_coherent()
        if not coherent:
            print("Graf nie jest sp??jny")
            return False
        visited = [False for _ in range(len(self.nodes))]
        stack = []
        self.hamilton_R(0, visited, stack)
        if len(stack) < len(self.nodes):
            print("Nie znaleziono cyklu Hamiltona")

    def hamilton_R(self, v, visited, stack):
        stack.append(v)
        if len(stack) < len(self.nodes):
            visited[v] = True
            for u in self.nodes[v].neighbours:
                if visited[u] == False:
                    cycle = self.hamilton_R(u, visited, stack)
                    if cycle:
                        return cycle
            visited[v] = False
            stack.pop()
        else:
            test = False
            for u in self.nodes[v].neighbours:
                if u == 0:
                    test = True
            cycle = stack
            if test == True:
                print("Cykl Hamiltona:")
                cycle.append(0)
            else:
                print("??cie??ka Hamiltona:")
            print([number+1 for number in stack])
            return cycle
        return None









