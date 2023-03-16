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
            
    def initWeights(self, wheight_amount: int):
        if type == 'input':
            return
        
        for neuron in self.neurons[:-1]:
            neuron.wheights = [1.0 for _ in range(wheight_amount + 1)]

class NeuralNetwork(Default):
    def __init__(self, input_amount: int, hidden_amounts: list[int], output_amount: int):
        self.input_amount = input_amount
        self.output_amount = output_amount

        self.input_layer = Layer(input_amount, 'input')
        
        self.hidden_layers: list[Layer] = []
        
        for i, hidden_amount in enumerate(hidden_amounts):
            prev_layer_amount = input_amount if i == 0 else hidden_amounts[i - 1]
            
            hidden_layer = Layer(hidden_amount, 'hidden')
            hidden_layer.initWeights(prev_layer_amount)
            
            self.hidden_layers.append(hidden_layer)
        
        self.output_layer = Layer(output_amount, 'output')
        self.output_layer.initWeights(hidden_amounts[i - 1])

        print(self)
    
    def relu(self, x: float):
        return max(0, x)


NeuralNetwork(2, [3, 3], 2)
