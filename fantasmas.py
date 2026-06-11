import pygame
import math
import random

class Fantasma:
    def __init__(self, x, y, color, tile_esquina, tamaño_tile=32):
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
        vel_100_porciento = (7.5 * tamaño_tile) / 60
        self.velocidades_dict = {
            "Scatter": vel_100_porciento * 0.75,         
            "Chase": vel_100_porciento * 0.75,          
            "En Tunel": vel_100_porciento * 0.40,     
            "Asustado": vel_100_porciento * 0.50, 
            "Ojos": vel_100_porciento * 1.50
        }
        self.modo = "Scatter" # "Scatter", "Chase", "Asustado", "Ojos"
    
    def obtener_direccion_opuesta(self, dir_nombre):
        opuestos = {"ARRIBA":"ABAJO","ABAJO":"ARRIBA","IZQUIERDA":"DERECHA","DERECHA":"IZQUIERDA"}
        return opuestos.get(dir_nombre)
    
    def calcular_distancia(self, tile_a, tile_b):
        return math.sqrt((tile_a[0] - tile_b[0])**2 + (tile_a[1] - tile_b[1])**2)
    
    def decidir_sig_direccion(self, mapa):
        opciones_validas = {}
        dir_opuesta = self.obtener_direccion_opuesta(self.direccion_actual)

        for nombre_dir, (dx, dy) in self.dirrecciones.items():
            if nombre_dir == dir_opuesta:
                continue

            sig_x = self.x + dx
            sig_y = self.y + dy

            if 0 <= sig_y < len(mapa) and 0 <= sig_x < len(mapa[0]):
                caracter_tile = mapa[sig_x][sig_y]

                if caracter_tile == 'X':
                    continue
                if caracter_tile in ['-','G'] and self.modo != "Ojos":
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
        
        if mapa[self.y][self.x] == 'T' and self.modo in ["Scatter", "Chase"]:
            self.velocidad_actual = self.velocidades_dict["En Tunel"]
        else:
            self.velocidad_actual = self.velocidades_dict[self.modo]
        
        self.px += dx * self.velocidad_actual
        self.py += dy * self.velocidad_actual

        self.x = int(self.px // self.tamaño_tile)
        self.y = int(self.py // self.tamaño_tile)

        if self.x < 0:
            self.x = len(mapa[0]) - 1
            self.px = self.x * self.tamaño_tile
        elif self.x >= len(mapa[0]):
            self.x = 0
            self.px = 0
        #return [self.x, self.y]

    def dibujar(self, pantalla):
        if self.modo == "Asustado":
            color_render = (0, 0, 255)
        elif self.modo == "Ojos":
            color_render = (255, 255, 255)
        else:
            color_render = self.color

        pygame.draw.circle(pantalla, color_render, (int(self.px + self.tamaño_tile//2), int(self.py + self.tamaño_tile//2)), self.tamaño_tile//2 - 2)

    



class Blinky(Fantasma):
    def __init__(self, x, y, tile_esquina):
        super().__init__(x, y, (255, 0, 0), tile_esquina)
    
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
    
    def actualizar_objetivo(self, pacman_tile, pacman_dir):
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            dx, dy = pacman_dir
            self.tile_objetivo = (pacman_tile[0] + dx * 4, pacman_tile[1] + dy * 4) # para que esté 4 posiciones adelante de la dirección actual de Pac-Man


class Inky(Fantasma):
    def __init__(self, x, y, tile_esquina):
        super().__init__(x, y, (15, 250, 242), tile_esquina)

    def definir_objetivo(self, )