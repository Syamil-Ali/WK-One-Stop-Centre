# function
from nicegui import ui, events, app, run

import repos.pdf_to_table.action.action_pipeline as ap
from repos.pdf_to_table.component.spinner_component import render_spinner, unrender_spinner

from utils import file_manipulation as fm
import requests

async def pdf_upload_handler(event: events.UploadEventArguments):
        
    try:
        render_spinner()

        content = event.content.read()  # Read bytes

        # Do Excel processing outside the handler
        app.storage.tab['main_file'] = await run.io_bound(ap.read_pdf_and_export, content)

        unrender_spinner()

        fm.export_file(file_type='pdf')

        ui.notify('Exported!')

    except:

        ui.notify('Error!')

    unrender_spinner()
    app.storage.tab['upload_component'].reset()
    app.storage.tab['main_body'].visible = True




def pro_upload(
    label: str = "Click or drag .pdf here",
    accept: str = ".pdf",
    max_files: int = 1,
    max_file_size: int = 1_000_000_000,
    on_upload=None,
):
    # Visual dropzone card
    with ui.card().classes(
        'w-full max-w-xl mx-auto rounded-2xl border-2 border-line '
        'border-blue-400 bg-blue-50 shadow-sm transition hover:shadow-md '
        'p-10 flex flex-col items-center justify-center space-y-3'
    ).style('position: relative; overflow: hidden; cursor: pointer;') as card:

        ui.icon('cloud_upload').classes(
            'text-6xl text-blue-500 transition-all duration-300'
        )
        ui.label(label).classes(
            'text-lg font-medium text-blue-700 transition-colors duration-300'
        )
        ui.label(f'Allowed: .pdf • Max 100 MB').classes(
            'text-sm text-blue-400'
        )

        # Add spinner (hidden initially)
        # floating spinner overlay (hidden by default)
        spinner_overlay = ui.column().style(
            'position: absolute; left: 0; top: 0; right: 0; bottom: 0; '
            'display: none; '
            'align-items: center; justify-content: center; '
            'background: rgba(255,255,255,0.78); backdrop-filter: blur(4px); '
            'z-index: 50; padding: 0; margin: 0;' 
            'pointer-events: none;')
        with spinner_overlay:
            ui.spinner(size='lg', color='blue')

        # Transparent uploader
        uploader = ui.upload(
            on_upload=pdf_upload_handler,
            on_rejected=lambda: ui.notify('File rejected'),
            max_file_size=max_file_size,
            max_files=max_files,
            auto_upload=True,
        ).props(f'hide-upload-button accept={accept}')

        uploader.style(
            'position: absolute; inset: 0; width: 100%; height: 100%; '
            'opacity: 0; z-index: 2; cursor: pointer;'
        )

        # Show spinner when uploading starts
        uploader.on('added', lambda e: spinner_overlay.style('display: flex;'))
        # Hide spinner when finished
        uploader.on('uploaded', lambda e: spinner_overlay.style('display: none;'))

        # Clicking anywhere on the card should open the file dialog
        uploader.on('click', lambda e: uploader.run_method('pickFiles'))

        # Dragging feedback
        card.on('dragover', lambda e: card.classes(add='bg-blue-50 border-blue-500'))
        card.on('dragleave', lambda e: card.classes(remove='bg-blue-50 border-blue-500'))
        card.on('drop', lambda e: card.classes(remove='bg-blue-50 border-blue-500'))

    return uploader


# DOWNLOAD PART
def download_pdf(url):

    if 'download=1' not in url:
        if '?' in url:
            url += '&download=1'
        else:
            url += '?download=1'


    resp = requests.get(url, allow_redirects=True)

    if resp.status_code == 200:
        return resp.content
    else:
        print(f'❌ Failed to Download PDF')



# DOWNLOAD AND READ EXCEL
async def pdf_download_handler(input_url):

    try:

        ui.notify('Downloading File..')

        render_spinner()
        content = await run.io_bound(download_pdf, input_url)
        app.storage.tab['file_name'] = 'Download PDF'
        ui.notify('Reading File..')

        app.storage.tab['main_file'] = await run.io_bound(ap.read_pdf_and_export, content)
        unrender_spinner()

        app.storage.tab['main_body'].visible = True
        fm.export_file(file_type='pdf')

        ui.notify('Exported!')  

    except:
        app.storage.tab['main_body'].visible = True # if file has been successfully upload - the upload button set to hidden
        unrender_spinner()
        ui.notify('Error!')