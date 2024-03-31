from ttkbootstrap import Window, Frame, Label, Button, Treeview, Scrollbar, TOP, SUCCESS, HEADINGS, BOTH, CENTER, HORIZONTAL, VERTICAL, RIGHT, Y, BOTTOM, X, END
from tkinter.messagebox import askyesno, showwarning, showinfo
from cytoflow import Tube, ImportOp, ThresholdOp, DensityGateOp, FlowPeaksOp
from numpy import argmax, sort
from os import path
from matplotlib.pyplot import subplots, close, show
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from csv import writer
# from atexit import register

# Variables globales
_theme_name = "cyborg"
_application_title = "Tkinter experiment"
_minimum_window_width = 800
_minimum_window_height = 600
_columns = ("file_name", "total_number_events", "number_cluster_events", "percentage_number_events_total", "mfi_cluster") # Definimos las columnas del treeview
_user_directory = path.expanduser("~") # Esto obtiene el directorio de usuario
_user_desktop_directory = path.join(_user_directory, "Desktop") # Esto obtiene el directorio de escritorio de usuario
_fcs_file_name = "1.fcs"
_fcs_file = path.join(_user_desktop_directory, _fcs_file_name)
_xchannel = "R1-A"
_ychannel = "B8-A"
_scale = "log"
_channel = "B4-A"
_cluster_name = "FlowPeaks"

# Función principal del programa
def _main():
    '''
    Función principal del programa
    '''
    # Generamos la ventana del programa
    window = generate_window()
    
    # Dimensionamos y posicionamos la ventana en la pantalla
    window_size_placement(window)

    # El estado de la ventana será maximizado
    # window.state("zoomed")

    # Generamos el marco de la tabla de datos
    treeview_frame = generate_tree_view_frame(window)
    
    # Generamos la tabla de datos
    treeview = generate_treeview(window, treeview_frame)

    # Generamos los botones
    generate_buttons(window, treeview)

    # Generamos el hilo que genera la ventana del programa
    window.mainloop()

# Función que genera la ventana del programa
def generate_window():
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
def window_size_placement(window):
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

# Función que genera el marco de la tabla de datos
def generate_tree_view_frame(window):
    '''
    Función que genera el marco de la tabla de datos
    '''
    # Creamos un marco en el que generaremos el treeview
    treeview_frame = Frame(window)
    treeview_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.5)

    return treeview_frame

# Función que genera la tabla con los datos
def generate_treeview(window, treeview_frame):
    '''
    Función que genera la tabla con los datos
    '''
    # Creamos el Treeview
    treeview = Treeview(treeview_frame, bootstyle=SUCCESS, columns=_columns, show=HEADINGS) # NOTA: Para mostrar la columna #0, poner el atributo show=TREEHEADINGS
    treeview.pack(fill=BOTH, expand=True, padx=(0, 20))
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

    # Añadimos los datos al treeview
    treeview = add_data_treeview(window, treeview)

    return treeview

# Función que añade los scrollbars del treeview
def add_treeview_scrollbars(treeview_frame, treeview):
    '''
    Función que añade los scrollbars del treeview
    '''
    vertical_scrollbar = Scrollbar(treeview_frame, orient=VERTICAL, command=treeview.yview)
    horizontal_scrollbar = Scrollbar(treeview_frame, orient=HORIZONTAL, command=treeview.xview)
    treeview.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, padx=5, pady=(0, 20))
    horizontal_scrollbar.pack(side=BOTTOM, fill=X, pady=5)

# Función que añade los datos al treeview
def add_data_treeview(window, treeview):
    '''
    Función que añade los datos al treeview
    '''
    treeview.insert("", END, values=new_experiment(window, _fcs_file))
    treeview.insert("", END, values=("A"))
    treeview.insert("", END, values=("B"))
    treeview.insert("", END, values=("C"))
    treeview.insert("", END, values=("D"))
    treeview.insert("", END, values=("E"))
    treeview.insert("", END, values=("F"))
    treeview.insert("", END, values=("G"))
    treeview.insert("", END, values=("H"))
    treeview.insert("", END, values=("I"))
    treeview.insert("", END, values=("J"))
    treeview.insert("", END, values=("K"))
    treeview.insert("", END, values=("L"))
    treeview.insert("", END, values=("M"))
    treeview.insert("", END, values=("N"))
    treeview.insert("", END, values=("Ñ"))
    treeview.insert("", END, values=("O"))
    treeview.insert("", END, values=("P"))
    treeview.insert("", END, values=("Q"))
    treeview.insert("", END, values=("R"))
    treeview.insert("", END, values=("S"))
    treeview.insert("", END, values=("T"))
    treeview.insert("", END, values=("U"))
    treeview.insert("", END, values=("V"))
    treeview.insert("", END, values=("W"))
    treeview.insert("", END, values=("X"))
    treeview.insert("", END, values=("Y"))
    treeview.insert("", END, values=("Z"))

    return treeview

# Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
def new_experiment(window, fcs_file):
    '''
    Función en la que aplicamos operaciones sobre el experimento y retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
    '''
    tube = Tube(file=fcs_file)

    import_op = ImportOp(tubes=[tube], channels={_xchannel : _xchannel, _ychannel : _ychannel, _channel : _channel})
    experiment = import_op.apply()

    # Realizamos la operación Threshold sobre el experimento
    operation_name = "Threshold"
    threshold_op = ThresholdOp(name=operation_name, channel=_xchannel, threshold=2000)
    experiment_threshold = threshold_op.apply(experiment)
    experiment_threshold = experiment_threshold.query(operation_name)

    # Realizamos la operación DensityGate sobre el experimento
    operation_name = "DensityGate"
    density_gate_op = DensityGateOp(name=operation_name, xchannel=_xchannel, xscale=_scale, ychannel=_ychannel, yscale=_scale, keep=0.5)
    density_gate_op.estimate(experiment_threshold)
    experiment_density_gate = density_gate_op.apply(experiment_threshold)
    experiment_density_gate = experiment_density_gate.query(operation_name)

    # Realizamos la operación de clustering FlowPeaks sobre el experimento
    flow_peaks_op = FlowPeaksOp(name=_cluster_name, channels=[_xchannel, _ychannel], scale={_xchannel : _scale, _ychannel : _scale}, h0=3)
    flow_peaks_op.estimate(experiment_density_gate)
    experiment_flow_peaks = flow_peaks_op.apply(experiment_density_gate)
    argmax(experiment_flow_peaks[[_cluster_name]].groupby(by=experiment_flow_peaks[_cluster_name]).count())

    # Una vez realizadas las opereaciones, pintamos la gráfica de puntos en la ventana del programa
    generate_canvas(window, experiment_flow_peaks)

    # Asignamos a variables los datos que queremos retornar del experimento
    file_name = path.basename(fcs_file)
    total_number_events = experiment.data.shape[0]
    number_events_cluster_interest = experiment_flow_peaks.data.shape[0]
    percentage_represents_number_events_cluster_interest_total = "{:.2%}".format(number_events_cluster_interest / total_number_events)
    mfi_cluster_interest = "{:.2f}".format(median_fluorescence_intensity_cluster_interest(experiment_flow_peaks))
    
    # Retornamos: el nombre del fichero, el nº de eventos total, el nº de eventos del cluster de interés, el % que representa el nº de eventos del cluster de interés sobre el total y la IMF del cluster de interés
    return (file_name, total_number_events, number_events_cluster_interest, percentage_represents_number_events_cluster_interest_total, mfi_cluster_interest)

# Función que calcula la Intensidad Mediana de Fluorescencia (IMF) sobre el cluster de interés
def median_fluorescence_intensity_cluster_interest(experiment_flow_peaks):
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

# Función que genera el marco del canvas
# def generate_canvas_frame(window):
#     '''
#     Función que genera el marco del canvas
#     '''
#     # Creamos un marco en el que generaremos el canvas
#     canvas_frame = Frame(window)
#     canvas_frame.place(relx=0.2, rely=0.5, relwidth=0.8, relheight=0.5)

#     return canvas_frame

# Función que pinta los eventos del cluster en una gráfica en la ventana del programa
def generate_canvas(window, experiment_flow_peaks):
    '''
    Función que pinta los eventos del cluster en una gráfica en la ventana del programa
    '''
    # Creamos un marco en el que generaremos el canvas
    canvas_frame = Frame(window)
    canvas_frame.place(relx=0.2, rely=0.5, relwidth=0.8, relheight=0.5)

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

    # Cerramos la figura para que el programa no se quede pillado al cerrarlo
    close(fig=figure)

    # Botón "View graph in window"
    # view_graph_window_button = Button(canvas_frame, text="View graph in window", command=lambda: show_graph_window())
    # view_graph_window_button.pack(side=BOTTOM, padx=10, pady=20)

    # register(lambda: close(fig=figure))

# Función que muestra la gráfica en ventana
# def show_graph_window():
#     '''
#     Función que muestra la gráfica en ventana
#     '''
#     show()

# Función que genera los botones
def generate_buttons(window, treeview):
    '''
    Función que genera los botones
    '''
    # Creamos un frame en el que generaremos los botones
    buttons_frame = Frame(window)
    buttons_frame.place(relx=0, rely=0, relwidth=0.2, relheight=1)

    # Ponemos un componente de relleno en la parte superior para poder centrar los botones verticalmente
    label1 = Label(buttons_frame)
    label1.pack(side=TOP, expand=True)
    
    # Creamos los botones
    # Botón "Load files"
    load_files_button = Button(buttons_frame, text="Load files")
    load_files_button.pack(side=TOP, pady=50)

    # Botón "Delete"
    delete_button = Button(buttons_frame, text="Delete", command=lambda: delete_row(treeview))
    delete_button.pack(side=TOP, pady=50)

    # Botón "Export"
    export_button = Button(buttons_frame, text="Export", command=lambda: export_to_csv(treeview, _columns))
    export_button.pack(side=TOP, pady=50)

    # Ponemos un componente de relleno en la parte inferior para poder centrar los botones verticalmente
    label2 = Label(buttons_frame)
    label2.pack(side=TOP, expand=True)

# Función que borra filas
def delete_row(treeview):
    '''
    Función que borra filas
    '''
    selected_items = treeview.selection() # Esto devuelve una lista de los ID de las filas seleccionadas
    if selected_items: # Si hay alguna fila seleccionada
        confirm = askyesno(title="Confirmation", message=f"Are you sure you want to delete {len(selected_items)} row(s)?") # Mostramos un popup para confirmar o no que queremos borrar las filas
        if confirm: # Si hemos confirmado
            for selected_item in selected_items: # Borramos las filas seleccionadas
                treeview.delete(selected_item)
    else: # En el caso de no haber ninguna fila seleccionada
        showwarning(title="Warning", message="No row selected") # Mostramos un cuadro de diálogo de advertencia

# Función que exporta el treeview a un fichero .csv
def export_to_csv(treeview, columns):
    '''
    Función que exporta el treeview a un fichero .csv
    '''
    confirm = askyesno(title="Confirmation", message=f"Do you want to export the treeview in a .csv file?") # Mostramos un popup para confirmar o no que queremos el treeview en un fichero .csv
    if confirm: # Si hemos confirmado
        csv_file_name = "treeview.csv"
        csv_file = path.join(_user_desktop_directory, csv_file_name) # Esto une el directorio de escritorio de usuario y "treeview.csv" para formar una ruta completa donde se encuentra el archivo .csv
        with open(csv_file, "w", newline="") as file:
            file_writer = writer(file)
            file_writer.writerow(columns)  # Escribimos los nombres de las columnas
            for row_id in treeview.get_children():
                row = treeview.item(row_id)["values"]
                file_writer.writerow(row)
        showinfo(title="Info", message="The treeview was exported in a .csv file")

# Si el nombre del módulo es igual a __main__ se ejecutará el código (esto se hace por si queremos utilizar este código como un módulo, y no queremos que ejecute el código del main)
if __name__ == "__main__":
    # Ejecutamos la función principal del programa
    _main()
