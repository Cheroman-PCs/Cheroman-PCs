from os import path
from ttkbootstrap import Window, Frame, Treeview, Scrollbar, Label, Button, SUCCESS, HEADINGS, LEFT, BOTH, CENTER, VERTICAL, RIGHT, Y, END, BOTTOM, TOP
from tkinter.messagebox import showinfo, askyesno, showwarning
from tkinter.filedialog import askopenfilenames
from typing import Tuple
from cytoflow import Tube, ImportOp, Experiment, ThresholdOp, DensityGateOp, FlowPeaksOp
from numpy import float64, argmax, sort
from csv import writer
from matplotlib.pyplot import subplots, show, close
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables globales
_theme_name = "cyborg"
_application_title = "Tkinter experiment"
_minimum_window_width = 800
_minimum_window_height = 600
_columns = ("file_name", "total_number_events", "number_cluster_events", "percentage_number_events_total", "mfi_cluster") # Definimos las columnas del treeview
_user_directory = path.expanduser("~") # Esto obtiene el directorio de usuario
_user_desktop_directory = path.join(_user_directory, "Desktop") # Esto obtiene el directorio de escritorio de usuario
_xchannel = "R1-A"
_ychannel = "B8-A"
_scale = "log"
_channel = "B4-A"
_cluster_name = "FlowPeaks"
_experiment_dictionary = {}

# Función principal del programa
def _main() -> None:
    '''
    Función principal del programa
    '''
    # Generamos la ventana del programa
    window = generate_window()
    
    # Dimensionamos y posicionamos la ventana en la pantalla
    window_size_placement(window)

    # El estado de la ventana será maximizado
    # window.state("zoomed")

    # Generamos los marcos de la ventana del programa
    buttons_frame = generate_buttons_frame(window) # Generamos el marco de los botones
    treeview_frame = generate_treeview_frame(window) # Generamos el marco de la tabla de datos
    canvas_frame = generate_canvas_frame(window) # Generamos el marco del canvas

    # Generamos la tabla de datos
    treeview = generate_treeview(treeview_frame)

    # Generamos los botones
    generate_buttons(buttons_frame, canvas_frame, treeview)

    # Si el treeview contiene alguna línea, seleccionamos el primer elemento del treeview y mostramos el canvas
    if treeview.get_children():
        treeview.selection_set(treeview.get_children()[0])
    
    # Mostramos el canvas cada vez que seleccionamos una fila del treeview una vez que se ha cargado todo
    treeview.bind("<<TreeviewSelect>>", lambda event: show_canvas_selected_row_treeview(canvas_frame, treeview))

    # Generamos el hilo que genera la ventana del programa
    window.mainloop()

# Función que genera la ventana del programa
def generate_window() -> Window:
    '''
    Función que genera la ventana del programa
    '''
    # Generamos la ventana con un tema específico, un título y unas dimensiones mínimas
    window = Window(themename=_theme_name)
    window.title(_application_title)
    window.minsize(_minimum_window_width, _minimum_window_height)

    # Retornamos la ventana del programa
    return window

# Función que dimensiona y posiciona la ventana en la pantalla
def window_size_placement(window: Window) -> None:
    '''
    Función que dimensiona y posiciona la ventana en la pantalla
    '''
    # Obtiene las dimensiones de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcula la posición del centro
    position_top = int(screen_height / 2 - _minimum_window_height / 2)
    position_right = int(screen_width / 2 - _minimum_window_width / 2)

    # Posiciona la ventana en el centro de la pantalla
    window.geometry(f"{_minimum_window_width}x{_minimum_window_height}+{position_right}+{position_top}")

# Función que genera el marco de los botones
def generate_buttons_frame(window: Window) -> Frame:
    '''
    Función que genera el marco de los botones
    '''
    # Creamos un frame en el que generaremos los botones
    buttons_frame = Frame(window)
    buttons_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)

    return buttons_frame

# Función que genera el marco de la tabla de datos
def generate_treeview_frame(window: Window) -> Frame:
    '''
    Función que genera el marco de la tabla de datos
    '''
    # Creamos un frame en el que generaremos el treeview
    treeview_frame = Frame(window)
    treeview_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.5)

    return treeview_frame

# Función que genera el marco del canvas y del botón de mostrar el canvas
# def generate_canvas_frame_show_canvas_button(window: Window) -> Frame:
#     '''
#     Función que genera el marco del canvas y del botón de mostrar el canvas
#     '''
#     # Creamos un frame en el que generaremos el canvas y del botón de mostrar el canvas
#     canvas_frame_show_canvas_button = Frame(window)
#     canvas_frame_show_canvas_button.place(relx=0.2, rely=0.5, relwidth=0.8, relheight=0.5)

#     return canvas_frame_show_canvas_button

# Función que genera el marco del canvas
def generate_canvas_frame(window: Window) -> Frame:
    '''
    Función que genera el marco del canvas
    '''
    # Creamos un frame en el que generaremos el canvas
    canvas_frame = Frame(window)
    canvas_frame.place(relx=0.2, rely=0.5, relwidth=0.8, relheight=0.5)

    return canvas_frame

# Función que genera la tabla con los datos
def generate_treeview(treeview_frame: Frame) -> Treeview:
    '''
    Función que genera la tabla con los datos
    '''
    # Creamos el treeview
    treeview = Treeview(treeview_frame, bootstyle=SUCCESS, columns=_columns, show=HEADINGS) # NOTA: Para mostrar la columna #0, poner el atributo show=TREEHEADINGS
    treeview.pack(side=LEFT, fill=BOTH, expand=True)
    treeview.column(_columns[0], minwidth=162, width=162, anchor=CENTER)
    treeview.column(_columns[1], minwidth=100, width=100, anchor=CENTER)
    treeview.column(_columns[2], minwidth=125, width=125, anchor=CENTER)
    treeview.column(_columns[3], minwidth=150, width=150, anchor=CENTER)
    treeview.column(_columns[4], minwidth=75, width=75, anchor=CENTER)

    # Definimos las cabeceras
    treeview.heading(_columns[0], text="File name")
    treeview.heading(_columns[1], text="Total no. of events")
    treeview.heading(_columns[2], text="No. cluster events")
    treeview.heading(_columns[3], text="% no. of events over total")
    treeview.heading(_columns[4], text="MFI cluster")

    # Añadimos los scrollbars del treeview
    add_treeview_scrollbars(treeview_frame, treeview)

    # Seleccionamos los ficheros .fcs que queramos cargar los datos
    showinfo(title="Info", message=("Select the .fcs files"))
    select_fcs_files(treeview)

    return treeview

# Función que añade los scrollbars del treeview
def add_treeview_scrollbars(treeview_frame: Frame, treeview: Treeview) -> None:
    '''
    Función que añade los scrollbars del treeview
    '''
    vertical_scrollbar = Scrollbar(treeview_frame, orient=VERTICAL, command=treeview.yview)
    treeview.configure(yscrollcommand=vertical_scrollbar.set)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)

# Función que selecciona archivos .fcs
def select_fcs_files(treeview: Treeview) -> None:
    '''
    Función que selecciona archivos .fcs
    '''
    file_paths = askopenfilenames(initialdir=_user_desktop_directory, filetypes=[("FCS files", "*.fcs")]) # Abre el cuadro de diálogo para seleccionar archivos
    if file_paths != "": # Si la lista de rutas de archivo no está vacía
        if treeview.get_children(): # Si el treeview contiene alguna línea
            treeview = delete_existing_elements_treeview(treeview) # Vaciamos el treeview
        # TODO REVISAR ESTO
        # FIXME
        # BUG
        for fcs_file in file_paths:
            add_data_treeview(treeview, fcs_file) # Añadimos los datos al treeview

# Función que borra todos los elementos existentes en el treeview
def delete_existing_elements_treeview(treeview: Treeview) -> Treeview:
    '''
    Función que borra todos los elementos existentes en el treeview
    '''
    for i in treeview.get_children():
        treeview.delete(i)

    return treeview

# Función que añade los datos al treeview
def add_data_treeview(treeview: Treeview, fcs_file: str) -> Treeview:
    '''
    Función que añade los datos al treeview
    '''
    treeview.insert("", END, values = new_experiment(fcs_file))

    return treeview

# Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
def new_experiment(fcs_file: str) -> Tuple[str, int, int, str, str]:
    '''
    Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
    '''
    tube = Tube(file=fcs_file)

    import_op = ImportOp(tubes=[tube], channels={_xchannel : _xchannel, _ychannel : _ychannel, _channel : _channel})
    experiment: Experiment = import_op.apply()

    # Realizamos la operación Threshold sobre el experimento
    operation_name = "Threshold"
    threshold_op = ThresholdOp(name=operation_name, channel=_xchannel, threshold=2000)
    experiment_threshold: Experiment = threshold_op.apply(experiment)
    experiment_threshold = experiment_threshold.query(operation_name)

    # Realizamos la operación DensityGate sobre el experimento
    operation_name = "DensityGate"
    density_gate_op = DensityGateOp(name=operation_name, xchannel=_xchannel, xscale=_scale, ychannel=_ychannel, yscale=_scale, keep=0.5)
    density_gate_op.estimate(experiment_threshold)
    experiment_density_gate: Experiment = density_gate_op.apply(experiment_threshold)
    experiment_density_gate = experiment_density_gate.query(operation_name)

    # Realizamos la operación de clustering FlowPeaks sobre el experimento
    flow_peaks_op = FlowPeaksOp(name=_cluster_name, channels=[_xchannel, _ychannel], scale={_xchannel : _scale, _ychannel : _scale}, h0=3)
    flow_peaks_op.estimate(experiment_density_gate)
    experiment_flow_peaks: Experiment = flow_peaks_op.apply(experiment_density_gate)
    argmax(experiment_flow_peaks[[_cluster_name]].groupby(by=experiment_flow_peaks[_cluster_name]).count())

    # Asignamos a variables los datos que queremos retornar del experimento
    file_name = path.basename(fcs_file)
    total_number_events = experiment.data.shape[0]
    number_events_cluster_interest = experiment_flow_peaks.data.shape[0]
    percentage_represents_number_events_cluster_interest_total = "{:.2%}".format(number_events_cluster_interest / total_number_events)
    mfi_cluster_interest = "{:.2f}".format(median_fluorescence_intensity_cluster_interest(experiment_flow_peaks))
    
    # Guardamos el experimento en un diccionario, tomando como clave el nombre del fichero .fcs
    _experiment_dictionary[file_name] = experiment_flow_peaks
    
    # Retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
    return (file_name, total_number_events, number_events_cluster_interest, percentage_represents_number_events_cluster_interest_total, mfi_cluster_interest)

# Función que calcula la Intensidad Mediana de Fluorescencia (IMF) sobre el cluster de interés
def median_fluorescence_intensity_cluster_interest(experiment_flow_peaks: Experiment) -> float64:
    '''
    Función que calcula la Intensidad Mediana de Fluorescencia (IMF) sobre el cluster de interés
    '''
    # Ordenamos los datos del experimento en el canal deseado
    sorted_data = sort(experiment_flow_peaks[_channel])

    # Obtenemos el número total de datos
    total_number_data = len(sorted_data)
    
    # Si el número de datos es par
    if total_number_data % 2 == 0:
        return (sorted_data[total_number_data // 2 - 1] + sorted_data[total_number_data // 2]) / 2
    # Si el número de datos es impar
    else:
        return sorted_data[total_number_data // 2]

# Función que genera los botones
def generate_buttons(buttons_frame: Frame, canvas_frame: Frame, treeview: Treeview) -> None:
    '''
    Función que genera los botones
    '''
    # Ponemos un componente de relleno en la parte superior para poder centrar los botones verticalmente
    label1 = Label(buttons_frame)
    label1.pack(side=TOP, expand=True)
    
    # Creamos los botones
    # Botón cargar archivos
    load_files_button = Button(buttons_frame, text="Load files", command=lambda: select_fcs_files(treeview))
    load_files_button.pack(side=TOP, pady=50)

    # Botón borrar
    delete_button = Button(buttons_frame, text="Delete", command=lambda: delete_row(treeview, canvas_frame))
    delete_button.pack(side=TOP, pady=50)

    # Botón exportar
    export_button = Button(buttons_frame, text="Export", command=lambda: export_to_csv(treeview))
    export_button.pack(side=TOP, pady=50)

    # Y también ponemos otro componente de relleno en la parte inferior para poder centrar los botones verticalmente
    label2 = Label(buttons_frame)
    label2.pack(side=TOP, expand=True)

# Función que borra filas
def delete_row(treeview: Treeview, canvas_frame: Frame) -> None:
    '''
    Función que borra filas
    '''
    selected_items = treeview.selection() # Esto devuelve una lista de los ID de las filas seleccionadas
    if selected_items: # Si hay alguna fila seleccionada
        confirm = askyesno(title="Confirmation", message=f"Are you sure you want to delete {len(selected_items)} row(s)?") # Mostramos un popup para confirmar o no que queremos borrar las filas
        if confirm: # Si hemos confirmado
            for selected_item in selected_items: # Borramos las filas seleccionadas
                treeview.delete(selected_item)
        if not treeview.get_children(): # Si el treeview se ha quedado vacío
            for widget in canvas_frame.winfo_children(): # Destruimos todos los componentes del marco del canvas
                widget.destroy()
    else: # En el caso de no haber ninguna fila seleccionada
        showwarning(title="Warning", message="No row selected") # Mostramos un cuadro de diálogo de advertencia

# Función que exporta el treeview a un fichero .csv
def export_to_csv(treeview: Treeview) -> None:
    '''
    Función que exporta el treeview a un fichero .csv
    '''
    if treeview.get_children(): # Si el treeview contiene alguna línea, se exportarán los datos del treeview, sino, aparecerá una advertencia diciendo que no hay datos que exportar del treeview
        csv_file_name = "treeview.csv"
        csv_file = path.join(_user_desktop_directory, csv_file_name) # Esto une el directorio de escritorio de usuario y "treeview.csv" para formar una ruta completa donde se encuentra el archivo .csv
        with open(csv_file, "w", newline="") as file:
            file_writer = writer(file)
            file_writer.writerow(_columns) # Escribimos los nombres de las columnas
            for row_id in treeview.get_children():
                row = treeview.item(row_id)["values"]
                file_writer.writerow(row)
        showinfo(title="Info", message="The treeview was exported to a .csv file on the desktop")
    else:
        showwarning(title="Warning", message="There is no data in the treeview to export") # Mostramos un cuadro de diálogo de advertencia

# Función que muestra el canvas
def show_canvas_selected_row_treeview(canvas_frame: Frame, treeview: Treeview) -> None:
    '''
    Función que muestra el canvas
    '''
    selected_items = treeview.selection() # Esto devuelve una lista de los ID de las filas seleccionadas
    if len(selected_items) == 1:
        # Obtenemos el valor de la 1ª columna
        column_value = treeview.item(selected_items[0])["values"][0]

        # Una vez realizadas las opereaciones, pintamos la gráfica de puntos en la ventana del programa
        generate_canvas(canvas_frame, _experiment_dictionary.get(column_value))

        # Y generamos el botón por si queremos visualizar la gráfica en una ventana a parte
        generate_canvas_button(canvas_frame, _experiment_dictionary.get(column_value))
    else:
        for widget in canvas_frame.winfo_children(): # Destruimos todos los componentes del marco del canvas
            widget.destroy()

# Función que pinta los eventos del cluster en una gráfica en la ventana del programa
def generate_canvas(canvas_frame: Frame, experiment_flow_peaks: Experiment, clic_view_graph_window_button: bool=False) -> None:
    '''
    Función que pinta los eventos del cluster en una gráfica en la ventana del programa
    '''
    for widget in canvas_frame.winfo_children(): # Destruimos todos los componentes del marco del canvas
        widget.destroy()
    
    data_frame = experiment_flow_peaks.data

    # Dibujamos la gráfica de puntos
    figure, axes = subplots()

    # Dibujamos los puntos, diferenciando los clusters por color
    clusters = data_frame[_cluster_name].unique()
    for cluster in clusters:
        data_frame_cluster = data_frame[data_frame[_cluster_name] == cluster]
        axes.scatter(data_frame_cluster[_xchannel], data_frame_cluster[_ychannel], label=f"{_cluster_name} {cluster}", s=5, color="green")

    # Mostramos la leyenda
    axes.legend()
    
    # Crear el canvas de tkinter y añadir la figura de matplotlib
    figure_canvas_tk_agg = FigureCanvasTkAgg(figure, master=canvas_frame)
    figure_canvas_tk_agg.draw()
    figure_canvas_tk_agg = figure_canvas_tk_agg.get_tk_widget()
    figure_canvas_tk_agg.pack(fill=BOTH, expand=True, padx=100, pady=20)

    # Si hemos pulsado el botón de ver gráfica en ventana
    if clic_view_graph_window_button:
        show()
    
    # Cerramos la figura para que el programa no se quede pillado al cerrarlo
    close(fig=figure)

# Función que genera el botón de ver la gráfica en ventana
def generate_canvas_button(canvas_frame: Frame, experiment_flow_peaks: Experiment) -> None:
    '''
    Función que genera el botón de ver la gráfica en ventana
    '''
    # Creamos el botón ver gráfica en ventana
    view_graph_window_button = Button(canvas_frame, text="View graph in window", command=lambda: show_graph_window(canvas_frame, experiment_flow_peaks))
    view_graph_window_button.pack(side=BOTTOM, padx=10, pady=20)

# Función que muestra la gráfica en ventana
def show_graph_window(canvas_frame: Frame, experiment_flow_peaks: Experiment) -> None:
    '''
    Función que muestra la gráfica en ventana
    '''
    # Generamos el canvas y lo mostramos en una ventana
    generate_canvas(canvas_frame, experiment_flow_peaks, clic_view_graph_window_button=True)

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Ejecutamos la función principal del programa
    _main()
