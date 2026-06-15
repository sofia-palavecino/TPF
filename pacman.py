import pygame

pacman_abierto = pygame.image.load("pacman_abierto.png")
pacman_cerrado = pygame.image.load("pacman_cerrado.png")

class Pacman:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x 
        self.y = y 
        self.ancho = 22
        self.alto = 22
        self.velocidad = 3 
        
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) #crea una "caja" que lo rodea
        self.dir_actual = (0, 0)
        self.dir_deseada = (0, 0)    
    def move(self, lista_paredes, lista_ghost_house, teclas):
        """
        lista_paredes: En el main, es necesario que haya un for que lea el mapa y guarde las paredes en una lista
        """
    #asignar un significado a cada tecla que es presionada. (wasd)
    #"recuerda" dónde quiere moverse el usuario, para poder ver si puede o no
        ancho_pantalla = 616  
        en_tunel = self.x < 0 or self.x > ancho_pantalla - self.ancho

        if not en_tunel:
            if teclas [pygame.K_a]:
                self.dir_deseada = (-self.velocidad, 0) #izquierda
            if teclas [pygame.K_d]:
                self.dir_deseada = (self.velocidad, 0) #derecha
            if teclas [pygame.K_w]:
                self.dir_deseada = (0, -self.velocidad) #arriba
            if teclas [pygame.K_s]:
                self.dir_deseada = (0, self.velocidad) #abajo
    
        dx_deseado, dy_deseado = self.dir_deseada
        dx_actual, dy_actual = self.dir_actual 
        
        pos_x_original = self.x
        pos_y_original = self.y

        if not en_tunel:
            if dx_deseado != 0 and dy_actual != 0:
                self.y = round(self.y / 22) * 22
            elif dy_deseado != 0 and dx_actual != 0:
                self.x = round(self.x / 22) * 22

        self.rect.x = self.x
        self.rect.y = self.y

        if not en_tunel and self.puede_moverse(dx_deseado, dy_deseado, lista_paredes, lista_ghost_house): #si se puede mover a esa casilla, la dirección actual cambia a la deseada. 
            self.dir_actual = self.dir_deseada
        else:
            self.x = pos_x_original
            self.y = pos_y_original
            self.rect.x = self.x
            self.rect.y = self.y
        
        dx_actual, dy_actual = self.dir_actual 
        if self.puede_moverse(dx_actual, dy_actual, lista_paredes, lista_ghost_house):
            self.x += dx_actual
            self.y += dy_actual 
        else: 
            self.dir_actual = (0, 0)
        #que cruce el tunel y aparezca del otro extremo
        
        if self.x < -22:
            self.x = ancho_pantalla 
            self.dir_deseada = self.dir_actual
        elif self.x > ancho_pantalla:
            self.x = -22
            self.dir_deseada = self.dir_actual

        self.rect.x = self.x
        self.rect.y = self.y 
    
    def puede_moverse(self, dx, dy, lista_paredes, lista_ghost_house_rect):
        """
        dx, dy: es el cambio de posición, para saber a qué lado está yendo
        lista_paredes: lista con todas las paredes del mapa
        Retorna True si el camino está libre, False si hay una pared
        """
        #Un "tile" en la posición futura
        margen = 2
        rect_futuro = pygame.Rect(self.x + dx + (margen // 2), self.y + dy + (margen // 2), self.ancho - margen, self.alto - margen)
        for pared in lista_paredes: #revisa todas las paredes del mapa
            if rect_futuro.colliderect(pared.rect):
                return False 
        for casa_ghost in lista_ghost_house_rect:
            if rect_futuro.colliderect(casa_ghost.rect):
                return False 
        return True
    
    def dibujar_pacman(self, pantalla):
        frame = (pygame.time.get_ticks() // 150) % 2
        sprite = pacman_abierto if frame == 0 else pacman_cerrado
        sprite = pygame.transform.scale(sprite, (self.ancho, self.alto))
        if self.dir_deseada == (-self.velocidad, 0): #si va a la izquierda, rota la imagen 180 grados
            angulo = 180
        elif self.dir_deseada == (0, -self.velocidad):
            angulo = 90
        elif self.dir_deseada == (0, self.velocidad):
            angulo = 270
        else:  
            angulo = 0
        sprite_rotado = pygame.transform.rotate(sprite, angulo)
        pantalla.blit(sprite_rotado, (self.x, self.y))        

    def comer(self, lista_comida):
        punto_comida = 0
        ya_comio = False
        for coord in lista_comida:
            c_x, c_y = coord
            rect_comida = pygame.Rect (c_x, c_y, 22, 22)
            if self.rect.colliderect(rect_comida): #si se choca con la comida, lo borra de la lista, suma puntos y devuelve True
                punto_comida += 10 
                ya_comio = True
                lista_comida.remove(coord) 
        return punto_comida, ya_comio, lista_comida  
    
    def power_pellet (self, lista_power):
        comio_power = False
        punto_power = 0
        for coord in lista_power:
            c_x, c_y = coord
            rect_power = pygame.Rect (c_x, c_y, 22, 22)
            if self.rect.colliderect(rect_power):
                comio_power = True
                punto_power += 50
                lista_power.remove(coord)
        return punto_power, comio_power, lista_power

class Pared: 
    def __init__(self, x, y):
        self.rect = pygame.Rect (x, y, 22, 22)
