from logica.sabana import Sabana
from logica.elefante import Elefante
from logica.leon import Leon
from logica.chimpance import Chimpance

sabana = Sabana(10, 10)

# Animales
elefante1 = Elefante("Dumbo", (1, 1), "M")
leon1 = Leon("Simba", (3, 3), "M")
chimpance1 = Chimpance("Coco", (2, 2), "F")

sabana.agregar_animal(elefante1)
sabana.agregar_animal(leon1)
sabana.agregar_animal(chimpance1)

for _ in range(10):
    sabana.mover_animales()
    sabana.reproducir()   # <--- nueva línea
    sabana.mostrar_estado()
    print("----")