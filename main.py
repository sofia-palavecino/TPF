import pygame
from pacman import Pared
from pacman import Pacman
from mapa import cargar_mapa
from mapa import verificar_mapa
from mapa import dibujar_mapa
from pacman import Puntuacion
pygame.init()

lista_paredes = []
lista_comida = []
lista_power = []
tamaño_bloque = 22
pacman_x = 0
pacman_y = 0
with open ("mapa.txt", "r") as archivo: 
    for fila, linea in enumerate (archivo):
        for columna, caracter in enumerate (linea):
            y = fila * tamaño_bloque
            x = columna * tamaño_bloque

            if caracter == "X":
                nueva_pared = Pared (x, y)
                lista_paredes.append(nueva_pared)
            elif caracter == "P":
                pacman_x = x 
                pacman_y = y
            elif caracter == ".":
                comida_x = x
                comida_y = y
                lista_comida.append((comida_x, comida_y))
            elif caracter == "o":
                power_x = x
                power_y = y
                lista_power.append ((power_x, power_y))

mapa0 = cargar_mapa('mapa.txt')
mapa = verificar_mapa(mapa0)
ancho = len(mapa[0]) * tamaño_bloque
alto = len(mapa) * tamaño_bloque
pantalla = pygame.display.set_mode((ancho, alto))

negro = (0,0,0)
azul = (0,0,255)
blanco = (255, 255, 255)
amarillo = (255, 255, 0)
rosa = (255, 184, 255)

pacman_personaje = Pacman ("Pacman", pacman_x, pacman_y)
vidas = 3
score = 0
reloj = pygame.time.Clock()
ejecutando = True


while ejecutando:
    reloj.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
    pantalla.fill(negro)
    dibujar_mapa(lista_comida, lista_power) 
    
    teclas = pygame.key.get_pressed()
    pacman_personaje.move(lista_paredes, teclas)
    pacman_personaje.dibujar_pacman(pantalla, amarillo)
    punto_comida, ya_comio, lista_comida = pacman_personaje.comer(lista_comida)
    punto_power, comio_power, lista_power = pacman_personaje.power_pellet(lista_power)
    score += punto_comida
    score += punto_power
    #muerte, vidas = pacman_personaje.choque_fantasma(fantasma_rect, vidas)
    pygame.display.flip()
    

pygame.draw.rect

                
