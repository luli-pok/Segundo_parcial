from modulos.objetos_del_juego.Personajes import Personaje
from modulos.objetos_del_juego.objeto import Objeto
from modulos.objetos_del_juego.personaje.configuraciones_personajes import reescalar_imagenes, rotar_imagen
from modulos.objetos_del_juego.personaje.heroe import Heroe
import pygame

class Enemigo(Personaje):
    def __init__(self, x, y, tamaño, animaciones, velocidad, screen_width=800):
        super().__init__(x, y, tamaño, animaciones, velocidad)
        self.screen_width = screen_width
        self.moviendo_izquierda = True

    def actualizar(self, pantalla, plataformas, jugador):
        self.manejar_movimiento_horizontal()
        self.aplicar_gravedad(plataformas)
        self.chequear_colision_con_bordes()
        self.chequear_colision_con_jugador(jugador)
        self.animar(pantalla)

    def manejar_movimiento_horizontal(self):
        if self.moviendo_izquierda:
            self.rectangulo_principal.x -= self.velocidad
            self.que_hace = "Izquierda"
            self.animacion_actual = self.animaciones["Izquierda"]
        else:
            self.rectangulo_principal.x += self.velocidad
            self.que_hace = "Derecha"
            self.animacion_actual = self.animaciones["Derecha"]

    def chequear_colision_con_bordes(self):
        if self.rectangulo_principal.left <= 0:
            self.moviendo_izquierda = False
        if self.rectangulo_principal.right >= self.screen_width:
            self.moviendo_izquierda = True

    def chequear_colision_con_jugador(self, jugador):
        # Crear un rectángulo central más pequeño en el rectángulo principal del jugador
        ancho_central = jugador.rectangulo_principal.width // 3  # Un tercio del ancho total
        alto_central = jugador.rectangulo_principal.height // 3  # Un tercio del alto total
        centro_x = jugador.rectangulo_principal.centerx - (ancho_central // 2)
        centro_y = jugador.rectangulo_principal.centery - (alto_central // 2)
        rectangulo_central = pygame.Rect(centro_x, centro_y, ancho_central, alto_central)

        # Verificar la colisión con el rectángulo central
        if self.rectangulo_principal.colliderect(rectangulo_central):
            jugador.perder_vida()
