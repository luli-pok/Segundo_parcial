import pygame as py
from assets.imagenes.objetos_juego.objetos_del_juego import CORAZON, GARRA
from assets.imagenes.fondo.fondos_juego import CIELO_1
from assets.imagenes.plataformas.plataformas_paths import PLATAFORMA_0
from modulos.values.configuraciones_juego import Configuraciones
from modulos.objetos_del_juego.objeto import Objeto
from modulos.objetos_del_juego.Plataformas import Plataformas
from modulos.objetos_del_juego.personaje.heroe import Heroe
from modulos.objetos_del_juego.personaje.enemigo import Enemigo
from modulos.values.game_over import GameOver
from modulos.values.pantalla_inicio import PantallaConfig, PantallaInicio, PantallaRanking
from modulos.objetos_del_juego.personaje.items import ObjetoCayendo
from assets.musica.musica_sonidos import MUSICA_FONDO

class Objeto_Juego(Configuraciones):
    def __init__(self, tamaño, FPS, título="Título", icono=""):
        super().__init__(tamaño, FPS, título, icono)
        self.establecer_plataformas()
        self.establecer_heroe()
        self.establecer_enemigos()
        self.set_background_image(CIELO_1, tamaño)
        self.teclas_presionadas = {
            py.K_RIGHT: False,
            py.K_LEFT: False,
            py.K_UP: False,
            py.K_DOWN: False,
            py.K_SPACE: False
        }
        self.reloj = py.time.Clock()
        self.puntuacion = 0  # Añadir atributo de puntuación
        self.heroe.vidas = 3  # Inicializar las vidas del héroe
        self.corazon_img = Objeto(0, 0, (40, 40), CORAZON).objeto["superficie"]  # Cargar imagen del corazón una vez
        self.tiempo_inicio = py.time.get_ticks()
        # self.iniciar_objeto_cayendo()
        self.set_music(MUSICA_FONDO)
        self.set_volume()
        self.play_music()

    def establecer_heroe(self):
        from modulos.objetos_del_juego.personaje.configuraciones_personajes import velocidad, animaciones
        x, y = 100, 100  # Posición inicial del héroe
        self.heroe = Heroe(x, y, (50, 50), animaciones, velocidad)
        self.heroe.plataformas = self.plataformas  # Asignar plataformas al héroe

    def establecer_enemigos(self):
        self.enemigos = []
        self.tiempo_inicio_enemigos = py.time.get_ticks()
        self.enemigos_por_aparecer = 3
    
    def actualizar_enemigos(self):
        from modulos.objetos_del_juego.personaje.configuraciones_personajes import velocidad, animaciones
        import random
        if py.time.get_ticks() - self.tiempo_inicio_enemigos > 5000:  # Cada 10 segundos
            self.tiempo_inicio_enemigos = py.time.get_ticks()
            for _ in range(self.enemigos_por_aparecer):
                x = random.randint(0, self.tamaño[0] - 50)  # Posición x aleatoria
                y = 0  # Posición y desde el punto más alto de la pantalla
                enemigo = Enemigo(x, y, (50, 50), animaciones, velocidad, self.tamaño[0])
                self.enemigos.append(enemigo)

    def establecer_plataformas(self):
        self.plataformas = []
        plataforma1 = Plataformas(0, 630, (1350, 20), PLATAFORMA_0)
        self.plataformas.append(plataforma1)
    
    # def iniciar_objeto_cayendo(self):
    #     from modulos.objetos_del_juego.personaje.configuraciones_personajes import velocidad, animaciones
    #     x, y = 400, -50  # Posición inicial del objeto cayendo
    #     self.objeto_cayendo = ObjetoCayendo(x, y, (50, 50), CORAZON, velocidad)
    #     self.objeto_cayendo.en_pantalla = False

    def manejar_comportamiento_heroe(self):
        if self.teclas_presionadas[py.K_RIGHT]:
            self.heroe.que_hace = "Derecha"
        elif self.teclas_presionadas[py.K_LEFT]:
            self.heroe.que_hace = "Izquierda"
        else:
            self.heroe.que_hace = "Quieto"

        if self.teclas_presionadas[py.K_UP]:
            self.heroe.que_hace = "Salta"

        self.heroe.actualizar(self.pantalla, self.plataformas, self.enemigos)
        self.eliminar_enemigos_atacados()  # Eliminar enemigos atacados

    def manejar_comportamiento_enemigos(self):
        for enemigo in self.enemigos:
            enemigo.actualizar(self.pantalla, self.plataformas, self.heroe)

    def manejar_ataque_heroe(self, x_click, y_click):
        centro_x_heroe = self.heroe.rectangulo_principal.centerx
        if x_click > centro_x_heroe:
            self.heroe.atacar("Derecha")
        else:
            self.heroe.atacar("Izquierda")
    
    # def manejar_comportamiento_objeto_cayendo(self):
    #     if py.time.get_ticks() - self.tiempo_inicio > 30000:
    #         self.objeto_cayendo.en_pantalla = True
    #     self.objeto_cayendo.actualizar(self.pantalla, self.plataformas)

    def mostrar_plataformas(self, pantalla):
        for plataforma in self.plataformas:
            pantalla.blit(plataforma.superficie, plataforma.rectangulo)

    def eliminar_enemigos_atacados(self):
        for enemigo in self.enemigos[:]:
            if self.heroe.atacando:
                if self.heroe.direccion_ataque == "Derecha" and self.heroe.rectangulo_principal.colliderect(enemigo.rectangulo_principal):
                    self.enemigos.remove(enemigo)
                    self.puntuacion += 100  # Incrementar la puntuación
                elif self.heroe.direccion_ataque == "Izquierda" and self.heroe.rectangulo_principal.colliderect(enemigo.rectangulo_principal):
                    self.enemigos.remove(enemigo)
                    self.puntuacion += 100  # Incrementar la puntuación

    def mostrar_puntuacion(self):
        fuente = py.font.Font(None, 36)  # Fuente y tamaño de la fuente
        texto_puntuacion = fuente.render(f"Puntuación: {self.puntuacion}", True, (0, 255, 255))
        self.pantalla.blit(texto_puntuacion, (10, 10))  # Posición del texto en la pantalla
    
    def mostrar_vidas(self):
        posicion_vida_x, posicion_vida_y = 500, 20
        for vida in range(self.heroe.vidas):
            self.pantalla.blit(self.corazon_img, (posicion_vida_x, posicion_vida_y))
            posicion_vida_x += 50

    def init(self):
        pantalla_inicio = PantallaInicio(self.pantalla, self.tamaño)
        pantalla_config = PantallaConfig(self.pantalla, self.tamaño)
        pantalla_ranking = PantallaRanking(self.pantalla, self.tamaño)

        estado = "inicio"
        self.juego_activo = True

        while self.juego_activo:
            if estado == "inicio":
                pantalla_inicio.mostrar()
                for evento in py.event.get():
                    if evento.type == py.QUIT:
                        self.juego_activo = False
                    accion = pantalla_inicio.manejar_eventos(evento)
                    if accion == "play":
                        estado = "juego"
                    elif accion == "config":
                        estado = "config"
                    elif accion == "ranking":
                        estado = "ranking"

            elif estado == "config":
                pantalla_config.mostrar()
                for evento in py.event.get():
                    if evento.type == py.QUIT:
                        self.juego_activo = False
                    accion = pantalla_config.manejar_eventos(evento)
                    if accion == "inicio":
                        estado = "inicio"

            elif estado == "ranking":
                pantalla_ranking.mostrar()
                for evento in py.event.get():
                    if evento.type == py.QUIT:
                        self.juego_activo = False
                    accion = pantalla_ranking.manejar_eventos(evento)
                    if accion == "inicio":
                        estado = "inicio"

            elif estado == "juego":
                self.pantalla.blit(self.fondo, (0, 0))
                for evento in py.event.get():
                    if evento.type == py.QUIT:
                        self.juego_activo = False
                    if evento.type == py.KEYDOWN:
                        if evento.key in self.teclas_presionadas:
                            self.teclas_presionadas[evento.key] = True
                    if evento.type == py.KEYUP:
                        if evento.key in self.teclas_presionadas:
                            self.teclas_presionadas[evento.key] = False
                    if evento.type == py.MOUSEBUTTONDOWN:
                        if evento.button == 1:  # Click izquierdo
                            x_click, y_click = evento.pos
                            self.manejar_ataque_heroe(x_click, y_click)

                self.mostrar_plataformas(self.pantalla)
                self.manejar_comportamiento_heroe()
                self.manejar_comportamiento_enemigos()
                self.actualizar_enemigos()
                self.mostrar_puntuacion()  # Mostrar la puntuación
                self.mostrar_vidas()  # Mostrar las vidas
                # self.manejar_comportamiento_objeto_cayendo()  # Manejar el objeto cayendo
                
                if self.heroe.vidas <= 0:
                    estado = "gameover"
                    game_over_screen = GameOver(self.pantalla, self.puntuacion)
                    game_over_screen.ejecutar()

                py.display.update()
                self.reloj.tick(self.FPS)

        py.quit()                                     