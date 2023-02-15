from abc import ABC, abstractmethod

class Algorithm(ABC):
    @abstractmethod
    def learn(self, data): ...
    
    @abstractmethod
    def predict(self, data): ...