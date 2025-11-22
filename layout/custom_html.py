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
            background-color: #D0E8F2;
            color: black;
        }
                    
        .q-uploader__list {
            display: none !important;
        }
                    
        .q-uploader__subtitle {
            display: none !important;
        }
                     
        .q-field__control {
            border: none !important;
        }

        .q-field__control::before,
        .q-field__control::after {
            border: none !important;
            background: none !important;
        }
                     

        .button-bordered {
            color: black !important;
            border: 1px solid black;
            background-color: white;
            border-radius: 0.5rem;
            transition: background-color 0.3s, color 0.3s;
        }

        .button-bordered:hover {
            background-color: #1B4965;
            color: white !important;
        }
                     
        .card-rounded {
            border-radius: 20px !important;
        }
                     
        .number-circle {
            width: 48px !important;
            height: 48px !important;
            border-radius: 9999px !important;  /* Fully rounded */
            background-color: white !important;
            color: #9400FF !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-weight: bold !important;
            font-size: 1.125rem !important;  /* ~text-lg */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
            margin-bottom: 0.5rem !important;
        }
                     
        .button-bottom-border {
            border: 1.5px solid black !important;
        }
                    
    </style>
    ''')

