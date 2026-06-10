import pygame
negro = (0,0,0)
azul = (0,0,255)
blanco = (255, 255, 255)
amarillo = (255, 255, 0)
rosa = (255, 184, 255)
rojo = (255, 0, 0)
verde = (0, 128, 0)
violeta = (128, 0, 128)
gris = (128, 128, 128)


def pantalla_main(pantalla, ancho, tiempo):
    pantalla.fill(negro)
    fuente_titulo = pygame.font.SysFont("comicans", 60, bold = True)
    fuente_subtitulo = pygame.font.SysFont("trebuchetms", 20)
    texto_titulo = fuente_titulo.render("PAC-MAN", True, amarillo) 
    texto_instrucciones = fuente_subtitulo.render("presiona ENTER para comenzar", True, blanco)

    pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 250)) #centrar el texto
    if (tiempo // 500) % 2 == 0: #cada 500ms se cumple, ahí se imprime el texto 
        pantalla.blit (texto_instrucciones, (ancho // 2 - texto_instrucciones.get_width() // 2, 400))
    
def pantalla_fants(pantalla, fants_elegidos, opciones_fants, lista_colores, ind_selecc): 
    pantalla.fill (negro)
    fuente_elegir = pygame.font.SysFont("Courier New", 30, bold = True)
    fuente_fants = pygame.font.SysFont("Courier New", 25, bold = True)
    fuente_fants_d = pygame.font.SysFont("Courier New", 18, bold = True)
    texto_elegir = fuente_elegir.render (f"Elegí los fantasmas: {len(fants_elegidos)}/4", True, amarillo)
    pantalla.blit(texto_elegir, (100, 50))

    texto_inst = fuente_fants_d.render ("flechas para mover opcion -- elegir presione ENTER", True, gris)
    pantalla.blit(texto_inst, (20, 600))
    pos_x = 160
    pos_y = 120

    for i, opcion in enumerate (opciones_fants):
        fantasmas_text = fuente_fants.render (opcion, True, gris)
        descp_text = fuente_fants_d.render (opciones_fants[opcion], True, blanco)
        
        ancho_caja = max(fantasmas_text.get_width(), descp_text.get_width()) + 20 #en vez de usar .rect, como son varios textos, busco el rect de la suma de ambos
        alto_caja = fantasmas_text.get_height() + descp_text.get_height() + 20

        rect_grande = pygame.Rect(pos_x -15, pos_y - 5, ancho_caja, alto_caja)
        
        color_actual = lista_colores[i]
        pygame.draw.circle(pantalla, color_actual, (120, pos_y + 25), 20)

        if i == ind_selecc:
            color_borde = color_actual
            fantasmas_text = fuente_fants.render (opcion, True, amarillo)
            descp_text = fuente_fants_d.render (opciones_fants[opcion], True, amarillo)
        else: 
            color_borde = gris 

        if opcion in fants_elegidos: 
            pygame.draw.rect(pantalla, color_borde, rect_grande, 3)
        
        pantalla.blit(fantasmas_text, (pos_x, pos_y))
        pantalla.blit(descp_text, (pos_x, pos_y + fantasmas_text.get_height()+ 6))
        pos_y += alto_caja + 10 #dar un espacio entre las cajas de las opciones 

def pantalla_game(pantalla, puntaje):
    pantalla.fill(negro)
    fuente_game = pygame.font.SysFont("trebuchetms", 30, bold = True)
    fuente_descp = pygame.font.SysFont("trebuchetms", 20, bold = True)
    text_game = fuente_game.render("GAME OVER", True, rojo)
    text_descp = fuente_descp.render (f"Puntaje final: {puntaje}", True, gris)
    text_descp_1 = fuente_descp.render ("Presione ENTER para volver a la página de inicio", True, gris)
    pantalla.blit(text_game, (150, 200)) 
    pantalla.blit(text_descp, (100, 300))
    pantalla.blit(text_descp_1, (100, 350)) 


