import pygame

class Pacman:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.ancho = 30
        self.alto = 30
        self.velocidad = 5 
        
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto) #crea una "caja" que lo rodea
        self.dir_actual = (0, 0)
        self.dir_deseada = (0, 0)    
    def move(self, lista_paredes):
        """
        lista_paredes: En el main, es necesario que haya un for que lea el mapa y guarde las paredes en una lista
        """
    #asignar un significado a cada tecla que es presionada. (wasd)
    #"recuerda" dónde quiere moverse el usuario, para poder ver si puede o no
        teclas = pygame.key.get_pressed() 
        if teclas [pygame.path.K_a]:
            self.dir_deseada = (-self.velocidad, 0) #izquierda
        if teclas [pygame.path.K_d]:
            self.dir_deseada = (self.velocidad, 0) #derecha
        if teclas [pygame.path.K_w]:
            self.dir_deseada = (0, -self.velocidad) #arriba
        if teclas [pygame.path.K_s]:
            self.dir_deseada = (0, self.velocidad) #abajo
        
        dx_deseado, dy_deseado = self.dir_deseada

        if self.puede_moverse(dx_deseado, dy_deseado, lista_paredes): #si se puede mover a esa casilla, la dirección actual cambia a la deseada. 
            self.dir_actual = self.dir_deseada
        else:
            self.dir_actual = (0, 0)

        self.rect.x = self.x
        self.rect.y = self.y
    
    def chocar_vecino (self, vecino_rect):
        """
        Devuelve True si se choca el vecino indicado, False si no.
        vecino_rect: debe ser un objeto pygame.rect
        """
        return self.rect.colliderect(vecino_rect) #devuelve true si se choca con ese vecino. 
    
    def puede_moverse(self, dx, dy, lista_paredes):
        """
        dx, dy: es el cambio de posición, para saber a qué lado está yendo
        lista_paredes: lista con todas las paredes del mapa
        Retorna True si el camino está libre, False si hay una pared
        """
        #Un "tile" en la posición futura
        rect_futuro = pygame.Rect(self.x + dx, self.y + dy, self.ancho, self.alto)

        for pared in lista_paredes: #revisa todas las paredes del mapa
            if rect_futuro.colliderect(pared.rect):
                return False 
        return True

class Pared: 
    def __init__(self, x, y):
        self.rect = pygame.Rect (x, y, 32, 32)


class Puntuacion: 
    def __init__(self, puntos):
        self.puntos = puntos
    def evaluar_vecinos (self, pacman, vecino_rect):
        vecino = Pacman(pacman, vecino_rect)
        