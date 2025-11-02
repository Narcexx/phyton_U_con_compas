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
            else:
                # si murio lo quitamos de la lista
                self.animales.remove(animal)
                print(f"{animal.nombre} fue removido de la sabana")

    def mostrar_estado(self):
        for animal in self.animales:
            print(f"{animal.nombre}: posicion {animal.posicion}, pasos {animal.pasos_dados}, vivo: {animal.vivo}")

    def reproducir(self):
        nuevos_animales = []
        for i in range(len(self.animales)):
            for j in range(i + 1, len(self.animales)):
                a1 = self.animales[i]
                a2 = self.animales[j]

                if type(a1) == type(a2) and a1.sexo != a2.sexo and a1.vivo and a2.vivo:
                    dist = abs(a1.posicion[0] - a2.posicion[0]) + abs(a1.posicion[1] - a2.posicion[1])

                    if dist <= 2:
                        if a1.comidas >= 3 and a2.comidas >= 3:
                            nombre_hijo = f"Bebe_{a1.nombre}_{a2.nombre}"
                            nueva_pos = ((a1.posicion[0] + a2.posicion[0]) // 2,
                                        (a1.posicion[1] + a2.posicion[1]) // 2)
                            nuevo_sexo = "M" if (i + j) % 2 == 0 else "F"
                            bebe = type(a1)(nombre_hijo, nueva_pos, nuevo_sexo)
                            nuevos_animales.append(bebe)
                            print(f"{a1.nombre} y {a2.nombre} tuvieron un bebé llamado {nombre_hijo}.")
                        else:
                            print(f"{a1.nombre} y {a2.nombre} no pueden reproducirse (no comieron 3 veces)")

        self.animales.extend(nuevos_animales)

    def generar_comida(self, cantidad):
        # Genera comida aleatoria en distintas posiciones
        tipos = ["pasto", "carne", "insectos"]
        for _ in range(cantidad):
            tipo = tipos[randint(0, 2)]
            x = randint(0, self.ancho - 1)
            y = randint(0, self.alto - 1)
            if tipo == "pasto":
                self.comidas.append(Pasto((x, y)))
            elif tipo == "carne":
                self.comidas.append(Carne((x, y)))
            else:
                self.comidas.append(Insectos((x, y)))

