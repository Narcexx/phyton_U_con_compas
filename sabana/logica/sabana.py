import random
from .elefante import Elefante
from .comida import Pasto, Carne, Insectos
from persistencia.gestor_guardado import Gestor_Guardado

class Sabana:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.animales = []
        self.comidas = []
        
        self.ciclos = 0  # Aquí llevaremos la cuenta de los ciclos
        self.manejador = Gestor_Guardado() 
        self.frecuencia_autoguardado = 50 # Guardar cada 50 ciclos
        self.ultimo_mensaje = "" # Para mandar mensajes a la vista

    def agregar_animal(self, animal):
        self.animales.append(animal)

    def agregar_comida(self, comida):
        self.comidas.append(comida)

    def mover_animales(self):
        
        # Aumentar ciclos y revisar Autoguardado 
        
        self.ciclos += 1  

        if self.ciclos % self.frecuencia_autoguardado == 0:
            self.guardar_datos("autoguardado") # Guardamos en un archivo aparte llamado 'autoguardado'
            self.ultimo_mensaje = "Autoguardado..." 
        
        for animal in list(self.animales):
            if animal.vivo:
                x, y = animal.posicion
                nuevo_x = max(0, min(self.ancho - 1, x + random.randint(-1, 1)))
                nuevo_y = max(0, min(self.alto - 1, y + random.randint(-1, 1)))
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
                            print(f"{a1.nombre} y {a2.nombre} tuvieron un bebe llamado {nombre_hijo}")
                        else:
                            print(f"{a1.nombre} y {a2.nombre} no pueden reproducirse (no comieron 3 veces)")

        self.animales.extend(nuevos_animales)

    def generar_comida(self, cantidad=5):
        # Genera comida aleatoria en distintas posiciones
        tipos = ["pasto", "carne", "insectos"]
        for _ in range(cantidad):
            tipo = random.choice(tipos)
            x = random.randint(0, self.ancho - 1)
            y = random.randint(0, self.alto - 1)
            if tipo == "pasto":
                self.comidas.append(Pasto((x, y)))
            elif tipo == "carne":
                self.comidas.append(Carne((x, y)))
            else:
                self.comidas.append(Insectos((x, y)))


    def mover_hacia_comida(self):
        self.ciclos += 1
        
        # Revisamos Autoguardado aquí también
        if self.ciclos % self.frecuencia_autoguardado == 0:
            self.guardar_datos("autoguardado") 
            self.ultimo_mensaje = "Autoguardado..."
        else:
            # Limpiamos el mensaje si no estamos guardando
            self.ultimo_mensaje = ""

        for animal in self.animales:
            if not animal.vivo:
                continue

            # Definir preferencia
            if animal.__class__.__name__ == "Elefante": preferida = "pasto"
            elif animal.__class__.__name__ == "Leon": preferida = "carne"
            elif animal.__class__.__name__ == "Chimpance": preferida = "insectos"
            else: preferida = None

            # Buscar comida cercana
            comida_cercana = None
            menor_distancia = 999
            for c in self.comidas:
                if c.tipo == preferida:
                    dist = abs(animal.posicion[0] - c.posicion[0]) + abs(animal.posicion[1] - c.posicion[1])
                    if dist < menor_distancia:
                        menor_distancia = dist
                        comida_cercana = c

            # Moverse
            if comida_cercana:
                x, y = animal.posicion
                cx, cy = comida_cercana.posicion
                
                # Logica simple de acercamiento
                if cx > x: x += 1
                elif cx < x: x -= 1
                if cy > y: y += 1
                elif cy < y: y -= 1
                
                animal.posicion = (x, y)

                # Comer si llego
                if animal.posicion == comida_cercana.posicion:
                    animal.comer()
                    # Verificar si la comida sigue en la lista antes de borrarla
                    # (Por si otro animal se la comio en el mismo turno)
                    if comida_cercana in self.comidas:
                        self.comidas.remove(comida_cercana)
        
        # Regenerar comida si falta
        if len(self.comidas) < 3:
            self.generar_comida(5)

    # METODOS PARA PERSISTENCIA

    def guardar_datos(self, nombre_slot):
        # Empaquetamos todo lo necesario para reconstruir la sabana
        datos_modelo = {
            "animales": self.animales,
            "comidas": self.comidas,
            "ancho": self.ancho,
            "alto": self.alto,
            "ciclos": self.ciclos
        }

        # Metadatos para mostrar en el menu
        metadatos = {
            "ciclos": self.ciclos,
            "cant_animales": len(self.animales),
            "info_extra": f"Ciclo {self.ciclos} - {len(self.animales)} Animales"
        }

        exito, mensaje = self.manejador.guardar_partida(nombre_slot, datos_modelo, metadatos)
        return mensaje

    def cargar_datos(self, nombre_slot):
        datos, mensaje = self.manejador.cargar_partida(nombre_slot)

        if datos is not None:
            # Restauramos el estado
            self.animales = datos["animales"]
            self.comidas = datos["comidas"]
            self.ancho = datos["ancho"]
            self.alto = datos["alto"]
            self.ciclos = datos["ciclos"] # Recuperamos el ciclo donde quedamos
            return True, mensaje
        else:
            return False, mensaje

    def obtener_info_partidas(self):
        return self.manejador.listar_partidas()

