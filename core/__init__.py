import pygame
import pygame.display
import core.app
import core.event_system
import core.entity_system
from typing import Tuple

def create_app(window_size: Tuple[int, int], frame_rate = 60) -> core.app.Application:
    """
    Esse método cria um objeto do tipo aplicação. Deve ser chamado apenas uma vez, do contrário um erro sera gerado.
    """
    
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init(channels=32)
    pygame.init()

    display = pygame.display.set_mode(window_size)
    clock = core.app.Clock()
    evt_sys = core.event_system.EventSystem()
    world = core.entity_system.World()
    timing_data = core.app.TimingData(frame_rate)
    img_loader = core.app.ImageLoader()
    keyboard = core.app.Keyboard(evt_sys)
    mouse = core.app.Mouse(evt_sys)
    sound_loader = core.app.SoundLoader()
    app = core.app.Application(display, clock, evt_sys, world, timing_data, img_loader, keyboard, mouse, sound_loader)
    return app
