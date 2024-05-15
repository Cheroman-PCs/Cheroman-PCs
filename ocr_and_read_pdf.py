import sys
import os
from PyPDF2 import PdfReader, PdfWriter, PageObject
import pytesseract
import pdf2image
from tkinter import messagebox, filedialog
from ttkbootstrap import Window, Label, Toplevel
import shutil
from PIL.PpmImagePlugin import PpmImageFile
import re
from threading import Thread
from loader import loader # type: ignore

_USER_DIRECTORY_PATH: str = os.path.expanduser("~") # Esto obtiene el directorio de usuario
_TEMPORARY_USER_DIRECTORY_NAME: str = "AppData\\Local\\Temp"
_TEMPORARY_USER_DIRECTORY_PATH: str = os.path.join(_USER_DIRECTORY_PATH, _TEMPORARY_USER_DIRECTORY_NAME)
_PROGRAM_TEMPORARY_DIRECTORY_NAME: str = "ocr-and-read-pdf"
_PROGRAM_TEMPORARY_DIRECTORY_PATH: str = os.path.join(_TEMPORARY_USER_DIRECTORY_PATH, _PROGRAM_TEMPORARY_DIRECTORY_NAME)
_BASE_ROUTE: str = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
_LOADER_IMAGE_NAME: str = "loader\\icons\\loader.gif"
_LOADER_IMAGE_PATH: str = os.path.join(_BASE_ROUTE, _LOADER_IMAGE_NAME) # Esto obtiene la imagen del loader
_TESSERACT_OCR_PROGRAM_PATH: str = os.path.join(_BASE_ROUTE, "Tesseract-OCR") # Esto obtiene la ruta del programa Tesseract OCR (versión 5.3.3.20231005)
_POPPLER_PROGRAM_PATH: str = os.path.join(_BASE_ROUTE, "poppler-24.02.0\\Library\\bin") # Esto obtiene la ruta del programa Poppler (versión 24.02.0)
_PATH: str = "PATH"
_RB: str = "rb"
_THEME_NAME: str = "cyborg"
_APPLICATION_TITLE: str = "OCR and read PDF"
_WB: str = "wb"

# Función que genera el directorio temporal del programa en el directorio temporal de usuario
def generate_temp_directory(program_temporary_directory_path: str) -> None:
    """
    Función que genera el directorio temporal del programa en el directorio temporal de usuario
    """
    # Comprobamos si el directorio del programa existe y si no, lo crea
    if not os.path.exists(program_temporary_directory_path):
        os.makedirs(program_temporary_directory_path) # Esto crea el directorio temporal del programa en el directorio temporal de usuario

# Función que lee el PDF
def read_pdf(pdf_file_path: str) -> str:
    """
    Función que lee el PDF
    """
    text: str
    with open(pdf_file_path, _RB) as pdf_file:
        pdf_reader: PdfReader = PdfReader(pdf_file)
        page_object: PageObject = pdf_reader.pages[0]
        text = page_object.extract_text()
    
    return text

# Función que convierte el PDF en texto aplicando OCR
def pdf_to_text_applying_ocr(pdf_file_path: str) -> str:
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
    # Convertimos la primera página del PDF a imagen
    image_first_page: PpmImageFile = pdf2image.convert_from_path(pdf_file_path)[0]

    # Aplicamos OCR a la imagen
    text: str = pytesseract.image_to_string(image_first_page)

    return text

# Función que extrae el valor del texto del PDF
def extract_value(text: str, words: list) -> str:
    """
    Función que extrae el valor del texto del PDF
    """
    # Reemplazamos y eliminamos previamente todo lo que nos pueda causar problemas
    text = text.replace(",", ".") # Sustituimos las comas por puntos
    text = text.replace("$", "5") # Sustituimos los dólares por cincos, ya que algunas veces el cinco lo lee como dólar
    CHARS: str = "!\"#%&'()*+-/:;<=>?@[\]^_`{|}~ø£Ø×ƒªº¿®¬½¼¡«»░▒▓│┤©╣║╗╝¢¥┐└┴┬├─┼╚╔╩╦╠═╬¤ðÐı┘┌█▄¦▀ßõµþÞ¯´≡±‗¾¶§÷¸°¨·¹³²■—”“‘€’™"
    for char in CHARS:
        text = text.replace(char, "") # Eliminamos los caracteres no deseados
    
    lines: list[str] = text.split("\n") # Partimos el texto en líneas
    word: str
    line: str
    value: str = None
    for word in words: # Recorremos la lista de palabras
        for line in lines: # Recorremos todas las líneas
            if word in line: # Si la palabra está en la línea
                # Con esto, conseguimos la línea desde la palabra clave, omitiendo todo lo que tenga por delante de la palabra clave
                list_: list[str] = line.split(word)
                if len(list_) > 1:
                    line = word + word.join(list_[1:])
                
                line = " ".join(line.split()) # Separamos todas las palabras por un sólo espacio

                value = line.split(" ")[1] # Cogemos el primer dato que hay después de la palabra clave, que es el valor, y lo almacenamos en la variable que vamos a retornar

                # Antes de retornar el valor lo arreglamos por si no es correcto
                value = re.sub("[^0-9\\.]", "", value) # Reemplazamos cualquier carácter que no sea un número o un punto por nada
                value = re.sub("^\\.|\\.$", "", value) # Si el valor comienza o termina con un punto, lo reemplazamos por nada

                # Convertimos el valor a un float, si lanza una excepción retornamos None, ya que el valor tiene que ser un número en decimal
                try:
                    float(value)
                except ValueError:
                    return None
                
                # Comprobamos si el valor no contiene un punto, si es así retornamos None, ya que el valor tiene que ser un número en decimal
                if "." not in value:
                    return None

                return value

# Función que rota el PDF 90°
def rotate_page_ninety_degrees(pdf_path: str, original_pdf_path: str, program_temporary_directory_path: str) -> str:
    """
    Función que rota el PDF 90°
    """
    # Abrimos el PDF y creamos un nuevo PDF temporal para la salida
    pdf_reader: PdfReader = PdfReader(pdf_path)
    pdf_writer: PdfWriter = PdfWriter()

    # Rotamos la página 90°
    page_object: PageObject = pdf_reader.pages[0]
    page_object = page_object.rotate(90)

    # Añadimos la página rotada al nuevo PDF temporal
    pdf_writer.add_page(page_object)

    # Guardamos el nuevo PDF temporal
    TEMPORARY_OUTPUT_PDF_FILE_NAME: str = f"temp_{os.path.basename(original_pdf_path)}"
    TEMPORARY_OUTPUT_PDF_FILE: str = os.path.join(program_temporary_directory_path, TEMPORARY_OUTPUT_PDF_FILE_NAME)
    with open(TEMPORARY_OUTPUT_PDF_FILE, _WB) as temp_output_pdf:
        pdf_writer.write(temp_output_pdf)
    
    return TEMPORARY_OUTPUT_PDF_FILE

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Generamos el directorio temporal del programa en el directorio temporal de usuario
    try:
        generate_temp_directory(_PROGRAM_TEMPORARY_DIRECTORY_PATH)
    except Exception as exception:
        messagebox.showerror(title="Error", message=f"Error creating temporary directory:\n{exception}")

    # Comprobamos si las rutas de los programas Tesseract y Poppler están en el path
    if _TESSERACT_OCR_PROGRAM_PATH not in os.environ[_PATH]:
        os.environ[_PATH] += os.pathsep + _TESSERACT_OCR_PROGRAM_PATH
    if _POPPLER_PROGRAM_PATH not in os.environ[_PATH]:
        os.environ[_PATH] += os.pathsep + _POPPLER_PROGRAM_PATH
    
    window: Window = Window(themename=_THEME_NAME)
    window.title(_APPLICATION_TITLE)
    PDF_FILE: str = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")]) # Abre el cuadro de diálogo para seleccionar un archivo
    if PDF_FILE != "":
        def work():
            # Leemos el PDF
            text: str = read_pdf(PDF_FILE)

            # Extraemos los valores
            WORDS_HEMOGLOBINA: list = ["HEMOGLOBINA ", "HGB "]
            WORDS_LEUCOCITOS: list = ["LEUCOCITOS ", "WBC "]
            WORDS_HEMATIES: list = ["HEMATIES ", "RBC ", "HEMATÍES "]
            value_hemoglobina: str = extract_value(text.upper(), WORDS_HEMOGLOBINA)
            value_leucocitos: str = extract_value(text.upper(), WORDS_LEUCOCITOS)
            value_hematies: str = extract_value(text.upper(), WORDS_HEMATIES)

            # Si alguno de estos valores es None aplicamos OCR al PDF
            if value_hemoglobina is None or value_leucocitos is None or value_hematies is None:
                # Aplicamos OCR al PDF
                text = pdf_to_text_applying_ocr(PDF_FILE)

                # Extraemos los valores
                value_hemoglobina = extract_value(text.upper(), WORDS_HEMOGLOBINA)
                value_leucocitos = extract_value(text.upper(), WORDS_LEUCOCITOS)
                value_hematies = extract_value(text.upper(), WORDS_HEMATIES)

                # Rotamos el PDF si es necesario
                pdf_file: str = PDF_FILE # En principio, el fichero que vamos a procesar es el PDF original
                for _ in range(3): # La rotación del PDF como máximo se aplicará 3 veces para poderlo leer. NOTA: En el caso de rotar por completo el PDF y obtener los 3 valores None, el PDF es ilegible
                    # Si todos los valores son None, probablemente el PDF esté mal rotado, por tanto, rotamos la página del PDF 90°
                    if value_hemoglobina is None and value_leucocitos is None and value_hematies is None:
                        # Rotamos la página 90° y ahora ya, una vez rotado el PDF tenemos que utilizar el PDF de salida temporal
                        pdf_file = rotate_page_ninety_degrees(pdf_file, PDF_FILE, _PROGRAM_TEMPORARY_DIRECTORY_PATH)

                        # Aplicamos OCR al PDF de salida temporal
                        text = pdf_to_text_applying_ocr(pdf_file)

                        # Extraemos los valores
                        value_hemoglobina = extract_value(text.upper(), WORDS_HEMOGLOBINA)
                        value_leucocitos = extract_value(text.upper(), WORDS_LEUCOCITOS)
                        value_hematies = extract_value(text.upper(), WORDS_HEMATIES)
                    else:
                        # Si alguno de los valores no es None, salimos del bucle
                        break
            # Mostramos los valores obtenidos
            hemoglobina_label: Label = Label(window, text=f"HEMOGLOBINA: {value_hemoglobina}")
            hemoglobina_label.pack()

            leucocitos_label: Label = Label(window, text=f"LEUCOCITOS: {value_leucocitos}")
            leucocitos_label.pack()

            hematies_label: Label = Label(window, text=f"HEMATÍES: {value_hematies}")
            hematies_label.pack()

            loader.hide_loader(window, loader_toplevel)

        loader_toplevel: Toplevel = loader.show_loader(window, _LOADER_IMAGE_PATH)
        # Arrancamos la función de trabajo en otro hilo y controlamos la excepción que pueda arrojar el hilo
        try:
            thread: Thread = Thread(target=work)
            thread.start()
        except Exception as exception:
            messagebox.showerror(title="Error", message=f"Thread execution error:\n{exception}")
        window.mainloop()
    
    # Eliminamos la carpeta temporal del programa antes de salir del programa
    try:
        if os.path.exists(_PROGRAM_TEMPORARY_DIRECTORY_PATH):
            shutil.rmtree(_PROGRAM_TEMPORARY_DIRECTORY_PATH)
    except Exception as exception:
        messagebox.showerror(title="Error", message=f"Error deleting temporary directory:\n{exception}")