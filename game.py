from core.math import Vector2
import core
import core.app
import core.entity_system as es
import core.core_components
import core.game_components
import pygame
app = core.create_app((1200, 800), 60)

app.image_loader.load_image("assets/images/wall.png", "wall")
app.image_loader.load_image("assets/images/dirt.jpg", "dirt")
app.image_loader.load_image("assets/images/obsidian.png", "ob")
app.image_loader.load_image("assets/images/bomb.png", "bomb")

app.image_loader.create_sprite_sheet("assets/images/explosions.png", "explosions", 4, 7)
app.image_loader.create_sprite_sheet("assets/images/player.gif", "player", 4, 7)

app.sound_loader.load_sound("assets/sfx/explosion_0.wav", "explosion")
app.sound_loader.load_sound("assets/sfx/player_death.wav", "player_death")
app.sound_loader.load_sound("assets/sfx/bomb_place.wav", "bomb_place")
app.sound_loader.load_sound("assets/sfx/ai_death.wav", "ai_death")


"""
tabuleiro = app.world.add_entity()
tabuleiro.add_component(core.core_components.SpriteRenderer)
gg: core.game_components.GameGrid = tabuleiro.add_component(core.game_components.GameGrid)
gg.generate_grid(Vector2(23,23), Vector2(32,32))

agent = app.world.add_entity()
agent.add_component(core.core_components.SpriteRenderer)
agent: core.game_components.GridAgent = agent.add_component(core.game_components.Player)
agent.set_grid(gg, Vector2(0,0))


ai = app.world.add_entity()
ai.add_component(core.core_components.SpriteRenderer)
ai_controller: core.game_components.GridAgent = ai.add_component(core.game_components.AIAgent)
ai_controller.set_grid(gg, Vector2(22, 22))
ai_controller.set_player(agent) 

ai2 = app.world.add_entity()
ai2.add_component(core.core_components.SpriteRenderer)
ai_controller: core.game_components.GridAgent = ai2.add_component(core.game_components.AIAgent)
ai_controller.set_grid(gg, Vector2(22,0))
ai_controller.set_player(agent)

ai2 = app.world.add_entity()
ai2.add_component(core.core_components.SpriteRenderer)
ai_controller: core.game_components.GridAgent = ai2.add_component(core.game_components.AIAgent)
ai_controller.set_grid(gg, Vector2(0,22))
ai_controller.set_player(agent)
"""

#menu code
"""
canvas_entity = app.world.add_entity()
canvas: core.core_components.Canvas = canvas_entity.add_component(core.core_components.Canvas)
play_button = core.core_components.Button(Vector2(600,200), canvas)
play_button.text = "JOGAR"
play_button.foreground_color = (0,200,200,255)
quit_button = core.core_components.Button(Vector2(600, 350), canvas)
quit_button.text = "SAIR"
quit_button.foreground_color = (0, 200, 200, 255)

canvas.add_widget(quit_button)
canvas.add_widget(play_button)
title_widget = core.core_components.Button(Vector2(600, 50), canvas)
canvas.add_widget(title_widget)
title_widget.foreground_color = (0,0,0,0)
title_widget.text = "py-BOMBERMAN"
title_widget.size = (600,300)
title_widget.font_size = 50
"""


game_entity = app.world.add_entity()
game_entity.add_component(core.game_components.GameManager)



app.start()
