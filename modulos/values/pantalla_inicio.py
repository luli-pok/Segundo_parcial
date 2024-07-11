import pygame as py

from pygame.locals import *

# Asegúrate de tener estas variables definidas
# CORAZON = 'path_to_heart_image.png'
# CIELO_1 = 'path_to_background_image.png'
# PLATAFORMA_0 = 'path_to_platform_image.png'
# Además de las clases Heroe, Enemigo, Plataformas y Configuraciones
def get_path_actual(nombre_archivo: str):
    """encuentra el archivo independientemente de en que path este

    Args:
        nombre_archivo (str): en este parametro se pone el nombre del archivo independientemente
                                de si esta el path o no

    Returns:
        _type_: retorna el nombre del archivo en su path actual 
    """
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

def nuevo_puntaje(nombre:str, puntos:int)->dict:
    puntaje = {}
    puntaje["nombre"] = nombre
    puntaje["puntaje"] = puntos
    return puntaje

def convertir_csv_lista_diccionarios(nombre_archivo: str) -> list:
    try:
        with open(get_path_actual(nombre_archivo), "r", encoding="utf-8") as archivo:
            lista = []
            encabezado = archivo.readline().strip("\n").split(",")
            for linea in archivo.readlines():
                puntuacion = {}
                linea = linea.strip("\n").split(",")
                nombre, puntaje = linea
                lista.append(nuevo_puntaje(nombre, int(puntaje)))
        return lista
    except FileNotFoundError:
        print(f"Archivo {nombre_archivo} no encontrado. Se devolverá una lista vacía.")
        return []
    except Exception as e:
        print(f"Error al leer el archivo {nombre_archivo}: {e}")
        return []

def ordenar_lista(lista: list, campo_1: str, descendente=True) -> None:
    n = len(lista)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if descendente:
                if lista[i][campo_1] < lista[j][campo_1]:
                    lista[i], lista[j] = lista[j], lista[i]
            else:
                if lista[i][campo_1] > lista[j][campo_1]:
                    lista[i], lista[j] = lista[j], lista[i]
class PantallaInicio:
    def __init__(self, pantalla, tamaño):
        self.pantalla = pantalla
        self.tamaño = tamaño
        self.fuente = py.font.Font(None, 74)
        self.fuente_pequeña = py.font.Font(None, 36)
        self.color_texto = (255, 255, 255)
        self.botones = {
            "Play": py.Rect(tamaño[0]//2 - 100, tamaño[1]//2 - 150, 200, 50),
            "Config": py.Rect(tamaño[0]//2 - 100, tamaño[1]//2 - 50, 200, 50),
            "Ranking": py.Rect(tamaño[0]//2 - 100, tamaño[1]//2 + 50, 200, 50)
        }
        self.musica_paused = False

    def mostrar(self):
        self.pantalla.fill((0, 0, 0))  # Pantalla negra
        titulo = self.fuente.render("MiJuego", True, self.color_texto)
        self.pantalla.blit(titulo, (self.tamaño[0]//2 - titulo.get_width()//2, 100))
        
        for texto, rect in self.botones.items():
            py.draw.rect(self.pantalla, (0, 255, 0), rect)
            texto_render = self.fuente_pequeña.render(texto, True, (0, 0, 0))
            self.pantalla.blit(texto_render, (rect.x + (rect.width - texto_render.get_width()) // 2, rect.y + (rect.height - texto_render.get_height()) // 2))

        py.display.flip()

    def manejar_eventos(self, evento):
        if evento.type == MOUSEBUTTONDOWN:
            pos = py.mouse.get_pos()
            if self.botones["Play"].collidepoint(pos):
                return "play"
            elif self.botones["Config"].collidepoint(pos):
                return "config"
            elif self.botones["Ranking"].collidepoint(pos):
                return "ranking"
        return None

class PantallaConfig:
    
    def __init__(self, pantalla, tamaño):
        self.pantalla = pantalla
        self.tamaño = tamaño
        self.fuente_pequeña = py.font.Font(None, 36)
        self.color_texto = (255, 255, 255)
        self.boton_mute = py.Rect(tamaño[0]//2 - 100, tamaño[1]//2 - 50, 200, 50)
        self.musica_paused = False

    def mostrar(self):
        self.pantalla.fill((0, 0, 0))  # Pantalla negra
        py.draw.rect(self.pantalla, (0, 255, 0), self.boton_mute)
        texto_render = self.fuente_pequeña.render("Mute", True, (0, 0, 0))
        self.pantalla.blit(texto_render, (self.boton_mute.x + (self.boton_mute.width - texto_render.get_width()) // 2, self.boton_mute.y + (self.boton_mute.height - texto_render.get_height()) // 2))
        py.display.flip()

    def manejar_eventos(self, evento):
        
        if evento.type == MOUSEBUTTONDOWN:
            pos = py.mouse.get_pos()
            if self.boton_mute.collidepoint(pos):
                self.musica_paused = not self.musica_paused
                if self.musica_paused:
                    py.mixer.music.pause()
                else:
                    py.mixer.music.unpause()
        elif evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                return "inicio"
        return None

class PantallaRanking:
    def __init__(self, pantalla, tamaño):
        self.pantalla = pantalla
        self.tamaño = tamaño
        self.fuente_pequeña = py.font.Font(None, 36)
        self.color_texto = (255, 255, 255)
        self.puntajes = self.leer_puntajes()

    def leer_puntajes(self):
        try:
            puntajes = convertir_csv_lista_diccionarios('puntuaciones.csv')
            ordenar_lista(puntajes, "puntaje", descendente=True)
            return puntajes[:5]  # Solo los 5 mejores puntajes
        except Exception as e:
            print(f"Error al leer los puntajes: {e}")
            return []

    def mostrar(self):
        self.pantalla.fill((0, 0, 0))  # Pantalla negra
        y_offset = 100
        for puntuacion in self.puntajes:
            texto_render = self.fuente_pequeña.render(f"{puntuacion['nombre']}: {puntuacion['puntaje']}", True, self.color_texto)
            self.pantalla.blit(texto_render, (self.tamaño[0]//2 - texto_render.get_width()//2, y_offset))
            y_offset += 50
        py.display.flip()

    def manejar_eventos(self, evento):
        if evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                return "inicio"
        return None