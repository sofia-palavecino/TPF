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

pacman_personaje = Pacman ("Pacman", pacman_x, pacman_y)
vidas = 3
score = 0
punto_fants = 0
reloj = pygame.time.Clock()
ejecutando = True
modo_asustado = False
estado = "MENU"

while ejecutando:
    reloj.tick(60)
    if estado == "MENU": #Página de inicio
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    estado = "MENU_FANTS"
        pantalla.fill(negro)
        fuente_titulo = pygame.font.SysFont("Courier New", 50, bold = True)
        fuente_subtitulo = pygame.font.SysFont("Comic Sans MS", 30)
        
        texto_titulo = fuente_titulo.render("PAC-MAN", True, (255, 255, 0)) #texto amarillo
        texto_instrucciones = fuente_subtitulo.render("Presiona ENTER para comenzar", True, (255, 255, 255)) #texto blanco

        pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 200)) #centrar el texto
        pantalla.blit (texto_instrucciones, (ancho // 2 - texto_instrucciones.get_width() // 2, 400))
    elif estado == "MENU_FANTS":
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    estado = "JUEGO" 
        pantalla.fill(negro)
        fuente_texto = pygame.font.SysFont("Courier New", 30, bold = True)
        cuenta_fants = 0
        texto_elegir = fuente_texto.render (f"Elija 4 fantasmas: [{cuenta_fants}/4]", True, (255, 255, 0))

        dicc_nomb_fants = {"blinky": "el merodeador", "pinky": "el", "inky": "el", "clyde" : "el", "spike": "el", "coward": "el"}
        pos_fants_x = 100
        pos_fants_y = 100
        fuente_sub_fants = pygame.font.SysFont("Arial", 20)
        for fantasma, descripcion in dicc_nomb_fants.items():
            nombre = fuente_texto.render (f"{fantasma}", True, (255, 255, 0))
            pantalla.blit(nombre, (pos_fants_x, pos_fants_y))
            pos_fants_y += 40
            descrp = fuente_sub_fants.render (f"{descripcion}", True, (255, 255, 255))
            pantalla.blit(descrp, (pos_fants_x, pos_fants_y))
            pos_fants_y += 40
            #hacer rectángulo
            pos_x = ancho // 2 - nombre.get_width() // 2
            pos_y = 50
            rect_nombre = nombre.get_rect()
            rect_nombre.x = pos_x 
            rect_nombre.y = pos_y
            rect_descp = descrp.get_rect()
            rect_descp.x = ancho // 2 - descrp.get_width() // 2 + rect_nombre.x
            rect_descp.y = pos_y
            pygame.draw.rect (pantalla, (0, 0, 255), rect_descp, 3) 
            
        pantalla.blit(texto_elegir, (pos_x, pos_y)) 
    


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
    pygame.display.flip()
    

pygame.draw.rect

