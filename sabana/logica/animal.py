class Animal:
    def __init__(self, nombre, posicion, sexo):
        self.nombre = nombre
        self.posicion = posicion  # (x, y)
        self.sexo = sexo          # M o F
        self.pasos_dados = 0
        self.comidas = 0
        self.vivo = True

    def mover(self):
        # Por ahora no hace nada
        pass

    def comer(self):
        # Aumenta el contador de comidas
        self.comidas += 1

    def paso(self):
        # Suma un paso y verifica si muere
        self.pasos_dados += 1
        if self.pasos_dados >= self.max_pasos():
            self.vivo = False

    def max_pasos(self):
        # Este metodo sera diferente para cada animal
        return 100

