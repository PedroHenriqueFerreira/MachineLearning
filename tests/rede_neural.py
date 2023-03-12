neuronio = {
    "peso": [1.0],
    "erro": 0.0,
    "saida": 1.0
}

camada = {
    'neuronios': [neuronio, neuronio],
}

rede_neural = {
    'camada_entrada': camada,
    'camada_oculta': [camada, camada],
    'camada_saida': camada,
}

# IGNORE THIS ABOVE

class NeuralNetwork:
    def relu(self, x: float):
        return max(0, x)
    
    