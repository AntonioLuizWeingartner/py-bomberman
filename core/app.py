import pygame
import pygame.display



class Application:

    """
    Essa classe é um contêiner para todos os outros objetos da aplicação. Ela é responsável por gerenciar e inicializar todos os objetos do jogo.
    """
    
    def __init__(self, display: pygame.Surface):
        self.__display: pygame.Surface = display

    def start(self):
        pass
