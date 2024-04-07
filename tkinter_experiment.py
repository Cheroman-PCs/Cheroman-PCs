from os import path
from ttkbootstrap import Window, Frame, Treeview, Scrollbar, Floodgauge, Style, Label, Button, SUCCESS, HEADINGS, LEFT, BOTH, CENTER, VERTICAL, RIGHT, Y, DETERMINATE, END, BOTTOM, TOP, Canvas, X
from tkinter.messagebox import showinfo, askyesno, showwarning
from tkinter.filedialog import askopenfilenames
from threading import Thread
from typing import Tuple
from cytoflow import Tube, ImportOp, Experiment, ThresholdOp, DensityGateOp, FlowPeaksOp
from numpy import float64, ndarray, argmax, sort
from csv import writer
from pandas.core.frame import DataFrame
from matplotlib.figure import Figure
from matplotlib.axes._axes import Axes
from matplotlib.pyplot import subplots, show, close
from pandas.core.arrays.categorical import Categorical
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables globales
_THEME_NAME: str = "cyborg"
_APPLICATION_TITLE: str = "Tkinter experiment"
_MINIMUM_WINDOW_WIDTH: int = 800
_MINIMUM_WINDOW_HEIGHT: int = 600
_COLUMNS: tuple = ("file_name", "total_number_events", "number_cluster_events", "percentage_number_events_total", "mfi_cluster") # Definimos las columnas del treeview
_USER_DESKTOP_DIRECTORY: str = path.expanduser("~\\Desktop") # Esto obtiene el directorio de escritorio de usuario
_XCHANNEL: str = "R1-A"
_YCHANNEL: str = "B8-A"
_SCALE: str = "log"
_CHANNEL: str = "B4-A"
_CLUSTER_NAME: str = "FlowPeaks"
_experiment_dictionary: dict = {}

# Función principal del programa
def _main() -> None:
    '''
    Función principal del programa
    '''
    # Generamos la ventana del programa
    window: Window = generate_window()
    
    # Dimensionamos y posicionamos la ventana en la pantalla
    window_size_placement(window)

    # El estado de la ventana será maximizado
    # window.state("zoomed")

    # Generamos los marcos de la ventana del programa
    buttons_frame: Frame = generate_buttons_frame(window) # Generamos el marco de los botones
    treeview_frame: Frame = generate_treeview_frame(window) # Generamos el marco de la tabla de datos
    canvas_button_frame: Frame = generate_canvas_button_frame(window) # Generamos el marco del botón del canvas
    # canvas_frame: Frame = generate_canvas_frame(canvas_button_frame) # Generamos el marco del canvas

    # Generamos la tabla de datos
    treeview: Treeview = generate_treeview(treeview_frame, window)

    # Generamos los botones
    generate_buttons(window, buttons_frame, canvas_button_frame, treeview)
    
    # Mostramos el canvas cada vez que seleccionamos una fila del treeview una vez que se ha cargado todo
    treeview.bind("<<TreeviewSelect>>", lambda event: show_canvas_selected_row_treeview(canvas_button_frame, treeview))

    # Generamos el hilo que genera la ventana del programa
    window.mainloop()

# Función que genera la ventana del programa
def generate_window() -> Window:
    '''
    Función que genera la ventana del programa
    '''
    # Generamos la ventana con un tema específico, un título y unas dimensiones mínimas
    window: Window = Window(themename=_THEME_NAME)
    window.title(_APPLICATION_TITLE)
    window.minsize(_MINIMUM_WINDOW_WIDTH, _MINIMUM_WINDOW_HEIGHT)

    # Retornamos la ventana del programa
    return window

# Función que dimensiona y posiciona la ventana en la pantalla
def window_size_placement(window: Window) -> None:
    '''
    Función que dimensiona y posiciona la ventana en la pantalla
    '''
    # Obtiene las dimensiones de la pantalla
    screen_width: int = window.winfo_screenwidth()
    screen_height: int = window.winfo_screenheight()

    # Calcula la posición del centro
    position_top: int = int(screen_height / 2 - _MINIMUM_WINDOW_HEIGHT / 2)
    position_right: int = int(screen_width / 2 - _MINIMUM_WINDOW_WIDTH / 2)

    # Posiciona la ventana en el centro de la pantalla
    window.geometry(f"{_MINIMUM_WINDOW_WIDTH}x{_MINIMUM_WINDOW_HEIGHT}+{position_right}+{position_top}")

# Función que genera el marco de los botones
def generate_buttons_frame(window: Window) -> Frame:
    '''
    Función que genera el marco de los botones
    '''
    # Creamos un frame en el que generaremos los botones
    buttons_frame: Frame = Frame(window)
    buttons_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)

    return buttons_frame

# Función que genera el marco de la tabla de datos
def generate_treeview_frame(window: Window) -> Frame:
    '''
    Función que genera el marco de la tabla de datos
    '''
    # Creamos un frame en el que generaremos el treeview
    treeview_frame: Frame = Frame(window)
    treeview_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.5)

    return treeview_frame

# Función que genera el marco del canvas y del botón de mostrar el canvas
def generate_canvas_button_frame(window: Window) -> Frame:
    '''
    Función que genera el marco del canvas y del botón de mostrar el canvas
    '''
    # Creamos un frame en el que generaremos el canvas y del botón de mostrar el canvas
    canvas_button_frame: Frame = Frame(window)
    canvas_button_frame.place(relx=0.2, rely=0.5, relwidth=0.8, relheight=0.5)

    return canvas_button_frame

# Función que genera el marco del canvas
# def generate_canvas_frame(canvas_button_frame: Frame) -> Frame:
#     '''
#     Función que genera el marco del canvas
#     '''
#     # Creamos un frame en el que generaremos el canvas
#     canvas_frame: Frame = Frame(canvas_button_frame)
#     canvas_frame.place(relx=0, rely=0, relwidth=1, relheight=0.8)

#     return canvas_frame

# Función que genera la tabla con los datos
def generate_treeview(treeview_frame: Frame, window: Window) -> Treeview:
    '''
    Función que genera la tabla con los datos
    '''
    # Creamos el treeview
    treeview: Treeview = Treeview(treeview_frame, bootstyle=SUCCESS, columns=_COLUMNS, show=HEADINGS) # NOTA: Para mostrar la columna #0, poner el atributo show=TREEHEADINGS
    treeview.pack(side=LEFT, fill=BOTH, expand=True)
    treeview.column(_COLUMNS[0], minwidth=162, width=162, anchor=CENTER)
    treeview.column(_COLUMNS[1], minwidth=100, width=100, anchor=CENTER)
    treeview.column(_COLUMNS[2], minwidth=125, width=125, anchor=CENTER)
    treeview.column(_COLUMNS[3], minwidth=150, width=150, anchor=CENTER)
    treeview.column(_COLUMNS[4], minwidth=75, width=75, anchor=CENTER)

    # Definimos las cabeceras
    treeview.heading(_COLUMNS[0], text="File name")
    treeview.heading(_COLUMNS[1], text="Total no. of events")
    treeview.heading(_COLUMNS[2], text="No. cluster events")
    treeview.heading(_COLUMNS[3], text="% no. of events over total")
    treeview.heading(_COLUMNS[4], text="MFI cluster")

    # Añadimos los scrollbars del treeview
    add_treeview_scrollbars(treeview_frame, treeview)

    # Seleccionamos los ficheros .fcs que queramos cargar los datos
    showinfo(title="Info", message=("Select the .fcs files"))
    select_fcs_files(treeview, window)

    return treeview

# Función que añade los scrollbars del treeview
def add_treeview_scrollbars(treeview_frame: Frame, treeview: Treeview) -> None:
    '''
    Función que añade los scrollbars del treeview
    '''
    style: Style = Style()
    style.configure("Vertical.TScrollbar", background="green", troughcolor="lightgreen", arrowcolor="white")

    vertical_scrollbar: Scrollbar = Scrollbar(treeview_frame, orient=VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)

# Función que selecciona archivos .fcs
def select_fcs_files(treeview: Treeview, window: Window) -> None:
    '''
    Función que selecciona archivos .fcs
    '''
    file_paths: tuple = askopenfilenames(initialdir=_USER_DESKTOP_DIRECTORY, filetypes=[("FCS files", "*.fcs")]) # Abre el cuadro de diálogo para seleccionar archivos
    if file_paths != "": # Si la lista de rutas de archivo no está vacía
        if treeview.get_children(): # Si el treeview contiene alguna línea
            treeview = delete_existing_elements_treeview(treeview) # Vaciamos el treeview
            _experiment_dictionary.clear() # Y también vaciamos el diccionario de experimentos
        
        floodgauge_frame = Frame(window)
        floodgauge_frame.place(relx=0.5, rely=0.5, relwidth=0.3, relheight=0.1, anchor=CENTER)

        style = Style()
        style.configure("Horizontal.TFloodgauge", background="green", troughcolor ="lightgreen", bordercolor="green")

        percentage: str = "0"
        floodgauge: Floodgauge = Floodgauge(floodgauge_frame, length=100, mode=DETERMINATE, style="Horizontal.TFloodgauge", mask=f"{update_floodgauge_mask(percentage)}", font=("Helvetica", 16, "bold"))
        floodgauge.pack(fill=BOTH, expand=True)

        thread: Thread = Thread(target=lambda: process_files(floodgauge, file_paths, treeview, floodgauge_frame))
        thread.start()

# Función que borra todos los elementos existentes en el treeview
def delete_existing_elements_treeview(treeview: Treeview) -> Treeview:
    '''
    Función que borra todos los elementos existentes en el treeview
    '''
    for i in treeview.get_children():
        treeview.delete(i)

    return treeview

# Función que actualiza la máscara de floodgauge
def update_floodgauge_mask(percentage: str) -> str:
    '''
    Función que actualiza la máscara de floodgauge
    '''
    return f"Processing\n{percentage}%"

# Función que procesa los archivos
def process_files(floodgauge: Floodgauge, file_paths: str, treeview: Treeview, floodgauge_frame: Frame) -> None:
    '''
    Función que procesa los archivos
    '''
    number_file_paths: int = len(file_paths)
    floodgauge["maximum"] = number_file_paths

    for i, fcs_file in enumerate(file_paths):
        add_data_treeview(treeview, fcs_file) # Añadimos los datos al treeview

        floodgauge["value"] = i + 1

        percentage: str = round((floodgauge["value"] / number_file_paths) * 100)
        floodgauge["mask"] = f"{update_floodgauge_mask(percentage)}"

        floodgauge.update()
    
    floodgauge.destroy()
    floodgauge_frame.destroy()

    # Si el treeview contiene alguna línea, seleccionamos el primer elemento del treeview para mostrar el canvas
    if treeview.get_children():
        treeview.selection_set(treeview.get_children()[0])

# Función que añade los datos al treeview
def add_data_treeview(treeview: Treeview, fcs_file: str) -> Treeview:
    '''
    Función que añade los datos al treeview
    '''
    treeview.insert("", END, values=new_experiment(fcs_file))

    return treeview

# Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
def new_experiment(fcs_file: str) -> Tuple[str, int, int, str, str]:
    '''
    Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
    '''
    tube: Tube = Tube(file=fcs_file)

    import_op: ImportOp = ImportOp(tubes=[tube], channels={_XCHANNEL : _XCHANNEL, _YCHANNEL : _YCHANNEL, _CHANNEL : _CHANNEL})
    experiment: Experiment = import_op.apply()

    # Realizamos la operación Threshold sobre el experimento
    operation_name: str = "Threshold"
    threshold_op: ThresholdOp = ThresholdOp(name=operation_name, channel=_XCHANNEL, threshold=2000)
    experiment_threshold: Experiment = threshold_op.apply(experiment)
    # print(f"type experiment_threshold.query(operation_name): {type(experiment_threshold.query(operation_name))}")
    experiment_threshold = experiment_threshold.query(operation_name)

    # Realizamos la operación DensityGate sobre el experimento
    operation_name: str = "DensityGate"
    density_gate_op: DensityGateOp = DensityGateOp(name=operation_name, xchannel=_XCHANNEL, xscale=_SCALE, ychannel=_YCHANNEL, yscale=_SCALE, keep=0.5)
    density_gate_op.estimate(experiment_threshold)
    experiment_density_gate: Experiment = density_gate_op.apply(experiment_threshold)
    experiment_density_gate = experiment_density_gate.query(operation_name)

    # Realizamos la operación de clustering FlowPeaks sobre el experimento
    flow_peaks_op: FlowPeaksOp = FlowPeaksOp(name=_CLUSTER_NAME, channels=[_XCHANNEL, _YCHANNEL], scale={_XCHANNEL : _SCALE, _YCHANNEL : _SCALE}, h0=3)
    flow_peaks_op.estimate(experiment_density_gate)
    experiment_flow_peaks: Experiment = flow_peaks_op.apply(experiment_density_gate)
    argmax(experiment_flow_peaks[[_CLUSTER_NAME]].groupby(by=experiment_flow_peaks[_CLUSTER_NAME]).count())

    # Asignamos a variables los datos que queremos retornar del experimento
    file_name: str = path.basename(fcs_file)
    total_number_events: int = experiment.data.shape[0]
    number_events_cluster_interest: int = experiment_flow_peaks.data.shape[0]
    percentage_represents_number_events_cluster_interest_total: str = "{:.2%}".format(number_events_cluster_interest / total_number_events)
    mfi_cluster_interest: str = "{:.2f}".format(median_fluorescence_intensity_cluster_interest(experiment_flow_peaks))

    # Guardamos el experimento en un diccionario, tomando como clave el nombre del fichero .fcs
    _experiment_dictionary[file_name] = experiment_flow_peaks
    
    # Retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
    return (file_name, total_number_events, number_events_cluster_interest, percentage_represents_number_events_cluster_interest_total, mfi_cluster_interest)

# Función que calcula la Intensidad Mediana de Fluorescencia (IMF) sobre el cluster de interés
def median_fluorescence_intensity_cluster_interest(file_name: str) -> float64:
    '''
    Función que calcula la Intensidad Mediana de Fluorescencia (IMF) sobre el cluster de interés
    '''
    # Ordenamos los datos del experimento en el canal deseado
    sorted_data: ndarray = sort(_experiment_dictionary[file_name][_CHANNEL])
    # Obtenemos el número total de datos
    total_number_data: int = len(sorted_data)
    
    # Si el número de datos es par
    if total_number_data % 2 == 0:
        return (sorted_data[total_number_data // 2 - 1] + sorted_data[total_number_data // 2]) / 2
    # Si el número de datos es impar
    else:
        return sorted_data[total_number_data // 2]

# Función que genera los botones
def generate_buttons(window, buttons_frame: Frame, canvas_button_frame: Frame, treeview: Treeview) -> None:
    '''
    Función que genera los botones
    '''
    # Ponemos un componente de relleno en la parte superior para poder centrar los botones verticalmente
    label1: Label = Label(buttons_frame)
    label1.pack(side=TOP, expand=True)
    
    # Creamos los botones
    # Creamos un estilo
    style: Style = Style()
    style.configure("TButton", background="green", foreground="lightgreen", font=("Helvetica", 12, "bold"))

    # Botón cargar archivos
    load_files_button: Button = Button(buttons_frame, text="Load files", command=lambda: select_fcs_files(treeview, window))
    load_files_button.pack(side=TOP, pady=50)

    # Botón borrar
    delete_button: Button = Button(buttons_frame, text="Delete", command=lambda: delete_row(treeview, canvas_button_frame))
    delete_button.pack(side=TOP, pady=50)

    # Botón exportar
    export_button: Button = Button(buttons_frame, text="Export", command=lambda: export_to_csv(treeview))
    export_button.pack(side=TOP, pady=50)

    # Y también ponemos otro componente de relleno en la parte inferior para poder centrar los botones verticalmente
    label2: Label = Label(buttons_frame)
    label2.pack(side=TOP, expand=True)

# Función que borra filas
def delete_row(treeview: Treeview, canvas_button_frame: Frame) -> None:
    '''
    Función que borra filas
    '''
    selected_items: tuple = treeview.selection() # Esto devuelve una lista de los ID de las filas seleccionadas
    if selected_items: # Si hay alguna fila seleccionada
        confirm: bool = askyesno(title="Confirmation", message=f"Are you sure you want to delete {len(selected_items)} row(s)?") # Mostramos un popup para confirmar o no que queremos borrar las filas
        if confirm: # Si hemos confirmado
            for selected_item in selected_items: # Borramos las filas seleccionadas
                valores = treeview.item(selected_item, "values") # Obtenemos los valores de la fila
                experiment = valores[0] # Obtenemos el valor de la primera columna
                if experiment in _experiment_dictionary: # Comprobamos si la clave está en el diccionario
                    del _experiment_dictionary[experiment] # Borramos el elemento del diccionario
                treeview.delete(selected_item)
        if not treeview.get_children(): # Si el treeview se ha quedado vacío
            for widget in canvas_button_frame.winfo_children(): # Destruimos todos los componentes del marco del canvas
                widget.destroy()
    else: # En el caso de no haber ninguna fila seleccionada
        showwarning(title="Warning", message="No row selected") # Mostramos un cuadro de diálogo de advertencia

# Función que exporta el treeview a un fichero .csv
def export_to_csv(treeview: Treeview) -> None:
    '''
    Función que exporta el treeview a un fichero .csv
    '''
    if treeview.get_children(): # Si el treeview contiene alguna línea, se exportarán los datos del treeview, sino, aparecerá una advertencia diciendo que no hay datos que exportar del treeview
        csv_file_name: str = "treeview.csv"
        csv_file: str = path.join(_USER_DESKTOP_DIRECTORY, csv_file_name) # Esto une el directorio de escritorio de usuario y "treeview.csv" para formar una ruta completa donde se encuentra el archivo .csv
        with open(csv_file, "w", newline="") as file:
            file_writer = writer(file)
            file_writer.writerow(_COLUMNS) # Escribimos los nombres de las columnas
            for row_id in treeview.get_children():
                row: list = treeview.item(row_id)["values"]
                file_writer.writerow(row)
        showinfo(title="Info", message="The treeview was exported to a .csv file on the desktop")
    else:
        showwarning(title="Warning", message="There is no data in the treeview to export") # Mostramos un cuadro de diálogo de advertencia

# Función que muestra el canvas
def show_canvas_selected_row_treeview(canvas_button_frame: Frame, treeview: Treeview) -> None:
    '''
    Función que muestra el canvas
    '''
    selected_items: tuple = treeview.selection() # Esto devuelve una lista de los ID de las filas seleccionadas
    if len(selected_items) == 1:
        # Obtenemos el valor de la 1ª columna
        column_value: str = treeview.item(selected_items[0])["values"][0]

        # Una vez realizadas las opereaciones, pintamos la gráfica de puntos en la ventana del programa
        generate_canvas(canvas_button_frame, column_value)

        # Y generamos el botón por si queremos visualizar la gráfica en una ventana a parte
        generate_canvas_button(canvas_button_frame, column_value)
    else:
        for widget in canvas_button_frame.winfo_children(): # Destruimos todos los componentes del marco del canvas
            widget.destroy()

# Función que pinta los eventos del cluster en una gráfica en la ventana del programa
def generate_canvas(canvas_button_frame: Frame, column_value: str, clic_view_graph_window_button: bool=False) -> None:
    '''
    Función que pinta los eventos del cluster en una gráfica en la ventana del programa
    '''
    for widget in canvas_button_frame.winfo_children(): # Destruimos todos los componentes del marco del canvas
        widget.destroy()
    
    data_frame: DataFrame = _experiment_dictionary.get(column_value).data

    # Dibujamos la gráfica de puntos
    figure: Figure
    axes: Axes
    figure, axes = subplots()

    # Dibujamos los puntos, diferenciando los clusters por color
    clusters: Categorical = data_frame[_CLUSTER_NAME].unique()
    for cluster in clusters:
        data_frame_cluster: DataFrame = data_frame[data_frame[_CLUSTER_NAME] == cluster]
        axes.scatter(data_frame_cluster[_XCHANNEL], data_frame_cluster[_YCHANNEL], label=f"{_CLUSTER_NAME} {cluster}", s=5, color="green")

    # Mostramos la leyenda
    axes.legend()
    
    # Crear el canvas de tkinter y añadir la figura de matplotlib
    figure_canvas_tk_agg: FigureCanvasTkAgg = FigureCanvasTkAgg(figure, master=canvas_button_frame)
    figure_canvas_tk_agg.draw()
    canvas: Canvas = figure_canvas_tk_agg.get_tk_widget()
    canvas.pack(fill=BOTH, expand=True, padx=100, pady=20)

    # Si hemos pulsado el botón de ver gráfica en ventana
    if clic_view_graph_window_button:
        show()
    
    # Cerramos la figura para que el programa no se quede pillado al cerrarlo
    close(fig=figure)

# Función que genera el botón de ver la gráfica en ventana
def generate_canvas_button(canvas_button_frame: Frame, column_value: str) -> None:
    '''
    Función que genera el botón de ver la gráfica en ventana
    '''
    # Creamos el botón ver gráfica en ventana
    view_graph_window_button: Button = Button(canvas_button_frame, text="View graph in window", command=lambda: show_graph_window(canvas_button_frame, column_value, True))
    # view_graph_window_button.pack(side=BOTTOM, padx=10, pady=20)
    view_graph_window_button.pack(fill=X, expand=True)

# Función que muestra la gráfica en ventana
def show_graph_window(canvas_button_frame: Frame, column_value: str, clic_view_graph_window_button: bool) -> None:
    '''
    Función que muestra la gráfica en ventana
    '''
    # Generamos el canvas y lo mostramos en una ventana
    generate_canvas(canvas_button_frame, column_value, clic_view_graph_window_button)

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Ejecutamos la función principal del programa
    _main()
