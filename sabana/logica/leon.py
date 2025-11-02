from .animal import Animal

class Leon(Animal):
    def __init__(self, nombre, posicion, sexo):
        super().__init__(nombre, posicion, sexo)

    def max_pasos(self):
        return 75

    def comer(self):
        print(f"{self.nombre} comió carne.")
        super().comer()
