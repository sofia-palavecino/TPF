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
            "Asustado": 2, 
            "Ojos": 4
        }
        self.modo = "Scatter" # "Scatter", "Chase", "Asustado", "Ojos"
        self.velocidad_actual = self.velocidades_dict[self.modo]
        self.sprites_vivos = {}
        self.imagen_actual = None
        self.saliendo = False
        self.objetivo_ghost_house = (13, 14)
        self.objetivo_salida = (13, 11)
        self.activo = False
        self.img_asustado = pygame.transform.scale(pygame.image.load("asustado_azul.jpeg").convert_alpha(), (tamaño_tile, tamaño_tile))
        self.img_asustado_blanco = pygame.transform.scale(pygame.image.load("asustado_blanco.jpeg").convert_alpha(), (tamaño_tile, tamaño_tile))
        self.img_ojos = pygame.transform.scale(pygame.image.load("ojos.png").convert_alpha(), (tamaño_tile, tamaño_tile))
        
    
    def obtener_direccion_opuesta(self, dir_nombre):
        opuestos = {"ARRIBA":"ABAJO","ABAJO":"ARRIBA","IZQUIERDA":"DERECHA","DERECHA":"IZQUIERDA"}
        return opuestos.get(dir_nombre)
    
    def calcular_distancia(self, tile_a, tile_b):
        return math.sqrt((tile_a[0] - tile_b[0])**2 + (tile_a[1] - tile_b[1])**2)
    
    def decidir_sig_direccion(self, mapa):
        if self.saliendo:
            objetivo_real = self.objetivo_salida
        else:
            objetivo_real = self.tile_objetivo
        
        opciones_validas = {}
        dir_opuesta = self.obtener_direccion_opuesta(self.direccion_actual)

        for nombre_dir, (dx, dy) in self.direcciones.items():
            if nombre_dir == dir_opuesta:
                continue

            sig_x = self.x + dx
            sig_y = self.y + dy

            if 0 <= sig_y < len(mapa) and 0 <= sig_x < len(mapa[0]):
                caracter_tile = mapa[sig_y][sig_x]

                if caracter_tile in ('X'):
                    continue
                if caracter_tile == 'G':
                    if self.modo == 'Ojos':
                        pass
                    elif self.saliendo or not self.activo:
                        pass
                    else:
                        continue
                if caracter_tile == '-':
                    if self.modo != 'Ojos' and not self.saliendo:
                        continue

                opciones_validas[nombre_dir] = (sig_x, sig_y)
        
        if not opciones_validas:
            return
        
        if self.modo == "Asustado" and not self.saliendo:
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
        
        if int(self.px) % self.tamaño_tile == 0 and int(self.py) % self.tamaño_tile == 0:
            sig_x = self.x + dx
            sig_y = self.y + dy
            if 0 <= sig_y < len(mapa) and 0 <= sig_x < len(mapa[0]):
                caracter_destino = mapa[sig_y][sig_x]
                bloqueado = False
                if caracter_destino in ('X'):
                    bloqueado = True
                elif caracter_destino == 'G':
                    if self.modo != 'Ojos' and not (self.saliendo or not self.activo):
                        bloqueado = True
                elif caracter_destino == '-':
                    if self.modo != 'Ojos' and not self.saliendo:
                        bloqueado = True
                if bloqueado:
                    dx, dy = 0, 0
        
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

        if self.modo == "Ojos" and (self.x, self.y) == self.objetivo_ghost_house:
            self.cambiar_modo("Scatter")
            self.activo = True
            self.saliendo = True
            self.px = self.x * self.tamaño_tile
            self.py = self.y * self.tamaño_tile
            self.direccion_actual = "ARRIBA"

        if self.saliendo and 0 <= self.y < len(mapa) and 0 <= self.x < len(mapa[0]):
            if mapa[self.y][self.x] == '-':
                self.saliendo = False

        if self.modo not in ("Ojos", "Asustado"):
            if self.direccion_actual in self.sprites_vivos:
                self.imagen_actual = self.sprites_vivos[self.direccion_actual]

    def dibujar(self, pantalla, tiempo_susto_inicio, modo_asustado_global, pacman_tile):
        img_a_dibujar = self.imagen_actual
        
        if self.modo == "Ojos":
            if hasattr(self, 'img_ojos') and self.img_ojos is not None:
                img_a_dibujar = self.img_ojos
        
        elif self.modo == "Asustado" and modo_asustado_global:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - tiempo_susto_inicio) / 1000.0

            if tiempo_transcurrido >= 4.0:
                if (tiempo_actual // 200) % 2 == 0:
                    img_a_dibujar = self.img_asustado if hasattr(self, 'img_asustado') else None
                else:
                    img_a_dibujar = self.img_asustado_blanco if hasattr(self, 'img_asustado_blanco') else None
            else:
                img_a_dibujar = self.img_asustado if hasattr(self, 'img_asustado') else None
        
        if img_a_dibujar is not None:
            if self.nombre == 'Mysterious' and self.calcular_distancia((self.x, self.y), pacman_tile)>12: # con esta línea logro el poder especial de mysterious: mostrarse solo si está en un ciruclo de radio 12 alrededor de pacman
                return
            pantalla.blit(img_a_dibujar, (int(self.px), int(self.py)))


        else: # respaldo por si fallan las imagenes
            centro_x = int(self.px + self.tamaño_tile // 2)
            centro_y = int(self.py + self.tamaño_tile // 2)
            radio = self.tamaño_tile // 2
            if self.modo == "Asustado":
                tiempo_actual = pygame.time.get_ticks()
                if ((tiempo_actual - tiempo_susto_inicio) / 1000.0) >= 4.0 and (tiempo_actual // 200) % 2 !=0:
                    color_respaldo = (255, 255, 255)
                else:
                    color_respaldo = (0, 0, 255)
            elif self.modo == "Ojos":
                color_respaldo = (255, 255, 255)
            else:
                color_respaldo = self.color
            
            pygame.draw.circle(pantalla, color_respaldo, (centro_x, centro_y), radio)

    
class Blinky(Fantasma):
    def __init__(self, x, y, tile_esquina, tamaño_tile):
        super().__init__(x, y, (255, 0, 0), tile_esquina, tamaño_tile)
        self.nombre = 'Blinky'
        self.sprites_vivos = {
            "ARRIBA": pygame.transform.scale(pygame.image.load('blinky_arriba.jpeg'), (tamaño_tile, tamaño_tile)),
            "ABAJO": pygame.transform.scale(pygame.image.load('blinky_abajo.jpeg'), (tamaño_tile, tamaño_tile)),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load('blinky_izq.jpeg'), (tamaño_tile, tamaño_tile)),
            "DERECHA": pygame.transform.scale(pygame.image.load('blinky_der.jpeg'), (tamaño_tile, tamaño_tile))
        }
        self.imagen_actual = self.sprites_vivos["DERECHA"]

    def actualizar_objetivo(self, pacman_tile, pacman_dir=None):
        if self.saliendo:
            self.tile_objetivo = self.objetivo_salida
            return
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            self.tile_objetivo = pacman_tile
        elif self.modo == "Ojos":
            self.tile_objetivo = self.objetivo_ghost_house


class Pinky(Fantasma):
    def __init__(self, x, y, tile_esquina, tamaño_tile):
        super().__init__(x, y, (255, 184, 255), tile_esquina, tamaño_tile)
        self.nombre = 'Pinky'
        self.sprites_vivos = {
            "ARRIBA": pygame.transform.scale(pygame.image.load('pinky_arriba.jpeg'), (tamaño_tile, tamaño_tile)),
            "ABAJO": pygame.transform.scale(pygame.image.load('pinky_abajo.jpeg'), (tamaño_tile, tamaño_tile)),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load('pinky_izq.jpeg'), (tamaño_tile, tamaño_tile)),
            "DERECHA": pygame.transform.scale(pygame.image.load('pinky_der.jpeg'), (tamaño_tile, tamaño_tile))
        }
        self.imagen_actual = self.sprites_vivos["IZQUIERDA"]
    
    def actualizar_objetivo(self, pacman_tile, pacman_dir):
        if self.saliendo:
            self.tile_objetivo = self.objetivo_salida
            return
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            dx, dy = pacman_dir
            self.tile_objetivo = (pacman_tile[0] + dx * 4, pacman_tile[1] + dy * 4) # para que esté 4 posiciones adelante de la dirección actual de Pac-Man
        elif self.modo == "Ojos":
            self.tile_objetivo = self.objetivo_ghost_house


class Inky(Fantasma):
    def __init__(self, x, y, tile_esquina, tamaño_tile):
        super().__init__(x, y, (15, 250, 242), tile_esquina, tamaño_tile)
        self.nombre = 'Inky'
        self.sprites_vivos = {
            "ARRIBA": pygame.transform.scale(pygame.image.load('inky_arriba.jpeg'), (tamaño_tile, tamaño_tile)),
            "ABAJO": pygame.transform.scale(pygame.image.load('inky_abajo.jpeg'), (tamaño_tile, tamaño_tile)),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load('inky_izq.jpeg'), (tamaño_tile, tamaño_tile)),
            "DERECHA": pygame.transform.scale(pygame.image.load('inky_der.jpeg'), (tamaño_tile, tamaño_tile))
        }
        self.imagen_actual = self.sprites_vivos["IZQUIERDA"]
        
        self.pivot = None
        self.punto_cero = None
        self.vector = None

    def elegir_fantasma_pivot(self, lista_fants):
        otros = []
        blinky_objeto = None
        for fantasma in lista_fants:
            if isinstance(fantasma, Blinky):
                blinky_objeto = fantasma
            elif fantasma is not self:
                otros.append(fantasma)
        if blinky_objeto is not None:
            fantasma_pivot = blinky_objeto
        elif otros: #si no está blinky y hay objetos en otros
            fantasma_pivot = random.choice(otros)
        else:
            fantasma_pivot = self
        self.pivot = (fantasma_pivot.x, fantasma_pivot.y)

    def elegir_punto_cero(self, pacman_tile, pacman_dir_matriz):
        dx, dy = pacman_dir_matriz
        self.punto_cero = [pacman_tile[0] + dx * 2, pacman_tile[1] + dy * 2]

    def calcular_vector(self):
        self.vector = [self.pivot[0]-self.punto_cero[0], self.pivot[1]-self.punto_cero[1]]

    def actualizar_objetivo(self, pacman_tile, pacman_dir_matriz, lista_fants):
        if self.saliendo:
            self.tile_objetivo = self.objetivo_salida
            return
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            self.elegir_fantasma_pivot(lista_fants)
            self.elegir_punto_cero(pacman_tile, pacman_dir_matriz)
            self.calcular_vector()
            self.tile_objetivo = (self.punto_cero[0]+self.vector[0], self.punto_cero[1]+self.vector[1])
        elif self.modo == "Ojos":
            self.tile_objetivo = self.objetivo_ghost_house

class Clyde(Fantasma):
    def __init__(self, x, y, tile_esquina, tamaño_tile):
        super().__init__(x, y, (250, 171, 52), tile_esquina, tamaño_tile)
        self.distancia_clyde_y_pacman = 0
        self.nombre = 'Clyde'
        self.sprites_vivos = {
            "ARRIBA": pygame.transform.scale(pygame.image.load('clyde_arriba.jpeg'), (tamaño_tile, tamaño_tile)),
            "ABAJO": pygame.transform.scale(pygame.image.load('clyde_abajo.jpeg'), (tamaño_tile, tamaño_tile)),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load('clyde_izq.jpeg'), (tamaño_tile, tamaño_tile)),
            "DERECHA": pygame.transform.scale(pygame.image.load('clyde_der.jpeg'), (tamaño_tile, tamaño_tile))
        }
        self.imagen_actual = self.sprites_vivos["IZQUIERDA"]

    def actualizar_objetivo(self, pacman_tile):
        if self.saliendo:
            self.tile_objetivo = self.objetivo_salida
            return
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            self.distancia_clyde_y_pacman = self.calcular_distancia((self.x,self.y), pacman_tile)
            if self.distancia_clyde_y_pacman > 8:
                self.tile_objetivo = pacman_tile
            else:
                self.tile_objetivo = self.tile_esquina
        elif self.modo == "Ojos":
            self.tile_objetivo = self.objetivo_ghost_house

class Silly(Fantasma): # su movimiento es random, pero respeta que no puede volver hacia atrás
    def __init__(self, x, y, tile_esquina, tamaño_tile):
        super().__init__(x, y, (250, 171, 52), tile_esquina, tamaño_tile)
        self.nombre = 'Silly'
        self.sprites_vivos = {
            "ARRIBA": pygame.transform.scale(pygame.image.load('silly_arriba.jpg'), (tamaño_tile, tamaño_tile)),
            "ABAJO": pygame.transform.scale(pygame.image.load('silly_abajo.jpg'), (tamaño_tile, tamaño_tile)),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load('silly_izq.jpg'), (tamaño_tile, tamaño_tile)),
            "DERECHA": pygame.transform.scale(pygame.image.load('silly_der.jpg'), (tamaño_tile, tamaño_tile))
        }
        self.imagen_actual = self.sprites_vivos["IZQUIERDA"]

    def decidir_sig_direccion_silly(self, mapa): # se aplica una logica similar al movimiento de los fantasmas en modo asustado     
        opciones_validas = {}
        dir_opuesta = self.obtener_direccion_opuesta(self.direccion_actual)
        for nombre_dir, (dx, dy) in self.direcciones.items():
            if nombre_dir == dir_opuesta:
                continue
            sig_x = self.x + dx
            sig_y = self.y + dy
            if 0 <= sig_y < len(mapa) and 0 <= sig_x < len(mapa[0]):
                caracter_tile = mapa[sig_y][sig_x]
                if caracter_tile in ('X'):
                    continue
                if caracter_tile == '-':
                    continue
                opciones_validas[nombre_dir] = (sig_x, sig_y)
        if not opciones_validas:
            self.direccion_actual = dir_opuesta # si por alguna razon no tiene a donde ir, se le permite darse vuelta 180 grados
            return
        self.direccion_actual = random.choice(list(opciones_validas.keys()))

    def actualizar_objetivo(self, mapa):
        if self.saliendo:
            self.tile_objetivo = self.objetivo_salida
            return
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase": # se le suma a su posicion actual la direccion random elegida
            self.decidir_sig_direccion_silly(mapa)
            dx, dy = self.direcciones[self.direccion_actual]
            self.tile_objetivo = (self.x+dx, self.y+dy) 
        elif self.modo == "Ojos":
            self.tile_objetivo = self.objetivo_ghost_house 


class Mysterious(Fantasma): # se mueve como pinky, pero hacia atrás de pacman. en la pantalla aparece parpadeante y parece que se teletransporta
    def __init__(self, x, y, tile_esquina, tamaño_tile):
        super().__init__(x, y, (255, 184, 255), tile_esquina, tamaño_tile)
        self.nombre = 'Mysterious'
        self.sprites_vivos = {
            "ARRIBA": pygame.transform.scale(pygame.image.load('mysterious_arriba.jpg'), (tamaño_tile, tamaño_tile)),
            "ABAJO": pygame.transform.scale(pygame.image.load('mysterious_abajo.jpg'), (tamaño_tile, tamaño_tile)),
            "IZQUIERDA": pygame.transform.scale(pygame.image.load('mysterious_izq.jpg'), (tamaño_tile, tamaño_tile)),
            "DERECHA": pygame.transform.scale(pygame.image.load('mysterious_der.jpg'), (tamaño_tile, tamaño_tile))
        }
        self.imagen_actual = self.sprites_vivos["IZQUIERDA"]

    def actualizar_objetivo(self, pacman_tile, pacman_dir):
        if self.saliendo:
            self.tile_objetivo = self.objetivo_salida
            return
        if self.modo == "Scatter":
            self.tile_objetivo = self.tile_esquina
        elif self.modo == "Chase":
            dx, dy = pacman_dir
            self.tile_objetivo = (pacman_tile[0] + dx * -4, pacman_tile[1] + dy * -4) # para que esté 4 posiciones detrás de la dirección actual de Pac-Man
        elif self.modo == "Ojos":
            self.tile_objetivo = self.objetivo_ghost_house              

# IDEAS
# hacer que se printee una x en el tile objetivo así corroborar si están funcionando bien los algoritmos











# the wizard: wizzy. envenena a pacman cuando colisionan. pacman se pone verde en el modo embrujado. si comes powerpellet se rompe el embrujo. este fantasma va a ser violeta
# the guardian: blanco. su funcion es crear un escudo para pacman cuando estas en chase indefinido. twinky