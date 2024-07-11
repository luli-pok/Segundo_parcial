import pygame
from modulos.objetos_del_juego.objeto import Objeto
from modulos.objetos_del_juego.personaje.configuraciones_personajes import reescalar_imagenes, rotar_imagen

class Personaje(Objeto):
    def __init__(self, x, y, tamaño, animaciones, velocidad, imagen=""):
        super().__init__(x, y, tamaño, imagen)
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, tamaño)
        self.rectangulo_principal = self.animaciones["Quieto"][0].get_rect(topleft=(x, y))
        self.velocidad = velocidad
        self.que_hace = "Quieto"
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["Quieto"]

        self.desplazamiento_y = 0
        self.potencia_salto = -15
        self.limite_velocidad_salto = 15
        self.gravedad = 1
        self.esta_saltando = False

    def actualizar(self, pantalla, plataformas):
        self.manejar_movimiento_horizontal(pantalla)
        self.manejar_salto()
        self.aplicar_gravedad(plataformas)
        self.animar(pantalla)

    def manejar_movimiento_horizontal(self, pantalla):
        if self.que_hace in ["Derecha", "Izquierda"]:
            velocidad_actual = self.velocidad
            if self.que_hace == "Izquierda":
                velocidad_actual *= -1

            nueva_x = self.rectangulo_principal.x + velocidad_actual
            if 0 <= nueva_x <= pantalla.get_width() - self.rectangulo_principal.width:
                self.rectangulo_principal.x += velocidad_actual
                self.animacion_actual = self.animaciones[self.que_hace]
        elif not self.esta_saltando:
            self.animacion_actual = self.animaciones["Quieto"]

    def manejar_salto(self):
        if self.que_hace == "Salta" and not self.esta_saltando:
            self.esta_saltando = True
            self.desplazamiento_y = self.potencia_salto
            self.animacion_actual = self.animaciones["Salta"]

    def animar(self, pantalla):
        largo = len(self.animacion_actual)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0

        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
        self.contador_pasos += 1

    def aplicar_gravedad(self, plataformas):
        self.velocidad_y = 0  # Define velocidad_y aquí
        self.velocidad_y += 1  # Acelerar la caída
        self.rectangulo_principal.y += self.velocidad_y
        if self.esta_saltando:
            self.rectangulo_principal.y += self.desplazamiento_y
            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_salto:
                self.desplazamiento_y += self.gravedad

        for piso in plataformas:
            if self.rectangulo_principal.colliderect(piso.rectangulo):
                self.desplazamiento_y = 0
                self.esta_saltando = False
                self.rectangulo_principal.bottom = piso.rectangulo.top
                break
            else:
                self.esta_saltando = True
