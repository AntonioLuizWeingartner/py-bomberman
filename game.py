import core
app = core.create_app((800, 600))

tabuleiro = app.world.add_entity()

app.start()
