class Animal:
    def __init__(self, nombre, posicion, sexo):
        self.nombre = nombre
        self.posicion = posicion  # (x, y)
        self.sexo = sexo          # M o F
        self.pasos_dados = 0
        self.comidas = 0
        self.vivo = True

    def mover(self):
        pass

    def comer(self):
        self.comidas += 1

    def paso(self):
        # Cada vez que da un paso, aumenta el contador y revisa si muere
        self.pasos_dados += 1
        if self.pasos_dados >= self.max_pasos():
            self.vivo = False
            print(f"{self.nombre} ha muerto por cansancio")

    def max_pasos(self):
        # Este metodo sera distinto para cada animal
        return 100


