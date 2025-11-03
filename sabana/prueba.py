from logica.sabana import Sabana
from logica.elefante import Elefante
from logica.leon import Leon
from logica.chimpance import Chimpance
from vista.interfaz import Interfaz

# Crear sabana 20x15
sabana = Sabana(20, 15)

# Crear animales (dos de cada especie)
sabana.agregar_animal(Elefante("Dumbo", (5, 5), "M"))
sabana.agregar_animal(Elefante("Eli", (8, 4), "F"))
sabana.agregar_animal(Leon("Simba", (10, 8), "M"))
sabana.agregar_animal(Leon("Nala", (12, 10), "F"))
sabana.agregar_animal(Chimpance("Coco", (3, 6), "M"))
sabana.agregar_animal(Chimpance("Luna", (4, 9), "F"))

# Generar comidas
sabana.generar_comida(10)

# Ejecutar interfaz
interfaz = Interfaz(sabana)
interfaz.ejecutar()
