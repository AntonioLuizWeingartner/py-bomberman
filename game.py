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



tabuleiro = app.world.add_entity()
tabuleiro.add_component(core.core_components.SpriteRenderer)
gg: core.game_components.GameGrid = tabuleiro.add_component(core.game_components.GameGrid)
gg.generate_grid(Vector2(21,21), Vector2(32,32))

agent = app.world.add_entity()
agent.add_component(core.core_components.SpriteRenderer)
agent: core.game_components.GridAgent = agent.add_component(core.game_components.Player)
agent.set_grid(gg, Vector2(0,0))

ai = app.world.add_entity()
ai.add_component(core.core_components.SpriteRenderer)
ai_controller: core.game_components.GridAgent = ai.add_component(core.game_components.AIAgent)
ai_controller.set_grid(gg, Vector2(20,20))
ai_controller.set_player(agent) 

app.start()
