from nicegui import ui
from starlette.formparsers import MultiPartParser
import os

# layout
import layout.custom_html as ch
import layout.header as header

# import page
from mql_automation import main as mam
from opportunity_generator import main as ogm
from pdf_to_table import main as ptt
from ultimate_parent_generator import main as upg



from starlette.formparsers import MultiPartParser
MultiPartParser.spool_max_size = 1024 * 1024 * 512  # 512 MB



@ui.page('/')
async def main_app():


    try:
        await ui.context.client.connected(timeout=60.0) # <<< this line is critical
    except TimeoutError:
        print("Client connection timed out during page render. The browser took too long to connect.")
        ui.notify("Connection failed. Please refresh the page.", type='negative')
        return


    # --- Initialize app.storage.tab variables directly after connection ---

    # Probably add global var here
    # Get today's date as a string

    

    # Add Custom HTML
    ch.custom_html()

    # Header
    header.header()
            

    # Render Process MQL

    #### UI BODY ###
    with ui.element('div').style('height: 90vh;').classes('flex pt-[10vh] justify-center max-w-[800px] w-full mx-auto'):
        with ui.column().classes('items-center w-full gap-4'):

            # Title
            ui.label('WK One Stop Centre') \
                .style('font-size: 1.5rem;') \
                .classes('text-white font-poppins text-6xl normal-case text-center font-bold bg-black p-[0.5rem] rounded-lg mb-2')


            with ui.row().classes('flex-wrap gap-4 justify-center mt-6'):
                with ui.card().tight().classes('bg-[#9400FF] text-white p-4 rounded-lg shadow-md w-[250px] h-[300px] items-center justify-center'):
                    # "1" styled as an icon
                    ui.label('1').classes(
                        'number-circle font-poppins'
                    )
                    ui.label('MQL Automation').classes('text-lg font-semibold font-poppins text-black mt-2 px-4 py-2 w-full text-center')
                    ui.label('Automates the process of compiling and generating lead notes.'
                    ).classes(
                        'text-sm font-poppins text-left mb-4 w-full border-t border-black pt-5'
                    )
                    ui.button(
                        'Go to Page',
                        on_click=lambda: ui.navigate.to('/mql_automation'),
                    ).classes(
                        'mt-auto self-start text-black py-1 font-poppins normal-case border border-black rounded-md bg-orange'
                    ).props('outline')


                with ui.card().tight().classes('bg-[#9400FF] text-white p-4 rounded-lg shadow-md w-[250px] h-[300px] items-center justify-center'):
                    # "1" styled as an icon
                    ui.label('2').classes(
                        'number-circle font-poppins'
                    )
                    ui.label('Opportunity Generator').classes('text-lg font-semibold font-poppins text-black mt-2 px-4 py-2 w-full text-center')
                    ui.label('Generate Opportunity Info from Salesforce using CE-Number'
                    ).classes(
                        'text-sm font-poppins text-left mb-4 w-full border-t border-black pt-5'
                    )
                    ui.button(
                        'Go to Page',
                        on_click=lambda: ui.navigate.to('/opportunity_generator'),
                    ).classes(
                        'mt-auto self-start text-black py-1 font-poppins normal-case border border-black rounded-md bg-orange'
                    ).props('outline')


                with ui.card().tight().classes('bg-[#9400FF] text-white p-4 rounded-lg shadow-md w-[250px] h-[300px] items-center justify-center'):
                    # "1" styled as an icon
                    ui.label('3').classes(
                        'number-circle font-poppins'
                    )
                    ui.label('PDF To Table').classes('text-lg font-semibold font-poppins text-black mt-2 px-4 py-2 w-full text-center')
                    ui.label('Convert PDF Data to Table Format'
                    ).classes(
                        'text-sm font-poppins text-left mb-4 w-full border-t border-black pt-5'
                    )
                    ui.button(
                        'Go to Page',
                        on_click=lambda: ui.navigate.to('/pdf_to_table'),
                    ).classes(
                        'mt-auto self-start text-black py-1 font-poppins normal-case border border-black rounded-md bg-orange'
                    ).props('outline')

                
                with ui.card().tight().classes('bg-[#9400FF] text-white p-4 rounded-lg shadow-md w-[250px] h-[300px] items-center justify-center'):
                    # "1" styled as an icon
                    ui.label('4').classes(
                        'number-circle font-poppins'
                    )
                    ui.label('Ultimate Parent Generator').classes('text-lg font-semibold font-poppins text-black mt-2 px-4 py-2 w-full text-center')
                    ui.label('Generate Ultimate Parent Info from Salesforce using CE-Number'
                    ).classes(
                        'text-sm font-poppins text-left mb-4 w-full border-t border-black pt-5'
                    )
                    ui.button(
                        'Go to Page',
                        on_click=lambda: ui.navigate.to('/ultimate_parent_generator'),
                    ).classes(
                        'mt-auto self-start text-black py-1 font-poppins normal-case border border-black rounded-md bg-orange'
                    ).props('outline')
                    


# Local deploymnet
#ui.run(port=8085, host='0.0.0.0', title='Seniority Classification', reload=False)

# Railway deploymnet
ui.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),  # use Railway's port, fallback to 8080 locally
    title='WK One Stop Centre',
    reload=False,
    reconnect_timeout=300
)
