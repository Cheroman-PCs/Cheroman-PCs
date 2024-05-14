import os
import sys
from ttkbootstrap import Window, Toplevel, Label
from typing import Union
from PIL import Image, ImageTk

# Constantes
_THEME_NAME: str = "cyborg"
_APPLICATION_TITLE: str = "Loader"
_BASE_ROUTE: str = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
_LOADER_IMAGE_NAME: str = "icons\\loader.gif"
_LOADER_IMAGE_PATH: str = os.path.join(_BASE_ROUTE, _LOADER_IMAGE_NAME) # Esto obtiene la imagen de la pantalla de bienvenida
_MINIMUM_WINDOW_WIDTH: int = 800
_MINIMUM_WINDOW_HEIGHT: int = 600
_0DISABLED: str = "-disabled"
_MINIMUM_LOADER_TOPLEVEL_WIDTH: int = 200
_MINIMUM_LOADER_TOPLEVEL_HEIGHT: int = 200

# Función que genera la ventana del programa
def generate_window() -> Window:
    """
    Función que genera la ventana del programa
    """
    # Generamos la ventana con un tema específico, un título y unas dimensiones mínimas
    window: Window = Window(themename=_THEME_NAME)
    window_size_placement(window) # Dimensionamos y posicionamos la ventana en la pantalla
    window.title(_APPLICATION_TITLE)
    window.minsize(_MINIMUM_WINDOW_WIDTH, _MINIMUM_WINDOW_HEIGHT)

    # Actualizamos las tareas pendientes de la ventana principal
    window.update_idletasks()

    # Retornamos la ventana del programa
    return window

# Función que dimensiona y posiciona la ventana en la pantalla
def window_size_placement(window: Window) -> None:
    """
    Función que dimensiona y posiciona la ventana en la pantalla
    """
    # Obtiene las dimensiones de la pantalla
    screen_width: int = window.winfo_screenwidth()
    screen_height: int = window.winfo_screenheight()

    # Calcula la posición del centro
    position_top: int = int(screen_height / 2 - _MINIMUM_WINDOW_HEIGHT / 2)
    position_right: int = int(screen_width / 2 - _MINIMUM_WINDOW_WIDTH / 2)

    # Posiciona la ventana en el centro de la pantalla
    window.geometry(f"{_MINIMUM_WINDOW_WIDTH}x{_MINIMUM_WINDOW_HEIGHT}+{position_right}+{position_top}")

# Función que genera el nivel superior
def generate_loader_toplevel(parent: Union[Window, Toplevel]) -> Toplevel:
    """
    Función que genera el nivel superior
    """
    # Generamos el nivel superior con un título y unas dimensiones mínimas
    loader_toplevel: Toplevel = Toplevel(parent)
    loader_toplevel_size_placement(parent, loader_toplevel) # Dimensionamos y posicionamos el nivel superior en la pantalla
    parent.attributes(_0DISABLED, True) # Deshabilitamos la ventana principal
    loader_toplevel.overrideredirect(True) # Eliminamos la barra de título
    loader_toplevel.grab_set() # Hacemos que la ventana sea modal

    # Retornamos el nivel superior
    return loader_toplevel

# Función que dimensiona y posiciona el nivel superior en la pantalla
def loader_toplevel_size_placement(parent: Union[Window, Toplevel], loader_toplevel: Toplevel) -> None:
    """
    Función que dimensiona y posiciona el nivel superior en la pantalla
    """
    # Obtenemos las dimensiones de la ventana principal
    parent_width: int = parent.winfo_width()
    parent_height: int = parent.winfo_height()

    # Obtenemos la posición de la ventana principal
    position_x: int = parent.winfo_x()
    position_y: int = parent.winfo_y()

    # Establecemos las dimensiones del toplevel
    loader_toplevel.geometry(f"{_MINIMUM_LOADER_TOPLEVEL_WIDTH}x{_MINIMUM_LOADER_TOPLEVEL_HEIGHT}")

    # Calculamos la posición de la ventana secundaria
    loader_toplevel.geometry("+%d+%d" % (position_x + (parent_width - _MINIMUM_LOADER_TOPLEVEL_WIDTH) / 2, position_y + (parent_height - _MINIMUM_LOADER_TOPLEVEL_HEIGHT) / 2))

def show_loader(parent: Union[Window, Toplevel], loader_image_path: str) -> Toplevel:
    loader_toplevel: Toplevel = generate_loader_toplevel(parent)

    # Cargar el GIF
    image: Image.Image = Image.open(loader_image_path)
    frames: list[ImageTk.PhotoImage] = [ImageTk.PhotoImage(file=loader_image_path, format="gif -index %i" %(i)) for i in range(image.n_frames)]

    def update(ind):
        if label.winfo_exists(): # Verifica si la etiqueta todavía existe
            frame = frames[ind]
            ind += 1
            if ind == len(frames):
                ind = 0
            label.configure(image=frame)
            parent.after(100, update, ind)

    parent.after(0, update, 0)

    # Crea una etiqueta para mostrar el GIF
    label: Label = Label(loader_toplevel)
    label.pack()

    return loader_toplevel

def hide_loader(parent: Union[Window, Toplevel], loader_toplevel: Toplevel) -> None:
    parent.attributes(_0DISABLED, False) # Habilitamos la ventana principal de nuevo
    loader_toplevel.destroy()
    parent.deiconify()

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Generamos la ventana del programa
    window: Window = generate_window()
    
    # Muestra el loader
    loader_toplevel: Toplevel = show_loader(window, _LOADER_IMAGE_PATH)

    # Programa la destrucción del toplevel después de 5 segundos (5000 milisegundos)
    window.after(5000, hide_loader, window, loader_toplevel)

    # Generamos el hilo que genera la ventana del programa
    window.mainloop()