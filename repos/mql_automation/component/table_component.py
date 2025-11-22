from nicegui import ui, events, app, run
from utils.file_manipulation import delete_file, export_file
from repos.mql_automation.component.spinner_component import render_spinner, unrender_spinner
from repos.mql_automation.action import action_pipeline as ap


def start_process_mql():


    app.storage.tab['table_container'].clear()  # Remove old content if any

    # predefined the item
    df_opp = app.storage.tab['excel_sheets_dict']['Opportunity Object']
    df_opp_owner= app.storage.tab['excel_sheets_dict']['User Object']
    df_provider_territories = app.storage.tab['excel_sheets_dict']['WK - Provider Territories']
    df_provider_new_assignment = app.storage.tab['excel_sheets_dict']['WK - Provider Postal Code Data']

    
    render_spinner()
    app.storage.tab['main_file'] = ap.main_pipeline(app.storage.tab['main_file'], df_opp, df_opp_owner, df_provider_territories, df_provider_new_assignment)

    unrender_spinner() # render the spinner

    render_mql_work_table()
    ui.notify('DONE!', type='positive', position='top')

    app.storage.tab['process_button'].visible = False


# Render MQL Table
def render_mql_work_table():
    
    if app.storage.tab['main_file'] is not None:

        # hide the main body
        app.storage.tab['main_body'].visible = False

        with app.storage.tab['table_container']:

            print('table generated here')

            with ui.column().classes('items-center justify-center w-full'):
                # Title
                ui.label('MQL Automation') \
                    .style('font-size: 1.5rem;') \
                    .classes('text-white font-poppins text-6xl normal-case text-center font-bold bg-black p-[0.5rem] rounded-lg mb-2')

            
            # Show File Option
            with ui.row().classes('items-center justify-between w-full px-2 border border-black rounded-lg bg-white'):
                
                ui.label(app.storage.tab['file_name']).classes('text-black font-poppins font-medium normal-case')

                with ui.row().classes('gap-4 gt-sm'):
                    app.storage.tab['process_button'] = ui.button('Process', 
                                                on_click= lambda: start_process_mql()
                                                ).props('flat rounded').classes('text-black font-poppins font-medium normal-case')
                    #process_button.visible = True
                    ui.button('Export', on_click= lambda: export_file(file_type='mql')).props('flat rounded').classes('text-black font-poppins font-medium normal-case')
                    ui.button('Delete', on_click= lambda: delete_file()).props('flat rounded').classes('text-black font-poppins font-medium normal-case')

            # Show Table
            with ui.element('div').classes('w-[85vw] overflow-x-hidden overflow-y-auto max-h-[400px]'):
                ui.table.from_pandas(app.storage.tab['main_file'], pagination={"rowsPerPage": 50}).classes('w-full text-sm text-black').props('dense')


"""
custom table

with ui.element('div').classes('w-[85vw] overflow-x-auto overflow-y-auto max-h-[400px]'):
                table = ui.table.from_pandas(
                    app.storage.tab['main_file'],
                    pagination={"rowsPerPage": 50}
                ).classes('w-full text-sm text-black').props('dense')

                # make browser use fixed table layout so explicit widths are respected
                table.style('table-layout: fixed;')

                # set a fixed width for every header cell so the fixed layout has something to base on
                table.add_slot('header-cell', '''
                    <th :props="props" style="width:200px; max-width:200px; white-space:normal;">
                        {{ props.col.label }}
                    </th>
                ''')

                # wrap content inside a fixed-width block so long text wraps into lines instead of overflowing
                table.add_slot('body-cell', '''
                    <q-td :props="props">
                        <div style="width:200px; max-width:200px; white-space:normal; overflow-wrap:anywhere; word-break:break-word;">
                            {{ props.value }}
                        </div>
                    </q-td>
                ''')
"""