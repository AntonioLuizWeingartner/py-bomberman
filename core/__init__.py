import pygame
import pygame.display
import core.app
from typing import Tuple

def create_app(window_size: Tuple[int, int]) -> core.app.Application:
    """
    Esse método cria um objeto do tipo aplicação. Deve ser chamado apenas uma vez, do contrário um erro sera gerado.
    """
    display = pygame.display(window_size)
    app = core.app.Application(display)
    return app
