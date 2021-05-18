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
app.image_loader.create_sprite_sheet("assets/images/player_b.png", "player_b", 4, 7)

app.sound_loader.load_sound("assets/sfx/explosion_0.wav", "explosion")
app.sound_loader.load_sound("assets/sfx/player_death.wav", "player_death")
app.sound_loader.load_sound("assets/sfx/bomb_place.wav", "bomb_place")
app.sound_loader.load_sound("assets/sfx/ai_death.wav", "ai_death")
app.sound_loader.load_sound("assets/sfx/new_highest_score.wav", "score_beat")

game_entity = app.world.add_entity()
game_entity.add_component(core.game_components.GameManager)

app.start()
