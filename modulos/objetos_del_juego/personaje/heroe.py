import pygame as py
from modulos.objetos_del_juego.personaje.configuraciones_personajes import *
from modulos.objetos_del_juego.Personajes import Personaje

class Heroe(Personaje):
    def __init__(self, x, y, tamaño, animaciones, velocidad):
        super().__init__(x, y, tamaño, animaciones, velocidad)
        self.vidas = 3
        self.saltando = False
        self.velocidad_y = 0  # Inicializar la velocidad vertical
        self.atacando = False
        self.direccion_ataque = ""
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 2000  # 2 segundos de invulnerabilidad
        self.ultimo_daño = 0
        self.tiempo_ataque = 500  # Duración del ataque en milisegundos
        self.ultimo_ataque = 0  # Tiempo del último ataque

    def actualizar(self, pantalla, plataformas, enemigos):
        self.mover()
        self.aplicar_gravedad(plataformas)
        # self.chequear_colision_con_enemigos(enemigos)
        self.animar(pantalla)
        self.gestionar_invulnerabilidad()
        self.gestionar_ataque()  # Gestión del estado de ataque

    def mover(self):
        keys = py.key.get_pressed()
        if not self.atacando:  # Permitir movimiento solo si no está atacando
            if keys[py.K_RIGHT]:
                self.rectangulo_principal.x += self.velocidad
                self.que_hace = "Derecha"
                self.animacion_actual = self.animaciones["Derecha"]
            elif keys[py.K_LEFT]:
                self.rectangulo_principal.x -= self.velocidad
                self.que_hace = "Izquierda"
                self.animacion_actual = self.animaciones["Izquierda"]
            elif keys[py.K_UP] and not self.saltando:
                self.saltando = True
                self.velocidad_y = -15
                self.que_hace = "Salta"
                self.animacion_actual = self.animaciones["Salta"]
            elif not self.saltando:
                self.que_hace = "Quieto"
                self.animacion_actual = self.animaciones["Quieto"]

    def aplicar_gravedad(self, plataformas):
        self.velocidad_y += 1  # Acelerar la caída
        self.rectangulo_principal.y += self.velocidad_y

        # Verificar colisión con las plataformas
        for plataforma in plataformas:
            if self.rectangulo_principal.colliderect(plataforma.rectangulo):
                if self.velocidad_y > 0:  # Solo ajustar si el héroe está cayendo
                    self.rectangulo_principal.bottom = plataforma.rectangulo.top
                    self.saltando = False
                    self.velocidad_y = 0

        # Asegurarse de que el héroe no caiga fuera de la pantalla
        if self.rectangulo_principal.bottom >= 680:
            self.rectangulo_principal.bottom = 680
            self.saltando = False
            self.velocidad_y = 0

    # def chequear_colision_con_enemigos(self, enemigos):
    #     if not self.invulnerable:
    #         for enemigo in enemigos:
    #             if self.rectangulo_principal.colliderect(enemigo.rectangulo_principal):
    #                 print("Colisión detectada con enemigo.")  # Mensaje de depuración
    #                 self.perder_vida()
    #                 break  # Solo perder una vida por colisión

    def atacar(self, direccion):
        self.atacando = True
        self.direccion_ataque = direccion
        self.ultimo_ataque = py.time.get_ticks()  # Tiempo del último ataque
        if direccion == "Derecha":
            self.que_hace = "Ataca_derecha"
            self.animacion_actual = self.animaciones["Ataca_derecha"]
        elif direccion == "Izquierda":
            self.que_hace = "Ataca_izquierda"
            self.animacion_actual = self.animaciones["Ataca_izquierda"]

    def gestionar_ataque(self):
        if self.atacando:
            ahora = py.time.get_ticks()
            if ahora - self.ultimo_ataque > self.tiempo_ataque:
                self.atacando = False  # Terminar el ataque después del tiempo especificado

    def perder_vida(self):
        if not self.invulnerable:  # Verificar si no es invulnerable antes de perder vida
            self.vidas -= 1
            self.invulnerable = True
            self.ultimo_daño = py.time.get_ticks()  # Guardar el tiempo del daño recibido
            print(f"Vida perdida. Vidas restantes: {self.vidas}")  # Mensaje de depuración
            print("Invulnerabilidad activada.")  # Mensaje de depuración

    def gestionar_invulnerabilidad(self):
        if self.invulnerable:
            ahora = py.time.get_ticks()
            if ahora - self.ultimo_daño > self.tiempo_invulnerabilidad:
                self.invulnerable = False
                print("Invulnerabilidad desactivada.")  # Mensaje de depuración
