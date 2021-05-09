from core.math import Vector2
import core
import core.entity_system as es
import core.core_components
import core.game_components
import pygame
app = core.create_app((800, 600), 60)

app.image_loader.load_image("assets/images/wall.png", "wall")
app.image_loader.load_image("assets/images/dirt.jpg", "dirt")



tabuleiro = app.world.add_entity()
tabuleiro.add_component(core.core_components.SpriteRenderer)
gg: core.game_components.GameGrid = tabuleiro.add_component(core.game_components.GameGrid)
gg.generate_grid(Vector2(4,4), Vector2(16,16))

app.start()
