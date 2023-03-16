from enum import Enum
from abc import ABC

BIAS = 1

neuron = {
    "peso": [1.0],
    "erro": 0.0,
    "saida": 1.0
}

camada = {
    'neurons': [neuron, neuron],
}

rede_neural = {
    'camada_entrada': camada,
    'camada_oculta': [camada, camada],
    'camada_saida': camada,
}

# IGNORE THIS ABOVE


class Default(ABC):
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict__})'

    def __str__(self) -> str:
        return self.__repr__()


class Neuron(Default):
    def __init__(self, wheights: list[float] | None = None):
        self.wheights = wheights
        self.error = 0.0
        self.output = 1.0


class Layer(Default):
    def __init__(self, neurons_amount: int, type: str):
        self.neurons: list[Neuron] = []

        bias = BIAS if type != 'output' else 0

        for _ in range(neurons_amount + bias):
            self.neurons.append(Neuron())

    def initWeights(self, prev_amount: int):
        if type == 'input':
            return

        for neuron in self.neurons[:-1]:
            neuron.wheights = [1.0 for _ in range(prev_amount + 1)]


class NeuralNetwork(Default):
    def __init__(self, input_amount: int, hidden_amounts: list[int], output_amount: int):
        self.input_amount = input_amount
        self.output_amount = output_amount
        self.hidden_amounts = hidden_amounts

        self.input_layer, self.hidden_layers, self.output_layer = self.initLayers()
        
        self.draw()

    def initLayers(self):
        input_layer = Layer(self.input_amount, 'input')

        hidden_layers: list[Layer] = []

        for i, hidden_amount in enumerate(self.hidden_amounts):
            prev_layer_amount = self.input_amount if i == 0 else self.hidden_amounts[i - 1]

            hidden_layer = Layer(hidden_amount, 'hidden')
            hidden_layer.initWeights(prev_layer_amount)

            hidden_layers.append(hidden_layer)

        output_layer = Layer(self.output_amount, 'output')
        output_layer.initWeights(self.hidden_amounts[i - 1])

        return [input_layer, hidden_layers, output_layer]

    def draw(self):
        from tkinter import Tk, Canvas
        
        root = Tk()
        
        canvas = Canvas(root, background='red', width=800, height=600)
        canvas.pack()
        
        canvas.create_oval(0, 0, 60, 60, width=3)
        canvas.create_line(0, 0, 100, 100, width=3)
        
        root.mainloop()

    def relu(self, x: float):
        return max(0, x)


NeuralNetwork(2, [3, 3], 2)
