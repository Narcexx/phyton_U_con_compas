from .animal import Animal

class Chimpance(Animal):
    def __init__(self, nombre, posicion, sexo):
        super().__init__(nombre, posicion, sexo)

    def max_pasos(self):
        return 125
    
    def comer(self):
        print(f"{self.nombre} comió insectos o pasto.")
        super().comer()
