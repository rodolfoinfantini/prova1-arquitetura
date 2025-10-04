from abc import ABC, abstractmethod


class EstrategiaDesconto(ABC):
    @abstractmethod
    def aplicar_desconto(self, valor: float) -> float:
        pass


class DescontoNormal(EstrategiaDesconto):
    def aplicar_desconto(self, valor: float) -> float:
        return valor


class Desconto10(EstrategiaDesconto):
    def aplicar_desconto(self, valor: float) -> float:
        return valor * 0.9


class Desconto20(EstrategiaDesconto):
    def aplicar_desconto(self, valor: float) -> float:
        return valor * 0.8


class Desconto5(EstrategiaDesconto):
    def aplicar_desconto(self, valor: float) -> float:
        return valor * 0.95
