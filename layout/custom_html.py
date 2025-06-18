from nicegui import ui


def custom_html():
    ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Yellowtail&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&family=Yellowtail&display=swap" rel="stylesheet">
    <link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />
    <link rel="stylesheet" href="https://unicons.iconscout.com/release/v4.0.8/css/line.css">
                    
    <style>
        .font-yellowtail {
            font-family: 'Yellowtail', cursive;
            font-size: .875rem;
        }
        .font-poppins {
            font-family: 'Poppins', sans-serif;
            font-size: .875rem;
        }
                    
        body{
            background-color: #FE7743;
            color: black;
        }
                    
        .q-uploader__list {
            display: none !important;
        }
                    
        .q-uploader__subtitle {
            display: none !important;
        }
                    
    </style>
    ''')