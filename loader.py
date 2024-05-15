import sys
import os
from ttkbootstrap import Window, Toplevel, Label, TOP, Button, PhotoImage
from typing import Union
from PIL import Image
from tkinter import messagebox
import time
from threading import Thread

# Constantes
_THEME_NAME: str = "cyborg"
_APPLICATION_TITLE: str = "Loader"
_MINIMUM_WINDOW_WIDTH: int = 800
_MINIMUM_WINDOW_HEIGHT: int = 600
_BASE_ROUTE: str = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
_LOADER_IMAGE_NAME: str = "icons\\loader.gif"
_LOADER_IMAGE_PATH: str = os.path.join(_BASE_ROUTE, _LOADER_IMAGE_NAME) # Esto obtiene la imagen del loader
_0ALPHA: str = "-alpha"
_0DISABLED: str = "-disabled"

# Función que genera la ventana del programa
def _generate_window() -> Window:
    """
    Función que genera la ventana del programa
    """
    # Generamos la ventana con un tema específico, un título y unas dimensiones mínimas
    window: Window = Window(themename=_THEME_NAME)
    window.title(_APPLICATION_TITLE)
    window.minsize(_MINIMUM_WINDOW_WIDTH, _MINIMUM_WINDOW_HEIGHT)
    window.configure(bg="red")
    _window_size_placement(window) # Dimensionamos y posicionamos la ventana en la pantalla

    # Actualizamos las tareas pendientes de la ventana principal
    window.update_idletasks()

    # Retornamos la ventana del programa
    return window

# Función que dimensiona y posiciona la ventana en la pantalla
def _window_size_placement(window: Window) -> None:
    """
    Función que dimensiona y posiciona la ventana en la pantalla
    """
    # Dimensiona la ventana
    window.geometry(f"{_MINIMUM_WINDOW_WIDTH}x{_MINIMUM_WINDOW_HEIGHT}")
    
    # Posiciona la ventana en el centro de la pantalla
    window.place_window_center()

# Función que genera el nivel superior
def _generate_loader_toplevel(parent: Union[Window, Toplevel]) -> Toplevel:
    """
    Función que genera el nivel superior
    """
    # Generamos el nivel superior con un título y unas dimensiones mínimas
    loader_toplevel: Toplevel = Toplevel(parent)
    loader_toplevel.attributes(_0ALPHA, 0.5) # Ajusta la transparencia del toplevel a semi-transparente
    parent.attributes(_0DISABLED, True) # Deshabilitamos la ventana principal
    loader_toplevel.overrideredirect(True) # Eliminamos la barra de título
    loader_toplevel.focus_force() # Forzamos el foco
    loader_toplevel.grab_set() # Hacemos que la ventana sea modal
    _loader_toplevel_size_placement(parent, loader_toplevel) # Dimensionamos y posicionamos el nivel superior en la pantalla

    # Retornamos el nivel superior
    return loader_toplevel

# Función que dimensiona y posiciona el nivel superior en la pantalla
def _loader_toplevel_size_placement(parent: Union[Window, Toplevel], loader_toplevel: Toplevel) -> None:
    """
    Función que dimensiona y posiciona el nivel superior en la pantalla
    """
    # Obtenemos las dimensiones de la ventana principal
    parent_width: int = parent.winfo_width()
    parent_height: int = parent.winfo_height()

    # Obtenemos la posición de la ventana principal
    position_x: int = parent.winfo_x()
    position_y: int = parent.winfo_y()

    # Establecemos las dimensiones del toplevel y lo centramos
    loader_toplevel.geometry(f"{parent_width}x{parent_height}+{position_x + 8}+{position_y + 31}") # Dimensiones del toplevel y la centramosTODA LA VENTANA SIN LA BARRA DE TÍTULO NI LOS BORDES
    # loader_toplevel.geometry(f"{parent_width + 2}x{parent_height + 32}+{position_x + 7}+{position_y}") # TODA LA VENTANA

# Función que muestra el loader
def show_loader(parent: Union[Window, Toplevel], loader_image_path: str) -> Toplevel:
    """
    Función que muestra el loader
    """
    # Crear un Toplevel
    loader_toplevel: Toplevel = _generate_loader_toplevel(parent)
    
    # Cargar la imagen .gif
    image: Image.Image = Image.open(loader_image_path)
    frames: list[PhotoImage] = [PhotoImage(file=loader_image_path, format=f"gif -index {i}") for i in range(image.n_frames)]
    
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind == len(frames):
            ind = 0
        loader_image_label.configure(image=frame)
        loader_toplevel.after(100, update, ind)

    # Crear el widget para mostrar la imagen .gif
    loader_image_label: Label = Label(loader_toplevel, background="")
    loader_image_label.pack(side=TOP, expand=True)

    loader_toplevel.after(0, update, 0)

    return loader_toplevel

# Función que oculta el loader
def hide_loader(parent: Union[Window, Toplevel], loader_toplevel: Toplevel) -> None:
    """
    Función que oculta el loader
    """
    parent.attributes(_0DISABLED, False) # Habilitamos la ventana principal de nuevo
    loader_toplevel.destroy() # Detener la animación y cerrar la ventana

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Crear la ventana principal
    window: Window = _generate_window()

    # Función que se ejecuta al pulsar el botón
    def clic() -> None:
        """
        Función que se ejecuta al pulsar el botón
        """
        # Función que ejecuta el trabajo
        def work() -> None:
            """
            Función que ejecuta el trabajo
            """
            print("sleep time start")        
            for i in range(10):
                print(i)
                time.sleep(1)
            print("sleep time stop")

            # Ocultamos el loader
            hide_loader(window, loader_toplevel)

        # Mostramos el loader
        loader_toplevel: Toplevel = show_loader(window, _LOADER_IMAGE_PATH)
        
        # Arrancamos la función de trabajo en otro hilo y controlamos la excepción que pueda arrojar el hilo
        try:
            thread: Thread = Thread(target=work)
            thread.start()
        except Exception as exception:
            messagebox.showerror(title="Error", message=f"Thread execution error:\n{exception}")

    button: Button = Button(window, text="Work", command=clic)
    button.pack(side=TOP, expand=True)

    # Generamos el hilo que genera la ventana del programa
    window.mainloop()
