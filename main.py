import sys
from ttkbootstrap import Window, PhotoImage, Label, Style, Progressbar, HORIZONTAL
from os import path, system

# Constantes
_THEME_NAME: str = "cyborg"
_HEIGHT: int = 430 #202
_WIDTH: int = 403
_BASE_ROUTE: str = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
_SPLASH_SCREEN_IMAGE_NAME: str = "images\\tkinter_ttkbootstrap_splash_screen.png"
_SPLASH_SCREEN_IMAGE_PATH: str = path.join(_BASE_ROUTE, _SPLASH_SCREEN_IMAGE_NAME) # Esto obtiene la imagen de la pantalla de bienvenida
_VALUE: str = "value"

splash_screen_window: Window = Window(themename=_THEME_NAME)

# Obtiene las dimensiones de la pantalla
screen_width: int = splash_screen_window.winfo_screenwidth()
screen_height: int = splash_screen_window.winfo_screenheight()

# Calcula la posición del centro
x: int = (screen_width // 2) - (_WIDTH // 2)
y: int = (screen_height // 2) - (_HEIGHT // 2)

# Posiciona la ventana en el centro de la pantalla
splash_screen_window.geometry(f"{_WIDTH}x{_HEIGHT}+{x}+{y}")
splash_screen_window.overrideredirect(1) # Eliminamos la barra de título

splash_screen_window.config(background="#2F6C60")

splash_screen_photo_image: PhotoImage = PhotoImage(file=_SPLASH_SCREEN_IMAGE_PATH)
label = Label(splash_screen_window, image=splash_screen_photo_image)
label.place(x=0, y=0, width=403, height=202)

progress_label: Label = Label(splash_screen_window, text="Loading...", font=("Trebuchet Ms", 13, "bold"), foreground="#FFFFFF", background="#2F6C60")
progress_label.place(x=131.5, y=330)

progress: Style = Style()
progress.configure("red.Horizontal.TProgressbar", background="#108CFF")

progress: Progressbar = Progressbar(splash_screen_window, orient=HORIZONTAL, length=400, mode="determinate", style="red.Horizontal.TProgressbar")
progress.place(x=1.5, y=370)

def top():
    splash_screen_window.withdraw()
    # main()
    system(f"python {path.join(_BASE_ROUTE, 'tkinter_experiment.py')}")
    splash_screen_window.destroy()

i = 0

def load():
    global i
    if i <= 10:
        txt = f"Loading... {10 * i}%"
        progress_label.config(text=txt)
        progress_label.after(600, load)
        progress[_VALUE] = 10 * i
        i += 1
    else:
        top()

load()

splash_screen_window.resizable(False, False)
splash_screen_window.mainloop()
