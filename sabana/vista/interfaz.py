import pygame
import random
import os

class Interfaz:
    def __init__(self, sabana):
        pygame.init()
        self.sabana = sabana
        self.tamaño_celda = 32
        self.ancho_pantalla = sabana.ancho * self.tamaño_celda
        self.alto_pantalla = sabana.alto * self.tamaño_celda
        self.pantalla = pygame.display.set_mode((self.ancho_pantalla, self.alto_pantalla))
        pygame.display.set_caption("Sabana")
        self.reloj = pygame.time.Clock()

        carpeta_base = os.path.dirname(__file__)  # carpeta donde está interfaz.py
        carpeta_imagenes = os.path.join(carpeta_base, "..", "imagenes")

        self.fondo = pygame.image.load(os.path.join(carpeta_imagenes, "sabana.png"))
        self.fondo = pygame.transform.scale(self.fondo, (self.ancho_pantalla, self.alto_pantalla))

        self.imagenes_animales = {
            "Elefante_M": pygame.image.load(os.path.join(carpeta_imagenes, "elefante_macho.png")),
            "Elefante_F": pygame.image.load(os.path.join(carpeta_imagenes, "elefante_hembra.png")),
            "Leon_M": pygame.image.load(os.path.join(carpeta_imagenes, "leon_macho.png")),
            "Leon_F": pygame.image.load(os.path.join(carpeta_imagenes, "leon_hembra.png")),
            "Chimpance_M": pygame.image.load(os.path.join(carpeta_imagenes, "chimpance_macho.png")),
            "Chimpance_F": pygame.image.load(os.path.join(carpeta_imagenes, "chimpance_hembra.png")),
        }

        self.imagenes_comidas = {
            "pasto": pygame.image.load(os.path.join(carpeta_imagenes, "pasto.png")),
            "carne": pygame.image.load(os.path.join(carpeta_imagenes, "carne.png")),
            "insectos": pygame.image.load(os.path.join(carpeta_imagenes, "insectos.png")),
        }
        self.contador_movimiento = 0

        # redimensiona todas las imagenes
        for clave in self.imagenes_animales:
            self.imagenes_animales[clave] = pygame.transform.scale(self.imagenes_animales[clave], (40, 40))
        for clave in self.imagenes_comidas:
            self.imagenes_comidas[clave] = pygame.transform.scale(self.imagenes_comidas[clave], (25, 25))

    # dibuja todo en pantalla
    def dibujar(self):
        self.pantalla.blit(self.fondo, (0, 0))

        # dibujar comidas
        for comida in self.sabana.comidas:
            x, y = comida.posicion
            img = self.imagenes_comidas[comida.tipo]
            self.pantalla.blit(img, (x * self.tamaño_celda, y * self.tamaño_celda))

        # dibujar animales
        for animal in self.sabana.animales:
            if not animal.vivo:
                continue
            x, y = animal.posicion
            clave = f"{animal.__class__.__name__}_{animal.sexo}"
            img = self.imagenes_animales.get(clave)
            if img:
                self.pantalla.blit(img, (x * self.tamaño_celda, y * self.tamaño_celda))

        pygame.display.flip()

    def ejecutar(self):
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            # controlar velocidad de movimiento
            self.contador_movimiento += 1
            if self.contador_movimiento >= 30:  # mover cada 30 frames (0.5 seg si hay 60 fps)
                self.sabana.mover_hacia_comida()
                self.sabana.reproducir()
                self.contador_movimiento = 0

            # redibujar siempre
            self.dibujar()
            self.reloj.tick(60)

        pygame.quit()