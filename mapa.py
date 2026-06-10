import pygame
pygame.init()

tamaño_bloque = 22

def cargar_mapa(nombre):
    mapa_cargado = []
    try:
        with open(nombre, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    mapa_cargado.append(list(linea))
        return mapa_cargado
    except FileNotFoundError:
        print(f'Error: no se encontró el archivo "{nombre}".')

def verificar_mapa(mapa):
    caracteres_permitidos = {'X', 'P', 'G', 'T', '.', 'o', '-', ' '}
    cuenta_pacman = 0
    cuenta_ghost_house = 0
    
    if len(mapa) != 31:
        raise ValueError('Error: el alto es distinto.')
    
    for num, linea in enumerate(mapa, 1):
        if len(linea) != 28:
            raise ValueError(f'Error en fila {num}: la fila tiene un largo distinto.')
        for caracter in linea:
            if caracter not in caracteres_permitidos:
                raise ValueError(f'Error en la fila {num}: la fila tiene un caracter desconocido "{caracter}".')
            if caracter == 'P':
                cuenta_pacman += 1
            elif caracter == 'G':
                cuenta_ghost_house += 1
    if cuenta_pacman == 0:
        raise ValueError('Error: falta la posición de Pac-Man.')
    elif cuenta_pacman > 1:
        raise ValueError('Error: sólo debe haber una posición de Pac-Man.')
    
    if cuenta_ghost_house == 0:
        raise ValueError('Error: no hay ghost house.')
    
    return mapa

tamaño_bloque = 22
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

def dibujar_mapa(lista_comida, lista_power):
    for i, fila in enumerate(mapa):
        for j, caracter in enumerate(fila):
            x = j * tamaño_bloque
            y = i * tamaño_bloque
            centro_x = x + tamaño_bloque // 2
            centro_y = y + tamaño_bloque // 2

            if caracter == 'X':
                pygame.draw.rect(pantalla, azul, (x, y, tamaño_bloque, tamaño_bloque), 1)
            elif caracter == '.' and (x, y) in lista_comida:
                pygame.draw.circle(pantalla, blanco, (centro_x, centro_y), 2)
            elif caracter == 'o' and (x, y) in lista_power:
                pygame.draw.circle(pantalla, blanco, (centro_x, centro_y), 6)
            elif caracter == 'P':
                mapa [i][j] = ""
            elif caracter == 'G' or caracter == '' or caracter == 'T':
                pygame.draw.rect(pantalla, negro, (x, y, tamaño_bloque, tamaño_bloque), 1)
            elif caracter == '-':
                pygame.draw.line(pantalla, rosa, (x, centro_y), (x + tamaño_bloque, centro_y), 3)
    
