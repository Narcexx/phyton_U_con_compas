from logica.sabana import Sabana
from logica.elefante import Elefante
from logica.leon import Leon
from logica.chimpance import Chimpance
from vista.consola import mostrar_mapa

sabana = Sabana(10, 10)
sabana.agregar_animal(Elefante("Dumbo", (1, 1), "M"))
sabana.agregar_animal(Leon("Simba", (5, 5), "F"))
sabana.agregar_animal(Chimpance("Coco", (8, 2), "M"))
sabana.generar_comida(10)

for _ in range(10):
    mostrar_mapa(sabana)
    sabana.mover_hacia_comida()
    print("---")