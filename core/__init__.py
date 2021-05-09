import pygame
import pygame.display
import core.app
import core.event_system
import core.entity_system
from typing import Tuple

def create_app(window_size: Tuple[int, int]) -> core.app.Application:
    """
    Esse método cria um objeto do tipo aplicação. Deve ser chamado apenas uma vez, do contrário um erro sera gerado.
    """
    pygame.init()
    display = pygame.display.set_mode(window_size)
    clock = core.app.Clock()
    evt_sys = core.event_system.EventSystem()
    world = core.entity_system.World()
    timing_data = core.app.TimingData(60)
    img_loader = core.app.ImageLoader()
    app = core.app.Application(display, clock, evt_sys, world, timing_data, img_loader)
    return app
