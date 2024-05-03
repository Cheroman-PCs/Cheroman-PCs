import sys
import os
# import pytesseract
import pdf2image
from tkinter import messagebox, filedialog
from ttkbootstrap import Window, Label
import subprocess
from subprocess import PIPE, CREATE_NO_WINDOW, CompletedProcess
from datetime import datetime
import shutil
from PIL.PpmImagePlugin import PpmImageFile
import re

_USER_DIRECTORY_PATH: str = os.path.expanduser("~") # Esto obtiene el directorio de usuario
_PROGRAM_DIRECTORY_NAME: str = "OCR and read PDF"
_PROGRAM_DIRECTORY_PATH: str = os.path.join(_USER_DIRECTORY_PATH, _PROGRAM_DIRECTORY_NAME) # Esto obtiene el directorio del programa
_LOGS_DIRECTORY_NAME: str = "Logs"
_LOGS_DIRECTORY_PATH: str = os.path.join(_PROGRAM_DIRECTORY_PATH, _LOGS_DIRECTORY_NAME)
_TEMPORARY_DIRECTORY_NAME: str = "AppData\\Local\\Temp"
_TEMPORARY_DIRECTORY_PATH: str = os.path.join(_USER_DIRECTORY_PATH, _TEMPORARY_DIRECTORY_NAME)
_PROGRAM_TEMPORARY_DIRECTORY_NAME: str = "ocr-and-read-pdf"
_PROGRAM_TEMPORARY_DIRECTORY_PATH: str = os.path.join(_TEMPORARY_DIRECTORY_PATH, _PROGRAM_TEMPORARY_DIRECTORY_NAME)
_BASE_ROUTE: str = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
_TESSERACT_OCR_PROGRAM_PATH: str = os.path.join(_BASE_ROUTE, "Tesseract-OCR") # Esto obtiene la ruta del programa Tesseract (versión 5.3.3.20231005)
_POPPLER_PROGRAM_PATH: str = os.path.join(_BASE_ROUTE, "poppler-24.02.0\\Library\\bin") # Esto obtiene la ruta del programa Poppler (versión 24.02.0)
_PATH: str = "PATH"
_W: str = "w"
_THEME_NAME: str = "cyborg"

# Función que genera el directorio del programa en el directorio de usuario
def generate_program_directory() -> None:
    """
    Función que genera el directorio del programa en el directorio de usuario
    """
    # Comprobamos si el directorio del programa existe y si no, lo crea
    if not os.path.exists(_PROGRAM_DIRECTORY_PATH):
        try:
            os.makedirs(_PROGRAM_DIRECTORY_PATH, exist_ok=True) # Esto crea el directorio del programa en el directorio de usuario
        except Exception as exception:
            messagebox.showerror(title="Error", message=f"Error creating program directory:\n{exception}")

# Función que genera el directorio logs del programa en el directorio del programa
def generate_logs_directory() -> None:
    """
    Función que genera el directorio logs del programa en el directorio del programa
    """
    # Comprobamos si el directorio del programa existe y si no, lo crea
    if not os.path.exists(_LOGS_DIRECTORY_PATH):
        try:
            os.makedirs(_LOGS_DIRECTORY_PATH, exist_ok=True) # Esto crea el directorio de logs del programa en el directorio de usuario
        except Exception as exception:
            messagebox.showerror(title="Error", message=f"Error creating program directory:\n{exception}")

# Función que genera el directorio temporal del programa en el directorio temporal de usuario
def generate_temp_directory() -> None:
    """
    Función que genera el directorio temporal del programa en el directorio temporal de usuario
    """
    # Comprobamos si el directorio temporal del programa existe y si no, lo crea
    if not os.path.exists(_PROGRAM_TEMPORARY_DIRECTORY_PATH):
        try:
            os.makedirs(_PROGRAM_TEMPORARY_DIRECTORY_PATH, exist_ok=True) # Esto crea el directorio temporal del programa en el directorio temporal de usuario
            # subprocess.check_call(["attrib", "+H", PROGRAM_TEMPORARY_DIRECTORY_PATH]) # Hacemos que el directorio sea oculto
        except Exception as exception:
            messagebox.showerror(title="Error", message=f"Error creating program temporary directory:\n{exception}")

# Función que convierte el PDF en texto aplicando OCR
def pdf_to_text(pdf_file_path: str) -> str:
    """
    Función que convierte el PDF en texto aplicando OCR
    #####################################################################
    # EJEMPLO DE PROCESAMIENTO DEL PDF COMPLETO:
    # Convertimos el PDF a imágenes
    images = pdf2image.convert_from_path(pdf_file_path)
    print(f"Nº images: {len(images)}")

    # Aplicamos OCR a cada imagen
    text = ""
    for i, image in enumerate(images):
        print(f"Procesando página {i + 1}...")
        text += pytesseract.image_to_string(image)

    return text
    #####################################################################
    """
    # Convertimos la primera página del PDF a imagen, ya que es la única que nos interesa
    image_first_page: PpmImageFile = pdf2image.convert_from_path(pdf_file_path)[0]

    # Guardamos la imagen en un archivo temporal
    TEMP_IMAGE_PNG_FILE_NAME: str = "temp_image.png"
    TEMP_IMAGE_PNG_FILE_PATH: str = os.path.join(_PROGRAM_TEMPORARY_DIRECTORY_PATH, TEMP_IMAGE_PNG_FILE_NAME)
    image_first_page.save(TEMP_IMAGE_PNG_FILE_PATH) # La guardamos en el directorio temporal del programa

    # Aplicamos OCR a la imagen mediante "pytesseract" (no podemos ocultar la consola de tesseract.exe)
    # text: str = pytesseract.image_to_string(image_first_page)

    # Aplicamos OCR a la imagen mediante comando "tesseract" (podemos ocultar la cosola de tesseract.exe)
    COMMAND: list[str] = ["tesseract", TEMP_IMAGE_PNG_FILE_PATH, "stdout", "--psm", "6"]
    result: CompletedProcess[bytes] = subprocess.run(COMMAND, stdout=PIPE, stderr=PIPE, creationflags=CREATE_NO_WINDOW)
    text_stdout: str = result.stdout.decode("utf-8") # Decodificamos el resultado de la salida en texto plano
    text_stderr: str = result.stderr.decode("utf-8") # Decodificamos el resultado de los errores en texto plano

    # Creamos un log de la operación tanto de la salida como de los errores
    TIMESTAMP: str = datetime.now().strftime("_%Y.%m.%d_%H.%M.%S")
    LOG_OUT_FILE_NAME: str = f"log_out{TIMESTAMP}.txt"
    LOG_OUT_FILE_PATH: str = os.path.join(_LOGS_DIRECTORY_PATH, LOG_OUT_FILE_NAME)
    LOG_ERR_FILE_NAME: str = f"log_err{TIMESTAMP}.txt"
    LOG_ERR_FILE_PATH: str = os.path.join(_LOGS_DIRECTORY_PATH, LOG_ERR_FILE_NAME)
    if text_stdout != "": # Si en la operación hay salida lo resgistramos en un fichero de log de salida
        with open(LOG_OUT_FILE_PATH, _W) as f_stdout:
            f_stdout.write(text_stdout)
    if text_stderr != "": # Si en la operación hay errores los resgistramos en un fichero de log de errores
        with open(LOG_ERR_FILE_PATH, _W) as f_stderr:
            f_stderr.write(text_stderr)

    # Eliminamos el fichero temporal de imagen PNG y la carpeta temporal del programa
    if os.path.isfile(TEMP_IMAGE_PNG_FILE_PATH):
        os.remove(TEMP_IMAGE_PNG_FILE_PATH)
    if os.path.exists(_PROGRAM_TEMPORARY_DIRECTORY_PATH):
        shutil.rmtree(_PROGRAM_TEMPORARY_DIRECTORY_PATH)

    return text_stdout

# Función que extrae el valor del texto del PDF
def extract_value(text: str, words: list) -> str:
    """
    Función que extrae el valor del texto del PDF
    """
    lines: list[str] = text.split("\n") # Partimos el texto en líneas
    word: str
    line: str
    value: str = None
    for word in words: # Recorremos la lista de palabras
        for line in lines: # Recorremos todas las líneas
            if word in line: # Si la palabra está en la línea
                # Reemplazamos y eliminamos todo lo que nos pueda causar problemas previamente
                line = line.replace(",", ".") # Sustituimos las comas por puntos
                line = line.replace(";", "") # Eliminamos los puntos y comas
                line = line.replace(":", "") # Eliminamos los dos puntos
                line = line.replace("*", "") # Eliminamos los asteriscos
                line = line.replace("=", "") # Eliminamos los símbolos igual a
                line = line.replace("¥", "") # Eliminamos los símbolos yen
                line = line.replace("‘", "") # Eliminamos las comillas simples inglesas de apertura
                line = line.replace("“", "") # Eliminamos las comillas dobles inglesas de apertura

                # Con esto, conseguimos la línea desde la palabra clave, omitiendo todo lo que tenga por delante de la palabra clave
                list_: list[str] = line.split(word)
                if len(list_) > 1:
                    line = word + word.join(list_[1:])
                
                line = " ".join(line.split()) # Separamos todas las palabras por un sólo espacio

                value = line.split(" ")[1] # Cogemos el primer dato que hay después de la palabra clave, que es el valor, y lo almacenamos en una variable que vamos a retornar

                value = re.sub("[^0-9\\.]", "", value) # Reemplazamos cualquier carácter que no sea un número o un punto por nada
                value = re.sub("^\\.|\\.$", "", value) # Si el valor comienza o termina con un punto, lo reemplazamos por nada

                return value

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Generamos el directorio del programa en el directorio de usuario
    generate_program_directory()

    # Generamos el directorio de logs del programa en el directorio del programa
    generate_logs_directory()

    # Generamos el directorio temporal del programa en el directorio temporal de usuario
    generate_temp_directory()

    # Comprobamos si las rutas de los programas Tesseract y Ghostscript están en el path
    if _TESSERACT_OCR_PROGRAM_PATH not in os.environ[_PATH]:
        os.environ[_PATH] += os.pathsep + _TESSERACT_OCR_PROGRAM_PATH
    if _POPPLER_PROGRAM_PATH not in os.environ[_PATH]:
        os.environ[_PATH] += os.pathsep + _POPPLER_PROGRAM_PATH
    
    window: Window = Window(themename=_THEME_NAME)
    window.title("OCR and read PDF")
    PDF_FILE_PATH: str = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")]) # Abre el cuadro de diálogo para seleccionar un archivo
    if PDF_FILE_PATH != "":
        # Aplicamos OCR al PDF
        text: str = pdf_to_text(PDF_FILE_PATH)

        # Extraemos los valores (HEMOGLOBINA <-> HGB, LEUCOCITOS <-> WBC, HEMATIES <-> RBC)
        words_hemoglobina_hgb: list = ["HEMOGLOBINA ", "HGB "]
        words_leucocitos_wbc: list = ["LEUCOCITOS ", "WBC "]
        words_hematies_rbc: list = ["HEMATIES ", "RBC ", "HEMATÍES "]
        value_hemoglobina_hgb: str = extract_value(text, words_hemoglobina_hgb)
        value_leucocitos_wbc: str = extract_value(text, words_leucocitos_wbc)
        value_hematies_rbc: str = extract_value(text, words_hematies_rbc)

        # Mostramos los valores obtenidos
        hemoglobina_hgb_label: Label = Label(window, text=f"HEMOGLOBINA <-> HGB: {value_hemoglobina_hgb}")
        hemoglobina_hgb_label.pack()

        leucocitos_wbc_label: Label = Label(window, text=f"LEUCOCITOS <-> WBC: {value_leucocitos_wbc}")
        leucocitos_wbc_label.pack()

        hematies_rbc_label: Label = Label(window, text=f"HEMATIES <-> RBC: {value_hematies_rbc}")
        hematies_rbc_label.pack()

        window.mainloop()

    # Eliminamos la carpeta temporal del programa antes de salir si no la hemos eliminado
    if os.path.exists(_PROGRAM_TEMPORARY_DIRECTORY_PATH):
        shutil.rmtree(_PROGRAM_TEMPORARY_DIRECTORY_PATH)
