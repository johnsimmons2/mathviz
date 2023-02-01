import numpy as np

def sigmoid(x):
    return 1/(1 + np.exp(-x))

class Node:
    def __init__(self, sv = None):
        self.value = sv
        self.b = np.random.rand()
        self.W = []
        self.activation = sigmoid
        self.parents: list[Node] = []
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        child.addParent(self)
    
    def addParent(self, parent):
        self.parents.append(parent)
        self.W.append(np.random.rand())

    def evaluate(self):
        val = 0
        for i in range(len(self.parents)):
            pval = self.parents[i].value
            if pval is None:
                self.parents[i].evaluate()
                pval = self.parents[i].value
            val = val + pval * self.W[i]
        if len(self.parents) > 0:
            self.value = self.activation(val + self.b)

    def clean(self):
        for k in self.parents:
            if len(k.parents) > 0:
                k.value = None
                k.clean()

    def getOutput(self):
        self.clean()
        self.evaluate()
        return self.value

class Network:
    def __init__(self, x, y, l, h):
        self.nodes = []
        self.input = []
        self.output = []

        for i in range(x):
            inpNode = Node(0)
            self.nodes.append(inpNode)
            self.input.append(inpNode)

        pn = self.nodes
        for i in range(l):
            layer = []
            for j in range(h):
                hNode = Node()
                for k in pn:
                    k.addChild(hNode)
                self.nodes.append(hNode)
                layer.append(hNode)
            pn = layer

        for i in range(y):
            yN = Node()
            for k in pn:
                k.addChild(yN)
            self.nodes.append(yN)
            self.output.append(yN)

    def setInput(self, X):
        for i, x in enumerate(self.input):
            x.value = X[i]
        for i, x in enumerate(self.input):
            print(x.value)


    def propagate(self):
        out = []
        for k in self.output:
            out.append(k.getOutput())
        return out
