# Example structure and probabilities for implemented Bayesian network
# Nodes are represented as dictionaries, where the key is the node name and the value is a list of parent nodes
# Probabilities are represented as dictionaries, where the key is the node name and the value is a dictionary of probabilities
# The inner dictionary has a key for True and False, and the value is a float
# If the node has parents, the inner dictionary has a key for True and False, and the value is a dictionary of parent values
# The innermost dictionary has a key for each combination of parent values saved as a tuple, and the value is a float

# The example is based on Judea Pearl's "Probabilistic Reasoning in Intelligent Systems" book

nodes = {
    'Burglary': [],
    'Earthquake': [],
    'Alarm': ['Burglary', 'Earthquake'],
    'JanCalls': ['Alarm'],
    'MagdaCalls': ['Alarm']
}

probabilities = {
    'Burglary': {
        True: 0.01,
        False: 0.99
    },
    'Earthquake': {
        True: 0.02,
        False: 0.98
    },
    'Alarm': {
        True: {
            (True, True): 0.95,
            (True, False): 0.94,
            (False, True): 0.29,
            (False, False): 0.001
        },
        False: {
            (True, True): 0.05,
            (True, False): 0.06,
            (False, True): 0.71,
            (False, False): 0.999
        }
    },
    'JanCalls': {
        True: {
            (True,): 0.90,
            (False,): 0.05
        },
        False: {
            (True,): 0.10,
            (False,): 0.95
        }
    },
    'MagdaCalls': {
        True: {
            (True,): 0.70,
            (False,): 0.01
        },
        False: {
            (True,): 0.30,
            (False,): 0.99
        }
    }
}