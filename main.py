import re


class PriceCounter:
    """
    Class calculates the prices from a, b cards
    by given network in *.dot
j
    nodes_length - key (nodes) value (length). Example: {'AF': 50}
    card_a_cost, card_b_cost -  future price of two cards
    cabinet - cabinet
    pots - the list of all pots
    stop - Flag to stop recursion in graph

    """

    nodes_length = {}
    card_a_cost = 0
    card_b_cost = 0
    cabinet = ''
    pots = []
    stop = False

    price_list_a = {
        'Cabinet': 1000,
        'verge': 50,
        'road': 100,
        'Chamber': 200,
        'Pot': 100
    }

    price_list_b = {
        'Cabinet': 1200,
        'verge': 40,
        'road': 80,
        'Chamber': 200,
        'Pot': 20
    }

    def _parse_file(self):
        """
        Parsing from file *.dot
        """
        with open(file='problem.dot', mode='r') as file:
            for line in file.readlines()[1:-1]:
                string_items = line.split()

                if string_items[1] != '--':
                    node_type = re.search(pattern=r'type=(.*)];', string=string_items[1]).group(1)
                    if node_type == 'Cabinet':
                        self.cabinet = string_items[0]
                    elif node_type == 'Pot':
                        self.pots.append(string_items[0])

                    self.card_a_cost += self.price_list_a.get(node_type)
                    self.card_b_cost += self.price_list_b.get(node_type)
                else:
                    node1 = string_items[0]
                    node2 = string_items[2]
                    length = re.search(pattern=r'length=(.*),', string=string_items[3]).group(1)
                    material = re.search(pattern=r'material=(.*)];', string=string_items[4]).group(1)

                    self.card_a_cost += int(length) * self.price_list_a.get(material)

                    self.nodes_length[node1+node2] = int(length)

    def _create_graph(self):
        """
        Creates graph by given network from a file
        key - vertex, values - nodes
        Example - {'A': [F]}

        :return: graph in dict format
        """
        graph = {}
        for nodes_pair in self.nodes_length.keys():
            for vertex in nodes_pair:
                if vertex not in graph:
                    vertex_nodes = [nodes.replace(vertex, '') for nodes in self.nodes_length if vertex in nodes]
                    graph[vertex] = vertex_nodes
        return graph

    def _find_node_length(self, node1, node2):
        """
        From self.nodes_length gets length
        Example: {'AF': 50} - the length between A and F nodes equals to 50

        :param node1: A
        :param node2: F
        :return: int length 50
        """
        for nodes, length in self.nodes_length.items():
            if node1 and node2 in nodes:
                return length

    def _find_path_cost(self, start, end, previous_vertex=None):
        """
        Using the method for card B, because we need to calculate the
        distance between Cabinet and Pot


        :param start: at first the Cabinet, after children of Cabinet
        :param end: the final pot
        :param previous_vertex: the previous_vertex of current node
        """
        if not self.stop:
            graph = self._create_graph()

            nodes = graph[start]
            vertex = start

            for node in nodes:
                length = self._find_node_length(vertex, node)
                self.card_b_cost += length * self.price_list_b['Pot']

                if node == end:
                    self.stop = True

                """means deadline"""
                if previous_vertex == node:
                    if len(nodes) == 1:
                        length = self._find_node_length(previous_vertex, node)
                        self.card_b_cost -= length * self.price_list_b['Pot']
                    self.card_b_cost -= length * self.price_list_b['Pot']
                    continue

                self._find_path_cost(start=node, end=end, previous_vertex=vertex)

    def cost_calculate(self):
        """
        Calculates the B card`s cost

        :return: cost A and B cards
        """
        self._parse_file()
        self._create_graph()
        for pot in self.pots:
            self._find_path_cost(start=self.cabinet, end=pot)
            self.stop = False
        return self.card_a_cost, self.card_b_cost


counter = PriceCounter()
card_a_cost, card_b_cost = counter.cost_calculate()

print(f'The cost of card A={card_a_cost} and card B={card_b_cost}')

