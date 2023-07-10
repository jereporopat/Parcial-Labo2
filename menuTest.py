import pygame
import sys
import sqlite3
from buttonClass import Button
from hola import main as start_game
from database import crear_tabla
from database import guardar_datos

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("GALAXIA")


def get_font(size):
    return pygame.font.SysFont("jueguito/imagenes/font.ttf", size, True, (255, 255, 255))


BG = pygame.image.load("jueguito/imagenes/Background.png")


player_name = ""  # Define el nombre del jugador

def database():
    # Establecer la conexión con la base de datos
    conexion = sqlite3.connect("datos_jugadores.db")
    cursor = conexion.cursor()

    # Obtener los registros de la base de datos
    cursor.execute("SELECT * FROM jugadores")
    registros = cursor.fetchall()

    # Mostrar los registros en pantalla
    SCREEN.fill("white")

    # Renderizar y mostrar los registros
    y = 100
    for registro in registros:
        nombre = registro[0]
        numero = registro[1]
        texto = f"Nombre: {nombre}, Score: {numero}"
        texto_renderizado = get_font(30).render(texto, True, "black")
        texto_rect = texto_renderizado.get_rect(center=(640, y))
        SCREEN.blit(texto_renderizado, texto_rect)
        y += 50

    # Cerrar la conexión con la base de datos
    conexion.close()

 # Botón de regreso al menú principal
    back_button = Button(image=pygame.image.load("jueguito/imagenes/Play Rect.png"), pos=(640, 650),
                         text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    back_button.changeColor(pygame.mouse.get_pos())  # Cambiar color del botón si el mouse está encima
    back_button.update(SCREEN)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(pygame.mouse.get_pos()):
                    main_menu()  # Volver al menú principal
                    return

        pygame.display.update()

def main_menu():
    global player_name
    play_game = False  # Bandera para indicar si se debe iniciar el juego
    name_active = False
    database_open = False  # Variable para controlar si la base de datos está abierta o no

    NAME_INPUT_BOX = pygame.Rect(520, 200, 240, 40)
    NAME_COLOR_INACTIVE = pygame.Color('lightskyblue3')
    NAME_COLOR_ACTIVE = pygame.Color('dodgerblue2')

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Galactico", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("jueguito/imagenes/Play Rect.png"), pos=(640, 350),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        DATABASE_BUTTON = Button(image=pygame.image.load("jueguito/imagenes/Options Rect.png"), pos=(640, 500),
                                 text_input="Base de datos", font=get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("jueguito/imagenes/Quit Rect.png"), pos=(640, 650),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, DATABASE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        pygame.draw.rect(SCREEN, NAME_COLOR_ACTIVE if name_active else NAME_COLOR_INACTIVE, NAME_INPUT_BOX, 2)
        name_text = get_font(30).render(player_name, True, "white")
        SCREEN.blit(name_text, (NAME_INPUT_BOX.x + 5, NAME_INPUT_BOX.y + 5))

        if database_open:
            database()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_game = True  # Activar la bandera para iniciar el juego
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if DATABASE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if not database_open:
                        database_open = True
                    else:
                        database_open = False
                if NAME_INPUT_BOX.collidepoint(event.pos):
                    name_active = True
                else:
                    name_active = False
                if play_game:
                    start_game(player_name)  # Llamar a la función principal del juego
                    break  # Salir del bucle principal del menú
            if event.type == pygame.KEYDOWN:
                if name_active:
                    if event.key == pygame.K_RETURN:
                        name_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

        pygame.display.update()


if __name__ == "__main__":   #verifica si el archivo actual está siendo ejecutado
    pygame.init()  # Inicializar pygame
    crear_tabla()  # Crear la tabla "jugadores" en la base de datos
    main_menu()

    pygame.quit()
    sys.exit()