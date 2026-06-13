import pygame
from pacman import Pared, Pacman
from mapa import cargar_mapa, verificar_mapa, dibujar_mapa
from pantallas import pantalla_main, pantalla_fants, pantalla_game, margen_mapa, pantalla_esquina, pantalla_aprender, pantalla_preparado
from fantasmas import Pinky, Blinky
pygame.init() 
pygame.mixer.init() 

lista_paredes = []
lista_ghost_house = []
lista_ghost_house_rect = [] #para que pacman no pueda pasar 
lista_comida = []
lista_comida_orig = [] #para guardar la comida del mapa original y poder regenerarla en el siguiente nivel
lista_power = []
lista_power_orig = []
lista_fants = [] #falta ver cómo obtener las coordenadas de los fantasmas en una lista, para saber dónde están y ver si se lo chocan a pacman
dicc_fantasmas = {} # TENGO QUE VER COMO CREARLO Y INSERTARLE LAS COORDENANDAS Y EL MODO ACTUAL DE CADA FANTASMA
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
            elif caracter == "G":
                lista_ghost_house.append((columna, fila))
                pared_ghost = Pared (x, y)
                lista_ghost_house_rect.append (pared_ghost)
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
sonido_intro.set_volume(0.3)
sonido_muerte_fants = pygame.mixer.Sound("muerte_fants.mp3")
sonido_muerte_pacman = pygame.mixer.Sound ("muerte_pacman.mp3") #falta agregarlo a cuando muere
sonido_nivel = pygame.mixer.Sound ("nivel.mp3")
sonido_vida_extra = pygame.mixer.Sound ("vida_extra.mp3")
sonido_select = pygame.mixer.Sound ("select.mp3") 
sonido_denied = pygame.mixer.Sound ("denied.mp3")

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
puntos_fantasmas_escala = [200, 400, 800, 1600] 
fantasmas_comidos_en_racha = 0
ya_recibio_vida_extra = False
#pantalla fantasmas: 
opciones_fants = {"Blinky": "el que persigue", "Pinky" : "el que", "Inky": "el que", "Clyde": "el que", "Coward": "el que", "Spyke": "el que"}
claves_fants = list(opciones_fants.keys()) #mantener los nombres como una lista facilita al momento de saber en qué opción está el usuario
lista_colores = [rojo, rosa, azul, verde, violeta, blanco]
colores_fants = dict(zip(claves_fants, lista_colores)) #creo un diccionarios con los nombres de los fantasmas y sus colores 
esquinas_elegidas = {} #luego queda con el nombre del fantasma de clave y el valor es dónde se va a posicionar. ej: pinky: superior izquierda. 
opciones_esquina = ["Superior izquierda", "Superior derecha", "Inferior izquierda", "Inferior derecha"]
coordenadas_esquinas = {
    "Superior izquierda": (1, 1),
    "Superior derecha": (len(mapa[0]) - 2, 1),
    "Inferior izquierda": (1, len(mapa) - 2),
    "Inferior derecha": (len(mapa[0]) - 2, len(mapa) - 2)
}
ind_selecc = 0
ind_fant = 0
fantasma_actual = claves_fants[ind_selecc]
fants_elegidos = []
opciones_modo = ["Modo Normal", "Modo Aprender"]
ind_modo = 0
#modo asustado
modo_asustado = False
duracion_susto = 6000 #6 segundos
tiempo_susto = 0
fantasmas_comidos = 0
# variables para fantasmas
tiempo_fase_inicio = 0
indice_fase_actual = 0 
fase_actual = 1 # 1: Scatter (7s), 2: Chase(20s), 3: Scatter(7s), etc.
tabla_fases = [
    {"modo": "Scatter", "duracion": 7.0},
    {"modo": "Chase", "duracion": 20.0},
    {"modo": "Scatter", "duracion": 7.0},
    {"modo": "Chase", "duracion": 20.0},
    {"modo": "Scatter", "duracion": 5.0},
    {"modo": "Chase", "duracion": 20.0},
    {"modo": "Scatter", "duracion": 5.0},
    {"modo": "Chase", "duracion": float('inf')}
]
fantasmas_inicializados = False

def reiniciar_juego(): # funcion para cargar todos los datos de cero
    global score, vidas, nivel, lista_comida, lista_power, fants_elegidos
    global esquinas_elegidas, ind_fant, modo_asustado, tiempo_susto
    global tiempo_fase_inicio, indice_fase_actual, fase_actual, fantasmas_inicializados
    global lista_fants, puntos_fantasmas_escala, ya_recibio_vida_extra, ind_selecc
    
    fants_elegidos = []        
    esquinas_elegidas = {}     
    ind_fant = 0               
    ind_selecc = 0           
    score = 0
    vidas = 3 
    nivel = 1
    modo_asustado = False
    tiempo_susto = 0
    ya_recibio_vida_extra = False
    puntos_fantasmas_escala = [200, 400, 800, 1600]
    
    lista_comida = list(lista_comida_orig)
    lista_power = list(lista_power_orig)
    
    pacman_personaje.x = pacman_x
    pacman_personaje.y = pacman_y
    pacman_personaje.rect.x = pacman_x
    pacman_personaje.rect.y = pacman_y
    pacman_personaje.dir_actual = (0, 0)
    pacman_personaje.dir_deseada = (0, 0)
    
    lista_fants = []
    
    for i, nombre_f in enumerate(fants_elegidos):
        esquina_texto = esquinas_elegidas[nombre_f]
        tile_esquina_real = coordenadas_esquinas[esquina_texto]

        g_col, g_fil = lista_ghost_house[i % len(lista_ghost_house)]

        if nombre_f == 'Blinky':
            nuevo_fant = Blinky(g_col, g_fil, tile_esquina_real)
        elif nombre_f == 'Pinky':
            nuevo_fant = Pinky(g_col, g_fil, tile_esquina_real)
        else:
            continue

        nuevo_fant.px = g_col * tamaño_bloque
        nuevo_fant.py = g_fil * tamaño_bloque
        nuevo_fant.direccion_actual = "IZQUIERDA"

        nuevo_fant.activo = True if i == 0 else False
        nuevo_fant.orden_salida = i
        nuevo_fant.modo = "Scatter"
        nuevo_fant.velocidad_actual = nuevo_fant.velocidades_dict[nuevo_fant.modo]

        lista_fants.append(nuevo_fant)

    tiempo_fase_inicio = pygame.time.get_ticks()
    indice_fase_actual = 0
    fase_actual = 1
    fantasmas_inicializados = True

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
                    esq_elegida = opciones_esquina[teclas_num[evento.key]]
                    if esq_elegida not in esquinas_elegidas.values(): 
                        esquinas_elegidas[fantasma_actual] = esq_elegida
                        ind_fant += 1
                        sonido_select.play() 
                        if ind_fant >= len (fants_elegidos):
                            lista_fants = []

                            for i, nombre_f in enumerate(fants_elegidos):
                                esquina_texto = esquinas_elegidas[nombre_f]
                                tile_esquina_real = coordenadas_esquinas[esquina_texto]
                                
                                g_col, g_fil = lista_ghost_house[i % len(lista_ghost_house)]

                                if nombre_f == 'Blinky':
                                    nuevo_fant = Blinky(g_col, g_fil, tile_esquina_real)
                                elif nombre_f == 'Pinky':
                                    nuevo_fant = Pinky(g_col, g_fil, tile_esquina_real)
                                
                                nuevo_fant.activo = True if i == 0 else False
                                nuevo_fant.orden_salida = i
                                
                                if nombre_f in ['Blinky', 'Pinky']:
                                    lista_fants.append(nuevo_fant)
                            
                            tiempo_fase_inicio = pygame.time.get_ticks()
                            fase_actual = 1
                            estado = "MODO"
                    else:
                        sonido_denied.play() 
                        pass 

        pantalla_esquina(pantalla, fantasma_actual, fants_elegidos, ind_fant, colores_fants, opciones_esquina, esquinas_elegidas)
    
    elif estado == "MODO": 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    ind_modo += 1
                    if ind_modo >= len(opciones_modo):
                        ind_modo = 0
                elif evento.key == pygame.K_UP:
                    ind_modo -= 1
                    if ind_modo < 0:
                        ind_modo = len(opciones_modo) - 1
                elif evento.key == pygame.K_RETURN:
                    estado = "PREPARADO"
                    tiempo_pantalla = pygame.time.get_ticks()
                    if ind_modo == 0:
                        modo_juego = "NORMAL"
                    else:
                        modo_juego = "APRENDER" #para luego cambiar lo necesario en el turno. 
        pantalla_aprender(pantalla, opciones_modo, ind_modo)
    
    elif estado == "PREPARADO": 
        pantalla_preparado(pantalla)
        if pygame.time.get_ticks() - tiempo_pantalla >= 1000: 
            estado = "JUEGO"

    elif estado == "JUEGO": 
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        
        pantalla.fill(negro)
        dibujar_mapa(lista_comida, lista_power)
        margen_mapa(pantalla, score, nivel, high_score, vidas) 

        teclas = pygame.key.get_pressed()
        pacman_personaje.move(lista_paredes, lista_ghost_house_rect, teclas)
        pacman_personaje.dibujar_pacman(pantalla)
        pacman_tile_x = int(pacman_personaje.x // tamaño_bloque)
        pacman_tile_y = int(pacman_personaje.y // tamaño_bloque)
        pacman_tile = (pacman_tile_x, pacman_tile_y)
        # traduzco la velocidad de píxeles a dirección cartesiana para Pinky/Inky
        p_dx = 1 if pacman_personaje. dir_actual[0] > 0 else (-1 if pacman_personaje.dir_actual[0] < 0 else 0)
        p_dy = 1 if pacman_personaje.dir_actual[1] > 0 else (-1 if pacman_personaje.dir_actual[1] < 0 else 0)
        pacman_dir_matriz = (p_dx, p_dy)

        punto_comida, ya_comio, lista_comida = pacman_personaje.comer(lista_comida)
        if ya_comio: 
            sonido_comer.play() 
        punto_power, comio_power, lista_power = pacman_personaje.power_pellet(lista_power)
        if comio_power:
            sonido_power.play()
            modo_asustado = True # si comio power pellet se activa el modo asustado 
            tiempo_susto = pygame.time.get_ticks()
            fantasmas_comidos_en_racha = 0
            for f in lista_fants:
                f.cambiar_modo("Asustado")
        score += punto_comida
        score += punto_power

        if not modo_asustado:
            tiempo_en_fase = (pygame.time.get_ticks() - tiempo_fase_inicio) / 1000.0 # para calcular los segundos que pasaron desde que inció la fase actual
            fase_actual_info = tabla_fases[indice_fase_actual]

            if tiempo_en_fase >= fase_actual_info["duracion"]:
                if indice_fase_actual < len(tabla_fases) - 1:
                    indice_fase_actual += 1
                    tiempo_fase_inicio = pygame.time.get_ticks()
                    nuevo_modo = tabla_fases[indice_fase_actual]["modo"]
                    
                    for f in lista_fants:
                        f.cambiar_modo(nuevo_modo)

        if modo_asustado: 
            tiempo_restante = duracion_susto - (pygame.time.get_ticks() - tiempo_susto)
            if tiempo_restante < 2000:
                if (pygame.time.get_ticks() // 200) % 2 == 0:
                    pygame.draw.rect(pantalla, negro, (pacman_personaje.x, pacman_personaje.y, 22, 22))#parpadea en los últimos dos segundos del modo asustado
            if pygame.time.get_ticks() - tiempo_susto >= duracion_susto:
                modo_asustado = False
                fantasmas_comidos_en_racha = 0
                modo_interrumpido = tabla_fases[indice_fase_actual]["modo"]
                for f in lista_fants:
                    f.cambiar_modo(modo_interrumpido)
                pacman_personaje.velocidad * 0.8 #velocidad normal
                tiempo_fase_inicio += duracion_susto
            else: 
                pacman_personaje.velocidad * 0.9 
        dot_comidos = len(lista_comida_orig) - len(lista_comida)

        for f in lista_fants:
            if not f.activo:
                if f.orden_salida == 1 and dot_comidos >= 30:
                    f.activo = True
                elif f.orden_salida == 2 and dot_comidos >= 60:
                    f.activo = True
                elif f.orden_salida == 3 and dot_comidos >= 90:
                    f.activo = True
            if not f.activo:
                f.dibujar(pantalla)
                continue

            if int(f.px) % tamaño_bloque < f.velocidad_actual and int(f.py) % tamaño_bloque < f.velocidad_actual: # verifico que esté alineado a una celda
                f.px = f.x * tamaño_bloque
                f.py = f.y * tamaño_bloque
                f.actualizar_objetivo(pacman_tile, pacman_dir_matriz)
                f.decidir_sig_direccion(mapa)
            
            f.actualizar_posicion(mapa)
            f.dibujar(pantalla)

            rect_fantasma_actual = pygame.Rect(f.px, f.py, tamaño_bloque, tamaño_bloque)

            if pacman_personaje.rect.colliderect(rect_fantasma_actual):
                if f.modo == "Asustado":
                    sonido_muerte_fants.play()
                    indice_puntos = min(fantasmas_comidos_en_racha, 3)
                    puntos_obtenidos = puntos_fantasmas_escala[indice_puntos]
                    score += puntos_obtenidos
                    fantasmas_comidos_en_racha += 1
                    f.cambiar_modo("Ojos")
                elif f.modo != "Ojos":
                    sonido_muerte_pacman.play()
                    vidas -= 1
                    pacman_personaje.x = pacman_x
                    pacman_personaje.y = pacman_y
                    pacman_personaje.dir_actual = (0, 0)
                    pacman_personaje.dir_deseada = (0, 0)

                    for i, fant in enumerate(lista_fants):
                        g_col, g_fil = lista_ghost_house[i % len(lista_ghost_house)]
                        fant.x = g_col
                        fant.y = g_fil
                        fant.px = g_col * tamaño_bloque
                        fant.py = g_fil * tamaño_bloque
                        fant.direccion_actual = "IZQUIERDA"
                        fant.cambiar_modo("Scatter")
                        fant.activo = True if i == 0 else False
                    
                    pygame.time.delay(1000)
                    break
                
        if len(lista_comida) == 0: #si se termina la comida, avanza un nivel
            nivel += 1
            sonido_nivel.play() 
            lista_comida = list(lista_comida_orig) #que se regenere la comida del mapa original
            lista_power = list(lista_power_orig)
            tiempo_fase_inicio = pygame.time.get_ticks()
            fase_actual = 1 
            fuente_titulo = pygame.font.SysFont("comicans", 60, bold = True)
            texto_titulo = fuente_titulo.render("PAC-MAN", True, amarillo) 
            pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 250)) 

        if vidas == 0: #si se queda sin vidas pasa a la pantalla de game over
            estado = "OVER" 

        if score >= 10000 and not ya_recibio_vida_extra: # si llega a 10mil puntos se le suma una vida
            vidas += 1
            ya_recibio_vida_extra = True 
            sonido_vida_extra.play() 
    
    elif estado == "OVER":
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT:
                ejecutando = False 
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    reiniciar_juego()
                    estado = "MENU"

        pantalla_game(pantalla, score) 

        
    pygame.display.flip()

pygame.draw.rect 