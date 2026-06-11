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
from pantallas import margen_mapa
from pantallas import pantalla_esquina

pygame.init() 
pygame.mixer.init() 

lista_paredes = []
lista_comida = []
lista_comida_orig = [] #para guardar la comida del mapa original y poder regenerarla en el siguiente nivel
lista_power = []
lista_power_orig = []
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
                lista_comida_orig.append((comida_x, comida_y))
            elif caracter == "o":
                power_x = x
                power_y = y
                lista_power.append ((power_x, power_y))
                lista_power_orig.append ((power_x, power_y))

mapa0 = cargar_mapa('mapa.txt')
mapa = verificar_mapa(mapa0)
ancho = len(mapa[0]) * tamaño_bloque
alto = len(mapa) * tamaño_bloque
pantalla = pygame.display.set_mode((ancho, alto + 50)) #le agrego al alto para tener el margen donde imprimir las vidas, el nivel, etc.

#colores
negro = (0,0,0)
azul = (0,0,255)
blanco = (255, 255, 255)
amarillo = (255, 255, 0)
rosa = (255, 184, 255)
rojo = (255, 0, 0)
verde = (0, 128, 0)
violeta = (128, 0, 128)
gris = (128, 128, 128)

#sonidos:
sonido_comer = pygame.mixer.Sound ("comer_punto.mp3")
sonido_power = pygame.mixer.Sound ("comer_pellet.mp3")
sonido_intro = pygame.mixer.Sound ("intro.mp3")
sonido_muerte_fants = pygame.mixer.Sound("muerte_fants.mp3")
sonido_muerte_pacman = pygame.mixer.Sound ("muerte_pacman.mp3") #falta agregarlo a cuando muere
sonido_nivel = pygame.mixer.Sound ("nivel.mp3")
sonido_vida_extra = pygame.mixer.Sound ("vida_extra.mp3")
sonido_select = pygame.mixer.Sound ("select.mp3") 

#datos para comenzar pygame:
reloj = pygame.time.Clock()
ejecutando = True
estado = "MENU" 
#datos para pacman y puntaje:
pacman_personaje = Pacman ("Pacman", pacman_x, pacman_y)
vidas = 3 
score = 0
punto_fants = 0
nivel = 1  
high_score = 0
#pantalla fantasmas: 
opciones_fants = {"Blinky": "el que persigue", "Pinky" : "el que", "Inky": "el que", "Clyde": "el que", "Coward": "el que", "Spyke": "el que"}
claves_fants = list(opciones_fants.keys()) #mantener los nombres como una lista facilita al momento de saber en qué opción está el usuario
lista_colores = [rojo, rosa, azul, verde, violeta, blanco]
colores_fants = dict(zip(claves_fants, lista_colores)) #creo un diccionarios con los nombres de los fantasmas y sus colores 
esquinas_elegidas = {} #luego queda con el nombre del fantasma de clave y el valor es dónde se va a posicionar. ej: pinky: superior izquierda. 
opciones_esquina = ["Superior izquierda", "Superior derecha", "Inferior izquierda", "Inferior derecha"]
ind_selecc = 0
ind_fant = 0
fantasma_actual = claves_fants[ind_selecc]
fants_elegidos = []
#modo asustado
modo_asustado = False
duracion_susto = 6000 #6 segundos
tiempo_susto = 0
fantasmas_comidos = 0

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
        pantalla_main(pantalla, ancho, tiempo, high_score)
        sonido_intro.play() 

    elif estado == "MENU_FANTS": #página de elegir los fantasmas
        sonido_intro.stop()
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
                    sonido_select.play()
                    if len(fants_elegidos) < 4: 
                        opcion_actual = claves_fants[ind_selecc]
                        if opcion_actual not in fants_elegidos:
                            fants_elegidos.append (opcion_actual)
                        if len(fants_elegidos) == 4:
                            estado = "MENU_ESQUINAS"
        pantalla_fants(pantalla, fants_elegidos, opciones_fants, lista_colores, ind_selecc)
    elif estado == "MENU_ESQUINAS":
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                teclas_num = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3}
                if evento.key in teclas_num:
                    fantasma_actual = fants_elegidos[ind_fant]
                    esquinas_elegidas[fantasma_actual] = opciones_esquina[teclas_num[evento.key]]
                    ind_fant += 1
                    sonido_select.play()
                    if ind_fant >= len (fants_elegidos):
                        estado = "JUEGO"
        pantalla_esquina(pantalla, fantasma_actual, fants_elegidos, ind_fant, colores_fants, opciones_esquina, esquinas_elegidas)
        
    elif estado == "JUEGO": 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        
        pantalla.fill(negro)
        dibujar_mapa(lista_comida, lista_power)
        margen_mapa(pantalla, score, nivel, high_score, vidas) 

        teclas = pygame.key.get_pressed()
        pacman_personaje.move(lista_paredes, teclas)
        pacman_personaje.dibujar_pacman(pantalla)
        punto_comida, ya_comio, lista_comida = pacman_personaje.comer(lista_comida)
        if ya_comio: 
            sonido_comer.play() 
        punto_power, comio_power, lista_power = pacman_personaje.power_pellet(lista_power)
        if comio_power:
            sonido_power.play()
        score += punto_comida
        score += punto_power
        if comio_power: #si comio power pellet se activa el modo asustado
            modo_asustado = True 
            tiempo_susto = pygame.time.get_ticks()
        if modo_asustado: 
            tiempo_restante = duracion_susto - (pygame.time.get_ticks() - tiempo_susto)
            if tiempo_restante < 2000:
                if (pygame.time.get_ticks() // 200) % 2 == 0:
                    pygame.draw.rect(pantalla, negro, (pacman_personaje.x, pacman_personaje.y, 22, 22))#parpadea en los últimos dos segundos del modo asustado
            if pygame.time.get_ticks() - tiempo_susto >= duracion_susto:
                modo_asustado = False 
                pacman_personaje.velocidad * 0.8 #velocidad normal
            else: 
                pacman_personaje.velocidad * 0.9
                #lista_fantasmas, puntos_fants, comio_fantasma = pacman_personaje.comer_fantasma(comio_power, lista_fants, punto_fants, fantasmas_comidos) 
                #if comio_fantasma: 
                    #fantasmas_comidos += 1
                    #sonido_muerte_fants.play() 
                #muerte, vidas = pacman_personaje.choque_fantasma(fantasma_rect, vidas) a

                
        if len(lista_comida) == 0: #si se termina la comida, avanza un nivel
            nivel += 1
            sonido_nivel.play() 
            lista_comida = lista_comida_orig #que se regenere la comida del mapa original
            lista_power = lista_power_orig 
            fuente_titulo = pygame.font.SysFont("comicans", 60, bold = True)
            texto_titulo = fuente_titulo.render("PAC-MAN", True, amarillo) 
            pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 250))

        if vidas == 0: #si se queda sin vidas pasa a la pantalla de game over
            estado = "OVER" 

        
        if score == 10000: #si llega a 10mil puntos se le suma una vida
            vidas += 1
            sonido_vida_extra.play() 
        
    elif estado == "OVER":
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT:
                ejecutando = False 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    estado = "MENU"
        pantalla_game(pantalla, score) 

        
    pygame.display.flip()

pygame.draw.rect

