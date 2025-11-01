class Comida:
    def __init__(self, tipo, posicion):
        self.tipo = tipo  # pasto, carne, insectos
        self.posicion = posicion

class Pasto(Comida):
    def __init__(self, posicion):
        super().__init__("pasto", posicion)

class Carne(Comida):
    def __init__(self, posicion):
        super().__init__("carne", posicion)

class Insectos(Comida):
    def __init__(self, posicion):
        super().__init__("insectos", posicion)
