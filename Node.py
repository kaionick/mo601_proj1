# Node class
#   It models a circuit node for simulation porpuse.
#       Attr:
#           * Name: string value (A-Z)
#           * Inputs: list of inputs (one or two strings following the name)
#           * Value: current node value
#           * Value history: history of the node value (help in convergence).

class Node:
    def __init__(self, name, inputs, op):
        self.name = name;
        self.inputs = inputs;
        self.op = op;
        self.value = '0';
        self.value_hist = 'x';
