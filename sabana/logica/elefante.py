from .animal import Animal

class Elefante(Animal):
    def __init__(self, nombre, posicion, sexo):
        super().__init__(nombre, posicion, sexo)

    def max_pasos(self):
        return 150  # El elefante muere tras 150 pasos

    def comer(self):
        # El elefante come pasto
        print(f"{self.nombre} comió pasto.")
        super().comer()
