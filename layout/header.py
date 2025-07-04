from nicegui import ui

def header(current_path: str):
    
    with ui.header().style('height: 10vh;').classes('bg-[#FE7743] text-black'):
        with ui.row().classes('items-center justify-between w-full px-6'):
            ui.button('WK One Stop Center') \
                .props('rounded') \
                .style('color: white;') \
                .classes('font-yellowtail normal-case bg-black')

            def nav_button(label: str, path: str):
                is_active = current_path == path
                style_class = 'button-bottom-border text-black' if is_active else 'text-white'
                props = 'outline rounded' if is_active else 'flat rounded'

                ui.button(label,
                          on_click=None if is_active else lambda p=path: ui.navigate.to(p)
                          ).props(props).classes(f'font-poppins font-medium normal-case {style_class}')

            with ui.row().classes('gap-4 flex-wrap'):
                nav_button('Home', '/')
                nav_button('MQL Automation', '/mql_automation')
                nav_button('Opportunity Generator', '/opportunity_generator')
                nav_button('PDF to Table', '/pdf_to_table')
                nav_button('Ultimate Parent Generator', '/ultimate_parent_generator')
