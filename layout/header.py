from nicegui import ui


def header():

    with ui.header().style('height: 10vh;').classes('bg-[#FE7743] text-black'):

        with ui.row().classes('items-center justify-between w-full px-6'):
            ui.button('MQL Generator') \
                .props('rounded') \
                .style('color: white;') \
                .classes('font-yellowtail normal-case bg-black')


            with ui.row().classes('gap-4 gt-sm'):
                
                ui.button('Home', on_click=lambda: ui.run_javascript(
                    "document.getElementById('home-top').scrollIntoView({ behavior: 'smooth' });"
                )).props('flat rounded').classes('text-white font-poppins font-medium normal-case')