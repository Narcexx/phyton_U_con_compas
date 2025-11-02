from logica.elefante import Elefante
from logica.sabana import Sabana
from logica.comida import Pasto

# Crear sabana
sabana = Sabana(10, 10)

# Crear animales
elefante1 = Elefante("Dumbo", (2, 3), "M")
sabana.agregar_animal(elefante1)

# Agregar comida
sabana.agregar_comida(Pasto((5, 5)))

# Simular movimientos
for _ in range(5):
    sabana.mover_animales()
    sabana.mostrar_estado()
    print("-----")