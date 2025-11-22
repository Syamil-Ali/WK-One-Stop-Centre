from nicegui import ui, app


def render_spinner():

    app.storage.tab['main_body'].visible = False

    app.storage.tab['spinner_container'].clear()

    with app.storage.tab['spinner_container']:
        with ui.column().classes('items-center justify-center gap-4'):
            ui.spinner('dots', color='black').style('height: 50vh;').classes('mt-4 text-6xl')


def unrender_spinner():

    app.storage.tab['spinner_container'].clear()

