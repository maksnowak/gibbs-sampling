# Note: code in this file has been extracted from the jupyter notebook

import numpy as np

# Node class used in the Bayesian network
class BayesianNode:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.children = []
        self.value = None
    
    def __str__(self):
        return self.name
    
    def add_parent(self, parent):
        self.parents.append(parent)
    
    def add_child(self, child):
        self.children.append(child)
    
    def set_value(self, value):
        self.value = value

# Bayesian network class
class BayesianNetwork:
    def __init__(self, nodes_struct, probabilities):
        self.nodes = []
        self.probabilities = probabilities
        self.build(nodes_struct)
    
    def build(self, nodes_struct):
        for node_name in nodes_struct:
            node = BayesianNode(node_name)
            self.nodes.append(node)
        
        for node_name in nodes_struct:
            node = self.get_node(node_name)
            for parent_name in nodes_struct[node_name]:
                parent = self.get_node(parent_name)
                node.add_parent(parent)
                parent.add_child(node)
    
    def get_node(self, node_name):
        for node in self.nodes:
            if node.name == node_name:
                return node
        return None
    
    def conditional_prob(self, node_name, value, parent_values=None):
        node = self.get_node(node_name)
        prob_table = self.probabilities[node.name]
        if len(node.parents) == 0:
            return prob_table[value]
        else:
            return prob_table[value][parent_values]
    
    def markov_blanket_prob(self, node_name, value):
        node = self.get_node(node_name)
        node.set_value(value)

        # P(node | parents)
        if len(node.parents) > 0:
            prob = self.conditional_prob(node_name, value, tuple([parent.value for parent in node.parents]))
        else:
            prob = self.conditional_prob(node_name, value)
        children = node.children
        # P(children | children_parents)
        for child in children:
            prob *= self.conditional_prob(child.name, child.value, tuple([child_parent.value for child_parent in child.parents]))
        return prob

# MCMC Gibbs sampling algorithm
class Gibbs:
    def __init__(self, network):
        self.network = network
        self.counts = {}
    
    def run(self, evidence, query, iterations):
        # Set initial values for observed variables, sample the rest
        for node in self.network.nodes:
            if node.name in evidence:
                node.set_value(evidence[node.name])
            else:
                node.set_value(np.random.choice([True, False]))
        # Set initial counts for query variable
        self.counts = {True: 0, False: 0}
        # Random walk
        for _ in range(iterations):
            # Select a non-evidence node
            not_evidence = [node for node in self.network.nodes if node.name not in evidence]
            node = np.random.choice(not_evidence)
            # Markov blanket
            blanket_prob_true = self.network.markov_blanket_prob(node.name, True)
            blanket_prob_false = self.network.markov_blanket_prob(node.name, False)
            prob_true = blanket_prob_true / (blanket_prob_true + blanket_prob_false)
            prob_false = blanket_prob_false / (blanket_prob_true + blanket_prob_false)
            node.set_value(np.random.choice([True, False], p=[prob_true, prob_false]))
            # Update counts
            query_node = self.network.get_node(query)
            self.counts[query_node.value] += 1
        # Normalize counts to get probabilities
        return {True: self.counts[True] / iterations, False: self.counts[False] / iterations}