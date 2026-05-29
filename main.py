import pygame
from pacman import Pared
from pacman import Pacman

lista_paredes = []

with open ("mapa.txt", "r") as archivo: 
    for fila, linea in enumerate (archivo):
        for columna, caracter in enumerate (linea):
            x = fila * 30
            y = columna * 30

            if caracter == "X":
                nueva_pared = Pared (x, y)
                lista_paredes.append(nueva_pared)


ejecutando = True

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

Pacman.move(lista_paredes)


pygame.draw.rect

                
