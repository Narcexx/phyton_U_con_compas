from logica.elefante import Elefante

elefante1 = Elefante("Dumbo", (0, 0), "M")

for _ in range(5):
    elefante1.comer()
    elefante1.paso()

print(f"Comidas: {elefante1.comidas}")
print(f"Pasos dados: {elefante1.pasos_dados}")
print(f"¿Sigue vivo?: {elefante1.vivo}")