import pygame
import pygame.display
import core.app
import core.event_system
from typing import Tuple

def create_app(window_size: Tuple[int, int]) -> core.app.Application:
    """
    Esse método cria um objeto do tipo aplicação. Deve ser chamado apenas uma vez, do contrário um erro sera gerado.
    """
    pygame.init()
    display = pygame.display.set_mode(window_size)
    clock = core.app.Clock()
    evt_sys = core.event_system.EventSystem()
    app = core.app.Application(display, clock, evt_sys)
    return app
