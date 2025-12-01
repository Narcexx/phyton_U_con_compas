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
        pygame.display.set_caption("Simulador de Ecosistema")
        self.reloj = pygame.time.Clock()

        # Cargar imagenes
        carpeta_base = os.path.dirname(__file__)
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
        
        # Redimensionar imagenes
        for clave in self.imagenes_animales:
            self.imagenes_animales[clave] = pygame.transform.scale(self.imagenes_animales[clave], (40, 40))
        for clave in self.imagenes_comidas:
            self.imagenes_comidas[clave] = pygame.transform.scale(self.imagenes_comidas[clave], (25, 25))

        self.contador_movimiento = 0

        # --- FUENTES Y ESTADOS ---
        pygame.font.init()
        self.fuente = pygame.font.SysFont("Arial", 18)
        self.fuente_titulo = pygame.font.SysFont("Arial", 24, bold=True)
        self.fuente_grande = pygame.font.SysFont("Arial", 40, bold=True)
        
        self.modo = "MENU_PRINCIPAL" 
        self.mensaje_estado = ""
        self.tiempo_mensaje = 0
        
        # Cache para guardar la info de los slots y no leer el disco 60 veces por segundo
        self.info_slots = [] 

    def actualizar_info_slots(self):
        # Le pide a la logica la lista de partidas guardadas
        if hasattr(self.sabana, "obtener_info_partidas"):
            self.info_slots = self.sabana.obtener_info_partidas()
        else:
            self.info_slots = []

    def obtener_texto_slot(self, nombre_slot_buscado, etiqueta_base):
        # Busca si existe informacion para ese slot
        for partida in self.info_slots:
            if partida["slot"] == nombre_slot_buscado:
                info = partida["info"]
                # Crea un texto bonito: "1. Slot 1 [Ciclo 50 - 10 Animales]"
                return f"{etiqueta_base} [Ciclo {info.get('ciclos', '?')} - {info.get('fecha', '')}]"
        
        # Si no existe, muestra vacio
        return f"{etiqueta_base} (Vacío)"

    def dibujar_ui(self):
        # 1. Contador de Ciclos (Esquina Superior Izquierda)
        if self.modo == "JUGANDO" or self.modo in ["MENU_GUARDAR", "MENU_CARGAR"]:
            texto_ciclo = self.fuente_titulo.render(f"Ciclo: {self.sabana.ciclos}", True, (255, 255, 255))
            # Dibujamos un fondo negro chiquito detras para que se lea bien
            bg_rect = texto_ciclo.get_rect(topleft=(10, 10))
            pygame.draw.rect(self.pantalla, (0, 0, 0), bg_rect)
            self.pantalla.blit(texto_ciclo, (10, 10))

        # 2. Mensajes temporales (Ej: "Guardado Exitoso")
        if self.mensaje_estado:
            texto = self.fuente.render(self.mensaje_estado, True, (255, 255, 0))
            self.pantalla.blit(texto, (10, 40)) # Debajo del ciclo
            self.tiempo_mensaje -= 1
            if self.tiempo_mensaje <= 0:
                self.mensaje_estado = ""

        # 3. Aviso de Autoguardado
        if self.sabana.ciclos > 0 and self.sabana.ciclos % self.sabana.frecuencia_autoguardado == 0:
             texto_auto = self.fuente.render("AUTOGUARDANDO...", True, (200, 200, 200))
             self.pantalla.blit(texto_auto, (self.ancho_pantalla - 160, 10))

        # --- MENUS ---
        cx = self.ancho_pantalla // 2
        cy = self.alto_pantalla // 2

        if self.modo == "MENU_PRINCIPAL":
            self.pantalla.fill((30, 30, 30))
            t_titulo = self.fuente_grande.render("SIMULADOR ECOSISTEMA", True, (0, 255, 100))
            t1 = self.fuente.render("1. Nueva Partida", True, (255, 255, 255))
            t2 = self.fuente.render("2. Cargar Partida", True, (255, 255, 255))
            t3 = self.fuente.render("3. Salir", True, (255, 255, 255))
            
            self.pantalla.blit(t_titulo, (cx - t_titulo.get_width()//2, cy - 100))
            self.pantalla.blit(t1, (cx - t1.get_width()//2, cy - 20))
            self.pantalla.blit(t2, (cx - t2.get_width()//2, cy + 20))
            self.pantalla.blit(t3, (cx - t3.get_width()//2, cy + 60))

        elif self.modo == "MENU_GUARDAR":
            # Fondo semitransparente
            s = pygame.Surface((500, 300))
            s.set_alpha(230)
            s.fill((0,0,0))
            self.pantalla.blit(s, (cx - 250, cy - 150))
            
            t_titulo = self.fuente_titulo.render("GUARDAR PARTIDA", True, (0, 255, 0))
            self.pantalla.blit(t_titulo, (cx - t_titulo.get_width()//2, cy - 130))

            # Obtenemos textos dinamicos para saber si vamos a sobrescribir
            txt1 = self.obtener_texto_slot("Partida_1", "1. Slot 1")
            txt2 = self.obtener_texto_slot("Partida_2", "2. Slot 2")
            txt3 = self.obtener_texto_slot("Partida_3", "3. Slot 3")
            
            self.pantalla.blit(self.fuente.render(txt1, True, (255, 255, 255)), (cx - 230, cy - 80))
            self.pantalla.blit(self.fuente.render(txt2, True, (255, 255, 255)), (cx - 230, cy - 40))
            self.pantalla.blit(self.fuente.render(txt3, True, (255, 255, 255)), (cx - 230, cy - 0))
            self.pantalla.blit(self.fuente.render("ESC. Volver", True, (255, 100, 100)), (cx - 230, cy + 80))

        elif self.modo == "MENU_CARGAR":
            s = pygame.Surface((500, 300))
            s.set_alpha(230)
            s.fill((0,0,50)) # Azulado
            self.pantalla.blit(s, (cx - 250, cy - 150))
            
            t_titulo = self.fuente_titulo.render("CARGAR PARTIDA", True, (0, 200, 255))
            self.pantalla.blit(t_titulo, (cx - t_titulo.get_width()//2, cy - 130))

            # Textos dinamicos
            txt1 = self.obtener_texto_slot("Partida_1", "1. Cargar Slot 1")
            txt2 = self.obtener_texto_slot("Partida_2", "2. Cargar Slot 2")
            txt3 = self.obtener_texto_slot("Partida_3", "3. Cargar Slot 3")
            txt4 = self.obtener_texto_slot("autoguardado", "4. Autoguardado") # Requisito extra

            self.pantalla.blit(self.fuente.render(txt1, True, (255, 255, 255)), (cx - 230, cy - 80))
            self.pantalla.blit(self.fuente.render(txt2, True, (255, 255, 255)), (cx - 230, cy - 40))
            self.pantalla.blit(self.fuente.render(txt3, True, (255, 255, 255)), (cx - 230, cy - 0))
            self.pantalla.blit(self.fuente.render(txt4, True, (200, 200, 0)), (cx - 230, cy + 40)) # Amarillo
            self.pantalla.blit(self.fuente.render("ESC. Volver", True, (255, 100, 100)), (cx - 230, cy + 100))

    def dibujar(self):
        if self.modo == "MENU_PRINCIPAL":
            self.dibujar_ui()
            pygame.display.flip()
            return

        self.pantalla.blit(self.fondo, (0, 0))

        for comida in self.sabana.comidas:
            x, y = comida.posicion
            img = self.imagenes_comidas[comida.tipo]
            self.pantalla.blit(img, (x * self.tamaño_celda, y * self.tamaño_celda))

        for animal in self.sabana.animales:
            if not animal.vivo:
                continue
            x, y = animal.posicion
            clave = f"{animal.__class__.__name__}_{animal.sexo}"
            img = self.imagenes_animales.get(clave)
            if img:
                self.pantalla.blit(img, (x * self.tamaño_celda, y * self.tamaño_celda))

        self.dibujar_ui()
        pygame.display.flip()

    def ejecutar(self):
        corriendo = True
        while corriendo:
            # Gestion de mensajes desde la logica (ej: autoguardado de martin)
            if hasattr(self.sabana, "ultimo_mensaje") and self.sabana.ultimo_mensaje:
                self.mensaje_estado = self.sabana.ultimo_mensaje
                self.tiempo_mensaje = 60
                self.sabana.ultimo_mensaje = "" # Limpiar mensaje

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                
                if evento.type == pygame.KEYDOWN:
                    
                    if self.modo == "MENU_PRINCIPAL":
                        if evento.key == pygame.K_1: # Nueva Partida
                            self.modo = "JUGANDO"
                        elif evento.key == pygame.K_2: # Cargar Partida
                            self.actualizar_info_slots() # Leemos disco antes de mostrar menu
                            self.modo = "MENU_CARGAR"
                        elif evento.key == pygame.K_3: # Salir
                            corriendo = False
                    
                    elif self.modo == "JUGANDO":
                        if evento.key == pygame.K_g:
                            self.actualizar_info_slots()
                            self.modo = "MENU_GUARDAR"
                        elif evento.key == pygame.K_c:
                            self.actualizar_info_slots()
                            self.modo = "MENU_CARGAR"
                        elif evento.key == pygame.K_ESCAPE:
                            self.modo = "MENU_PRINCIPAL"
                    
                    elif self.modo == "MENU_GUARDAR":
                        slot = ""
                        if evento.key == pygame.K_1: slot = "Partida_1"
                        elif evento.key == pygame.K_2: slot = "Partida_2"
                        elif evento.key == pygame.K_3: slot = "Partida_3"
                        elif evento.key == pygame.K_ESCAPE: self.modo = "JUGANDO"
                        
                        if slot:
                            mensaje = self.sabana.guardar_datos(slot)
                            self.mensaje_estado = mensaje
                            self.tiempo_mensaje = 120
                            self.modo = "JUGANDO"

                    elif self.modo == "MENU_CARGAR":
                        slot = ""
                        if evento.key == pygame.K_1: slot = "Partida_1"
                        elif evento.key == pygame.K_2: slot = "Partida_2"
                        elif evento.key == pygame.K_3: slot = "Partida_3"
                        elif evento.key == pygame.K_4: slot = "autoguardado" # Opcion extra
                        elif evento.key == pygame.K_ESCAPE: 
                            # Si no hay partida activa, volver al principal
                            if len(self.sabana.animales) == 0: 
                                self.modo = "MENU_PRINCIPAL"
                            else:
                                self.modo = "JUGANDO"

                        if slot:
                            exito, mensaje = self.sabana.cargar_datos(slot)
                            self.mensaje_estado = mensaje
                            self.tiempo_mensaje = 120
                            if exito:
                                self.modo = "JUGANDO"

            if self.modo == "JUGANDO":
                self.contador_movimiento += 1
                if self.contador_movimiento >= 30: 
                    self.sabana.mover_hacia_comida()
                    self.sabana.reproducir()
                    self.contador_movimiento = 0

            self.dibujar()
            self.reloj.tick(60)

        pygame.quit()