from nicegui import ui
from starlette.formparsers import MultiPartParser
import os
import json

# layout
import layout.custom_html as ch
import layout.header as header

# import page
#from AI_mql_automation import main
from repos.mql_automation import main
from repos.mql_automation_v2 import main
from repos.opportunity_generator import main
from repos.pdf_to_table import main
from repos.ultimate_parent_generator import main



from starlette.formparsers import MultiPartParser
MultiPartParser.spool_max_size = 1024 * 1024 * 512  # 512 MB

# read json file
with open("repo_schema.json") as f:
    data = json.load(f)


def card_generator(item):

    with ui.card().tight().classes('bg-[#9400FF] text-white p-4 rounded-lg shadow-md w-[250px] h-[300px] items-center justify-center'):
        # "1" styled as an icon
        ui.label(item['Number']).classes(
            'number-circle font-poppins'
        )
        ui.label(item['Title']).classes('text-lg font-semibold font-poppins text-black mt-2 px-4 py-2 w-full text-center')
        ui.label(item['Description']
        ).classes(
            'text-sm font-poppins text-left mb-4 w-full border-t border-black pt-5'
        )
        ui.button(
            'Go to Page',
            on_click=lambda: ui.navigate.to(item['URL']),
        ).classes(
            'mt-auto self-start text-black py-1 font-poppins normal-case border border-black rounded-md bg-orange'
        ).props('outline')



@ui.page('/')
async def main_app():


    try:
        await ui.context.client.connected(timeout=60.0) # <<< this line is critical
    except TimeoutError:
        print("Client connection timed out during page render. The browser took too long to connect.")
        ui.notify("Connection failed. Please refresh the page.", type='negative')
        return


    # --- Initialize app.storage.tab variables directly after connection ---

    # Add Custom HTML
    ch.custom_html()

    # Header
    # get the current path
    current_path = ui.context.client.request.url.path
    header.header(current_path)
            

    # Render Process MQL

    #### UI BODY ###
    with ui.element('div').style().classes('flex pt-[10vh] justify-center max-w-[800px] w-full mx-auto'):
        with ui.column().classes('items-center w-full gap-4'):

            # Title
            ui.label('WK One Stop Centre') \
                .style('font-size: 1.5rem;') \
                .classes('text-white font-poppins text-6xl normal-case text-center font-bold bg-black p-[0.5rem] rounded-lg mb-2')


            with ui.row().classes('flex-wrap gap-4 justify-center mt-6'):

                # loop the schema
                for item in data["Repos"]:
                    card_generator(item)
                    



smiley = '''
    <svg width="800px" height="800px" viewBox="-0.04 0 96 96" xmlns="http://www.w3.org/2000/svg">
  <g id="Group_7" data-name="Group 7" transform="translate(-111 -696)">
    <rect id="Rectangle_54" data-name="Rectangle 54" width="14" height="36" transform="translate(181 707)" fill="#5aade0" stroke="#2d4d68" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
    <path id="Path_54" data-name="Path 54" d="M159,709l-36,33v48h72V741Z" fill="#5aade0" stroke="#2d4d68" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
    <rect id="Rectangle_55" data-name="Rectangle 55" width="22" height="25" transform="translate(148 765)" fill="#ebf4f7" stroke="#2d4d68" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
    <rect id="Rectangle_60" data-name="Rectangle 60" width="30" height="10" rx="5" transform="translate(144 755)" fill="#ffffff" stroke="#2d4d68" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
    <rect id="Rectangle_61" data-name="Rectangle 61" width="6" height="6" transform="translate(156 774)" fill="#5aade0"/>
    <path id="Path_55" data-name="Path 55" d="M195,741H123l36-32Z" fill="#ebf4f7" stroke="#2d4d68" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
    <line id="Line_41" data-name="Line 41" y2="8" transform="translate(159 704)" fill="none" stroke="#2d4d68" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
    <line id="Line_42" data-name="Line 42" x1="6" y2="6" transform="translate(147 698)" fill="none" stroke="#2d4d68" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
    <line id="Line_43" data-name="Line 43" x2="6" y2="6" transform="translate(165 698)" fill="none" stroke="#2d4d68" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"/>
  </g>
</svg>
    '''


# Railway deploymnet
ui.run(
    host='0.0.0.0',
    port=int(os.getenv('PORT', 8080)),  # use Railway's port, fallback to 8080 locally
    title='WK One Stop Centre',
    favicon=smiley, #"🚀"
    reload=False,
    reconnect_timeout=300
)

