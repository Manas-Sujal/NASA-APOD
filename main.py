import flet as ft
import requests
import datetime

# --- Configuration ---
API_KEY = '9yb8FeuYjrWykZEQaYar7bErsYKLyCt9yBl5edct'
API_URL = 'https://api.nasa.gov/planetary/apod'

def main(page: ft.Page):
    # Window Settings
    page.title = "NASA APOD Explorer"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width=850
    page.window.height=800
    page.scroll = ft.ScrollMode.ALWAYS  # Forces scrollbar to stay on the far right
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0  # CRITICAL: Remove page padding
    page.spacing = 0
    page.update()

    # --- State Variables ---
    today = datetime.datetime.now()

    # --- UI Elements ---
    title_text = ft.Text(value="Discover the Cosmos", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    date_text = ft.Text(value=today.strftime("%Y-%m-%d"), italic=True, color=ft.colors.BLUE_GREY_200)
    
    # Smaller Image Settings
    image_display = ft.Image(
        src="", 
        border_radius=10, 
        height=400, # Fixed height to keep it smaller
        fit=ft.ImageFit.CONTAIN, 
        visible=False
    )
    
    explanation_text = ft.Text(value="", size=15, text_align=ft.TextAlign.JUSTIFY)
    status_text = ft.Text(value="READY", color=ft.colors.WHITE70, weight=ft.FontWeight.W_500)
    
    # Date Picker (Defaulted to Today)
    def handle_date_change(e):
        date_button.text = date_picker.value.strftime("%Y-%m-%d")
        page.update()

    date_picker = ft.DatePicker(
        value=today,
        on_change=handle_date_change,
        first_date=datetime.datetime(1995, 6, 16),
        last_date=today,
    )
    page.overlay.append(date_picker)

    def fetch_data(e):
        fetch_btn.disabled = True
        status_text.value = "📡 FETCHING..."
        page.update()

        try:
            current_date = date_picker.value if date_picker.value else today
            formatted_date = current_date.strftime("%Y-%m-%d")
            
            params = {'api_key': API_KEY, 'date': formatted_date}
            response = requests.get(API_URL, params=params, timeout=10)
            data = response.json()

            title_text.value = data.get("title", "No Title")
            explanation_text.value = data.get("explanation", "")
            date_text.value = f"Captured on: {formatted_date}"
            
            if data.get("media_type") == "image":
                image_display.src = data.get("url")
                image_display.visible = True
            else:
                image_display.visible = False
                explanation_text.value = "[Video Content] " + explanation_text.value

            status_text.value = "✅ SUCCESS"
        except Exception as ex:
            status_text.value = "❌ ERROR"
            explanation_text.value = str(ex)
        
        fetch_btn.disabled = False
        page.update()


    # bar thingy
    input_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row([ 
                    date_button := ft.ElevatedButton(
                        today.strftime("%Y-%m-%d"), 
                        icon=ft.icons.CALENDAR_MONTH, 
                        on_click=lambda _: date_picker.pick_date()
                    ),
                    fetch_btn := ft.ElevatedButton(
                        "Fetch", 
                        bgcolor=ft.colors.BLUE_700,
                        color=ft.colors.WHITE,
                        on_click=fetch_data
                    ),
                ]),
                ft.Container(status_text, padding=ft.padding.only(right=10))
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=ft.colors.SURFACE_VARIANT,
        padding=10,
        border_radius=10,
    )

    # main thing
    app_layout = ft.Container(
        padding=20,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("", size=7),
                ft.Text("NASA APOD Explorer", size=32, weight=ft.FontWeight.W_900, color=ft.colors.BLUE_400),
                ft.Text("", size=10),
                input_bar,
                title_text,
                image_display,
                date_text,
                explanation_text,
            ]
        )
    )

    page.add(app_layout)
    
    # get img immediately
    fetch_data(None)

ft.app(target=main, assets_dir="assets")
