import pygame
from pacman import Pared
from pacman import Pacman
from mapa import cargar_mapa
from mapa import verificar_mapa
from mapa import dibujar_mapa
from pacman import Puntuacion
from pantallas import pantalla_main
from pantallas import pantalla_fants
from pantallas import pantalla_game
pygame.init() 

lista_paredes = []
lista_comida = []
lista_power = []
lista_fants = [] #falta ver cómo obtener las coordenadas de los fantasmas en una lista, para saber dónde están y ver si se lo chocan a pacman
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
rojo = (255, 0, 0)
verde = (0, 128, 0)
violeta = (128, 0, 128)
gris = (128, 128, 128)


pacman_personaje = Pacman ("Pacman", pacman_x, pacman_y)
vidas = 3
score = 0
punto_fants = 0
reloj = pygame.time.Clock()
ejecutando = True
modo_asustado = False
estado = "MENU" 
opciones_fants = {"Blinky": "el que persigue", "Pinky" : "el que", "Inky": "el que", "Clyde": "el que", "Coward": "el que", "Spyke": "el que"}
claves_fants = list(opciones_fants.keys()) #mantener los nombres como una lista facilita al momento de saber en qué opción está el usuario
lista_colores = [rojo, rosa, azul, verde, violeta, blanco]
ind_selecc = 0
fants_elegidos = []


while ejecutando:
    reloj.tick(60)
    tiempo = pygame.time.get_ticks()
    if estado == "MENU": #Página de inicio
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    estado = "MENU_FANTS"
        pantalla_main(pantalla, ancho, tiempo)

    elif estado == "MENU_FANTS": #página de elegir los fantasmas
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    ind_selecc += 1 
                    if ind_selecc >= len(claves_fants):
                        ind_selecc = 0
                elif evento.key == pygame.K_UP:
                    ind_selecc -= 1
                    if ind_selecc < 0:
                        ind_selecc = len(claves_fants) - 1
                elif evento.key == pygame.K_RETURN:
                    if len(fants_elegidos) < 4: 
                        opcion_actual = claves_fants[ind_selecc]
                        if opcion_actual not in fants_elegidos:
                            fants_elegidos.append (opcion_actual)
                        if len(fants_elegidos) == 4:
                            estado = "OVER"
        pantalla_fants(pantalla, fants_elegidos, opciones_fants, lista_colores, ind_selecc)
    elif estado == "OVER":
        puntaje = 0 
        pantalla_game(pantalla, puntaje)
    elif estado == "JUEGO":
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
        if comio_power: #si comio power pellet se activa el modo asustado
            modo_asustado = True 
            pacman_personaje.velocidad * 0.9
            pacman_personaje.comer_fantasma(comio_power, lista_fants, punto_fants)
        else:
            pacman_personaje.velocidad * 0.8 #velocidad normal
        #muerte, vidas = pacman_personaje.choque_fantasma(fantasma_rect, vidas)
    
    elif estado == "OVER":
        pantalla_game(pantalla)
    pygame.display.flip()
    

pygame.draw.rect

