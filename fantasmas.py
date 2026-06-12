import pygame
import math
import random
import os 

class Fantasma:
    def __init__(self, x, y, color, tile_esquina, tamaño_tile=22):
        self.tamaño_tile = tamaño_tile
        self.x = x
        self.y = y
        self.px = x * tamaño_tile
        self.py = y * tamaño_tile
        self.color = color
        self.tile_esquina = tile_esquina
        self.tile_objetivo = tile_esquina # es el objetivo actual (va cambiando)
        self.direcciones = {"ARRIBA":(0,-1), "IZQUIERDA":(-1,0), "ABAJO":(0,1), "DERECHA":(1,0)} # este diccionario ya está orden de prioridad de movimiento si dos rutas tienen exactamente la misma distancia lineal
        self.direccion_actual = "IZQUIERDA"
        self.velocidades_dict = {
            "Scatter": 2,         
            "Chase": 2,          
            "En Tunel": 1,     
            "Asustado": 1, 
            "Ojos": 4
        }
        self.modo = "Scatter" # "Scatter", "Chase", "Asustado", "Ojos"
        self.velocidad_actual = self.velocidades_dict[self.modo]
        self.imagen_actual = None
        try:
            self.img_asustado = pygame.transform.scale(pygame.image.load("asustado.png").convert_alpha(), (tamaño_tile, tamaño_tile))
            self.img_ojos = pygame.transform.scale(pygame.image.load("ojos.png").convert_alpha(), (tamaño_tile, tamaño_tile))
        except:
            self.img_asustado = None
            self.img_ojos = None
    
    def obtener_direccion_opuesta(self, dir_nombre):
        opuestos = {"ARRIBA":"ABAJO","ABAJO":"ARRIBA","IZQUIERDA":"DERECHA","DERECHA":"IZQUIERDA"}
        return opuestos.get(dir_nombre)
    
    def calcular_distancia(self, tile_a, tile_b):
        return math.sqrt((tile_a[0] - tile_b[0])**2 + (tile_a[1] - tile_b[1])**2)
    
    def decidir_sig_direccion(self, mapa):
        opciones_validas = {}
        dir_opuesta = self.obtener_direccion_opuesta(self.direccion_actual)

        for nombre_dir, (dx, dy) in self.direcciones.items():
            if nombre_dir == dir_opuesta:
                continue

            sig_x = self.x + dx
            sig_y = self.y + dy

            if 0 <= sig_y < len(mapa) and 0 <= sig_x < len(mapa[0]):
                caracter_tile = mapa[sig_y][sig_x]

                if caracter_tile == 'X':
                    continue
                if caracter_tile == 'G' and self.modo != "Ojos":
                    continue
                if caracter_tile == '-' and (not self.activo or self.modo == "Asustado"):
                    continue

                opciones_validas[nombre_dir] = (sig_x, sig_y)
        
        if not opciones_validas:
            return
        
        if self.modo == "Asustado":
            self.direccion_actual = random.choice(list(opciones_validas.keys()))
        else:
            mejor_dir = None
            distancia_min = float('inf')
            for nombre_dir, pos_tile in opciones_validas.items():
                dist = self.calcular_distancia(pos_tile, self.tile_objetivo)
                if dist < distancia_min:
                    distancia_min = dist
                    mejor_dir = nombre_dir
            if mejor_dir:
                self.direccion_actual = mejor_dir
    
    def cambiar_modo(self, nuevo_modo):
        if self.modo != nuevo_modo:
            self.modo = nuevo_modo
            self.direccion_actual = self.obtener_direccion_opuesta(self.direccion_actual) # al cambiar de modo, invierten su dirección
    
    def actualizar_posicion(self, mapa):
        dx, dy = self.direcciones[self.direccion_actual]
        
        columnas_totales = len(mapa[0])

        if self.x < 0:
            self.x = columnas_totales - 1
            self.px = self.x * self.tamaño_tile
        elif self.x >= columnas_totales:
            self.x = 0
            self.px = 0

        if 0 <= self.y < len(mapa) and 0 <= self.x < len(mapa[0]):
            if mapa[self.y][self.x] == 'T' and self.modo in ["Scatter", "Chase"]:
                self.velocidad_actual = self.velocidades_dict["En Tunel"]
            else:
                self.velocidad_actual = self.velocidades_dict[self.modo]
        else:
            self.velocidad_actual = self.velocidades_dict[self.modo]

        self.px += dx * self.velocidad_actual
        self.py += dy * self.velocidad_actual

        self.x = int(self.px // self.tamaño_tile)
        self.y = int(self.py // self.tamaño_tile)

        if self.modo == "Ojos":
            if self.x == 13 and self.y == 11:
                self.cambiar_modo("Scatter")
                self.activo = True
                self.px = self.x * self.tamaño_tile
                self.py = self.y * self.tamaño_tile
                self.direccion_actual = "ARRIBA"

    def dibujar(self, pantalla):
        img_a_dibujar = self.imagen_actual
        
        if self.modo == "Asustado":
            if hasattr(self, 'img_asustado') and self.img_asustado is not None:
                img_a_dibujar = self.img_asustado
        elif self.modo == "Ojos":
            if hasattr(self, 'img_ojos') and self.img_ojos is not None:
                img_a_dibujar = self.img_ojos

        if img_a_dibujar is not None:
            pantalla.blit(img_a_dibujar, (int(self.px), int(self.py)))
        else:
            centro_x = int(self.px + self.tamaño_tile // 2)
            centro_y = int(self.py + self.tamaño_tile // 2)
            radio = self.tamaño_tile // 2
            
            if self.modo == "Asustado":
                color_respaldo = (0, 0, 255)
            elif self.modo == "Ojos":
                color_respaldo = (255, 255, 255)
            else:
                color_respaldo = self.color
            
            pygame.draw.circle(pantalla, color_respaldo, (centro_x, centro_y), radio)

    
class Blinky(Fantasma):
    def __init__(self, x, y, tile_esquina):
        super().__init__(x, y, (255, 0, 0), tile_esquina)

        try:
            imagen_base = pygame.image.load("blinky.png").convert_alpha()
            self.imagen_actual = pygame.transform.scale(imagen_base, (self.tamaño_tile, self.tamaño_tile))
        except:
            print("No se pudo cargar la imagen de Blinky, se usará el color base.")

    def actualizar_objetivo(self, pacman_tile, pacman_dir=None):
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            self.tile_objetivo = pacman_tile
        elif self.modo == "Ojos":
            self.tile_objetivo = (13, 11) # coordenadas de la Ghost House


class Pinky(Fantasma):
    def __init__(self, x, y, tile_esquina):
        super().__init__(x, y, (255, 184, 255), tile_esquina)
        
        try:
            imagen_base = pygame.image.load("pinky.png").convert_alpha()
            self.imagen_actual = pygame.transform.scale(imagen_base, (self.tamaño_tile, self.tamaño_tile))
        except:
            print("No se pudo cargar la imagen de Pinky, se usará el color base.")
   
    def actualizar_objetivo(self, pacman_tile, pacman_dir):
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            dx, dy = pacman_dir
            self.tile_objetivo = (pacman_tile[0] + dx * 4, pacman_tile[1] + dy * 4) # para que esté 4 posiciones adelante de la dirección actual de Pac-Man
        elif self.modo == "Ojos":
            self.tile_objetivo = (13, 11)

class Inky(Fantasma): # tal vez sería mejor que en dicc_fantasmas se guarde también el estado de los fantasmas. por ejemplo, no se toman en cuenta las coor de blinky si está en modo ojos --> crear el dicc_fantasmas en paralelo a la lista_fants
    def __init__(self, x, y, tile_esquina):
        super().__init__(x, y, (15, 250, 242), tile_esquina)
        self.pivot = None
        self.punto_cero = None
        self.vector = None

    def elegir_pivot(self, dicc_fantasmas): # dicc_fantasmas me permite usar a un fantasma random como pivot si blinky no está en la partida. dicc fantasma tiene LISTAS de posicion de cada fantasma
        if "Blinky" in dicc_fantasmas: # esto depende de qué hagamos con cada fantasma cuando es comido: desparece? sus coordenadas están vacías o en la ghost house?
            self.pivot = dicc_fantasmas["Blinky"]
        else:
            opciones_pivot=[]
            for nombre in dicc_fantasmas:
                if nombre != "Inky":
                    opciones_pivot.append(nombre)
            if len(opciones_pivot)==0: # si solo queda inky --> CONSULTAR: qué les parece que hagamos si solo queda inky? opciones: tileesquina, que haga lo mismo que blinky o que se use a sí mismo de pivot
                self.pivot = dicc_fantasmas["Inky"]
            else:
                self.pivot = dicc_fantasmas[random.choice(opciones_pivot)] # para chequear: que pasa si solo está disponible inky en la partida? existe tal escenario?

    def elegir_punto_cero(self, pacman_tile, pacman_dir):
        dx, dy = pacman_dir
        self.punto_cero = [pacman_tile[0] + dx * 2, pacman_tile[1] + dy * 2]

    def calcular_vector(self):
        self.vector = [self.pivot[0]-self.punto_cero[0], self.pivot[1]-self.punto_cero[1]]

    def actualizar_objetivo_inky(self, dicc_fantasmas, pacman_tile, pacman_dir):
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            self.elegir_pivot(dicc_fantasmas)
            self.elegir_punto_cero(pacman_tile, pacman_dir)
            self.calcular_vector()
            self.tile_objetivo = (self.punto_cero[0]-self.vector[0], self.punto_cero[1]-self.vector[1])

class Clyde(Fantasma):
    def __init__(self, x, y, tile_esquina):
        super().__init__(x, y, (250, 171, 52), tile_esquina)
        self.distancia_clyde_y_pacman = 0

    def actualizar_objetivo(self, pacman_tile):
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            self.distancia_clyde_y_pacman = self.calcular_distancia((self.x,self.y), pacman_tile)
            if self.distancia_clyde_y_pacman > 8:
                self.tile_objetivo = pacman_tile
            else:
                self.tile_objetivo = self.tile_esquina


# IDEAS
# hacer que se printee una x en el tile objetivo así corroborar si están funcionando bien los algoritmos
# the wizard: wizzy. envenena a pacman cuando colisionan. pacman se pone verde en el modo embrujado. si comes powerpellet se rompe el embrujo. este fantasma va a ser violeta
# the guardian: blanco. su funcion es crear un escudo para pacman cuando estas en chase indefinido. twinky