import pygame
from modulos.objetos_del_juego.Personajes import Personaje
from modulos.objetos_del_juego.personaje.configuraciones_personajes import reescalar_imagenes

class ObjetoCayendo(Personaje):
    def __init__(self, x, y, tamaño, imagen, velocidad):
        self.animaciones = {"caida": [imagen]}  # Diccionario con la animación de caída
        super().__init__(x, y, tamaño, self.animaciones, velocidad)
        self.en_pantalla = False

    def actualizar(self, pantalla, plataformas):
        if self.en_pantalla:
            self.aplicar_gravedad(plataformas)
            self.animar(pantalla)