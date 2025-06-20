from nicegui import ui


def header():

    with ui.header().style('height: 10vh;').classes('bg-[#FE7743] text-black'):

        with ui.row().classes('items-center justify-between w-full px-6'):
            ui.button('WK One Stop Center') \
                .props('rounded') \
                .style('color: white;') \
                .classes('font-yellowtail normal-case bg-black')


            with ui.row().classes('gap-4 gt-sm'):
                
                ui.button('Home', on_click=lambda: ui.navigate.to('/')
                ).props('flat rounded').classes('text-white font-poppins font-medium normal-case')

                ui.button('MQL Automation', on_click=lambda: ui.navigate.to('/mql_automation'
                )).props('flat rounded').classes('text-white font-poppins font-medium normal-case')

                ui.button('Opportunity Generator', on_click=''
                ).props('outline rounded').classes('text-black font-poppins font-medium normal-case button-bottom-border')