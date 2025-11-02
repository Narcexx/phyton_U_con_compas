from random import randint
from .elefante import Elefante
from .comida import Pasto, Carne, Insectos

class Sabana:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.animales = []
        self.comidas = []

    def agregar_animal(self, animal):
        self.animales.append(animal)

    def agregar_comida(self, comida):
        self.comidas.append(comida)

    def mover_animales(self):
        for animal in self.animales:
            if animal.vivo:
                x, y = animal.posicion
                nuevo_x = max(0, min(self.ancho - 1, x + randint(-1, 1)))
                nuevo_y = max(0, min(self.alto - 1, y + randint(-1, 1)))
                animal.posicion = (nuevo_x, nuevo_y)
                animal.paso()

    def mostrar_estado(self):
        for animal in self.animales:
            print(f"{animal.nombre}: posición {animal.posicion}, pasos {animal.pasos_dados}, vivo: {animal.vivo}")