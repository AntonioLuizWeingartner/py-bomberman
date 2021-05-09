import core
import core.entity_system as es
import core.core_components
app = core.create_app((800, 600), 60)

tabuleiro = app.world.add_entity()
tabuleiro.add_component(core.core_components.SpriteRenderer)

app.start()
