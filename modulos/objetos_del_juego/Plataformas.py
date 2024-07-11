import pygame
from modulos.objetos_del_juego.objeto import*
from assets.imagenes.plataformas.plataformas_paths import PLATAFORMA_0

class Plataformas(Objeto):
    def __init__(self, x, y, tamaño, imagen):
        super().__init__(x, y, tamaño, imagen)
        self.superficie = pygame.image.load(imagen)
        self.superficie = pygame.transform.scale(self.superficie, tamaño)
        self.rectangulo = self.superficie.get_rect(topleft=(x, y))
        
    def definir_plataformas(self):
        plataformas = []
        piso = Plataformas(0, 630, (1350, 20), PLATAFORMA_0)
        plataformas.append(piso)
        return plataformas

        
        
        
    