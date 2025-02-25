import tkinter as tk
from tkinter import ttk, messagebox
import copy

# ------------------------------------------------------------------------
# ALGORITMOS DE PLANIFICACIÓN (MODIFICADOS PARA INCLUIR START Y FINISH)
# ------------------------------------------------------------------------

def fcfs(processes):
    """ Retorna (start, finish, espera, retorno) en 4 dicts. """
    procs = sorted(processes, key=lambda x: x['llegada'])
    tiempo_actual = 0

    tiempos_inicio = {}
    tiempos_final = {}
    tiempos_espera = {}
    tiempos_retorno = {}

    for p in procs:
        nombre = p['nombre']

        if tiempo_actual < p['llegada']:
            tiempo_actual = p['llegada']

        # Tiempo de Inicio
        start = tiempo_actual
        tiempos_inicio[nombre] = start

        # Tiempo de Espera = start - llegada
        espera = start - p['llegada']
        tiempos_espera[nombre] = espera

        # Tiempo de Final
        finish = start + p['duracion']
        tiempos_final[nombre] = finish

        # Tiempo de Retorno = finish - llegada
        retorno = finish - p['llegada']
        tiempos_retorno[nombre] = retorno

        # Actualizar tiempo_actual
        tiempo_actual = finish

    return tiempos_inicio, tiempos_final, tiempos_espera, tiempos_retorno


def sjf(processes):
    procs = sorted(processes, key=lambda x: x['llegada'])
    completados = []
    tiempo_actual = 0

    tiempos_inicio = {}
    tiempos_final = {}
    tiempos_espera = {}
    tiempos_retorno = {}

    while len(completados) < len(procs):
        candidatos = [p for p in procs if p['llegada'] <= tiempo_actual and p not in completados]
        if not candidatos:
            pendientes = [p for p in procs if p not in completados]
            if not pendientes:
                break
            tiempo_actual = min(pen['llegada'] for pen in pendientes)
            continue

        p_sjf = min(candidatos, key=lambda x: x['duracion'])
        nombre = p_sjf['nombre']

        # start
        start = tiempo_actual
        # si el CPU está ocioso antes de la llegada
        if start < p_sjf['llegada']:
            start = p_sjf['llegada']
        tiempos_inicio[nombre] = start

        espera = start - p_sjf['llegada']
        tiempos_espera[nombre] = espera

        finish = start + p_sjf['duracion']
        tiempos_final[nombre] = finish

        retorno = finish - p_sjf['llegada']
        tiempos_retorno[nombre] = retorno

        tiempo_actual = finish
        completados.append(p_sjf)

    return tiempos_inicio, tiempos_final, tiempos_espera, tiempos_retorno


def priority_scheduling(processes):
    procs = sorted(processes, key=lambda x: x['llegada'])
    completados = []
    tiempo_actual = 0

    tiempos_inicio = {}
    tiempos_final = {}
    tiempos_espera = {}
    tiempos_retorno = {}

    while len(completados) < len(procs):
        candidatos = [p for p in procs if p['llegada'] <= tiempo_actual and p not in completados]
        if not candidatos:
            pendientes = [p for p in procs if p not in completados]
            if not pendientes:
                break
            tiempo_actual = min(pp['llegada'] for pp in pendientes)
            continue

        p_max = max(candidatos, key=lambda x: x['prioridad'])
        nombre = p_max['nombre']

        start = tiempo_actual
        if start < p_max['llegada']:
            start = p_max['llegada']
        tiempos_inicio[nombre] = start

        espera = start - p_max['llegada']
        tiempos_espera[nombre] = espera

        finish = start + p_max['duracion']
        tiempos_final[nombre] = finish

        retorno = finish - p_max['llegada']
        tiempos_retorno[nombre] = retorno

        tiempo_actual = finish
        completados.append(p_max)

    return tiempos_inicio, tiempos_final, tiempos_espera, tiempos_retorno


def hybrid_scheduling(processes):
    procs = sorted(processes, key=lambda x: x['llegada'])
    completados = []
    tiempo_actual = 0

    tiempos_inicio = {}
    tiempos_final = {}
    tiempos_espera = {}
    tiempos_retorno = {}

    while len(completados) < len(procs):
        candidatos = [p for p in procs if p['llegada'] <= tiempo_actual and p not in completados]
        if not candidatos:
            pendientes = [p for p in procs if p not in completados]
            if not pendientes:
                break
            tiempo_actual = min(pen['llegada'] for pen in pendientes)
            continue

        # Mayor prioridad, luego menor duracion, luego menor llegada
        candidatos_ordenados = sorted(
            candidatos,
            key=lambda x: (-x['prioridad'], x['duracion'], x['llegada'])
        )
        elegido = candidatos_ordenados[0]
        nombre = elegido['nombre']

        start = tiempo_actual
        if start < elegido['llegada']:
            start = elegido['llegada']
        tiempos_inicio[nombre] = start

        espera = start - elegido['llegada']
        tiempos_espera[nombre] = espera

        finish = start + elegido['duracion']
        tiempos_final[nombre] = finish

        retorno = finish - elegido['llegada']
        tiempos_retorno[nombre] = retorno

        tiempo_actual = finish
        completados.append(elegido)

    return tiempos_inicio, tiempos_final, tiempos_espera, tiempos_retorno


# ------------------------------------------------------------------------
# CLASE PRINCIPAL DE LA INTERFAZ GRÁFICA
# ------------------------------------------------------------------------
class ProcessSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador por Algoritmo Asignado (con T.Inicio, T.Final, etc.)")
        self.root.geometry("1200x700")

        # Lista de procesos
        self.processes = []

        # Variables de entrada
        self.var_nombre = tk.StringVar()
        self.var_alg = tk.StringVar(value="FCFS")
        self.var_llegada = tk.StringVar()
        self.var_duracion = tk.StringVar()
        self.var_prioridad = tk.StringVar()

        # Algoritmos disponibles
        self.alg_list = ["FCFS", "SJF", "Prioridad", "Híbrido"]

        # Variables para mostrar promedios (Compare All)
        self.var_fcfs_wait = tk.StringVar(value="---")
        self.var_fcfs_turn = tk.StringVar(value="---")
        self.var_sjf_wait = tk.StringVar(value="---")
        self.var_sjf_turn = tk.StringVar(value="---")
        self.var_pri_wait = tk.StringVar(value="---")
        self.var_pri_turn = tk.StringVar(value="---")
        self.var_hyb_wait = tk.StringVar(value="---")
        self.var_hyb_turn = tk.StringVar(value="---")

        self.create_widgets()

    def create_widgets(self):
        # FRAME INPUT
        frame_input = tk.LabelFrame(self.root, text="Agregar Proceso")
        frame_input.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(frame_input, text="Nombre:").grid(row=0, column=0, padx=5, pady=3, sticky=tk.E)
        tk.Entry(frame_input, textvariable=self.var_nombre, width=12).grid(row=0, column=1, padx=5, pady=3)

        tk.Label(frame_input, text="Algoritmo:").grid(row=0, column=2, padx=5, pady=3, sticky=tk.E)
        combo_add = ttk.Combobox(frame_input, textvariable=self.var_alg,
                                 values=self.alg_list, state="readonly", width=10)
        combo_add.grid(row=0, column=3, padx=5, pady=3)
        combo_add.bind("<<ComboboxSelected>>", self.on_alg_selected)  # para habilitar/deshabilitar prioridad

        tk.Label(frame_input, text="Llegada:").grid(row=0, column=4, padx=5, pady=3, sticky=tk.E)
        tk.Entry(frame_input, textvariable=self.var_llegada, width=5).grid(row=0, column=5, padx=5, pady=3)

        tk.Label(frame_input, text="Duración:").grid(row=0, column=6, padx=5, pady=3, sticky=tk.E)
        tk.Entry(frame_input, textvariable=self.var_duracion, width=5).grid(row=0, column=7, padx=5, pady=3)

        tk.Label(frame_input, text="Prioridad:").grid(row=0, column=8, padx=5, pady=3, sticky=tk.E)
        self.entry_prioridad = tk.Entry(frame_input, textvariable=self.var_prioridad, width=5)
        self.entry_prioridad.grid(row=0, column=9, padx=5, pady=3)

        tk.Button(frame_input, text="Añadir", bg="#2196f3", fg="white",
                  command=self.add_process).grid(row=0, column=10, padx=8, pady=3)

        # Deshabilitar prioridad si es FCFS o SJF
        self.on_alg_selected()

        # FRAME TABLA
        frame_table = tk.LabelFrame(self.root, text="Lista de Procesos (Algoritmo Asignado)")
        frame_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Agregamos T.Inicio, T.Final, T.Espera y T.Retorno como columnas extras
        columns = ("Nombre", "Alg", "Llegada", "Duración", "Prioridad", 
                   "T.Inicio", "T.Final", "T.Espera", "T.Retorno")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)

        self.tree.column("Nombre", width=120, anchor=tk.CENTER)
        self.tree.heading("Nombre", text="Nombre")

        self.tree.column("Alg", width=80, anchor=tk.CENTER)
        self.tree.heading("Alg", text="Alg")

        self.tree.column("Llegada", width=70, anchor=tk.CENTER)
        self.tree.heading("Llegada", text="Llegada")

        self.tree.column("Duración", width=70, anchor=tk.CENTER)
        self.tree.heading("Duración", text="Duración")

        self.tree.column("Prioridad", width=70, anchor=tk.CENTER)
        self.tree.heading("Prioridad", text="Prioridad")

        self.tree.column("T.Inicio", width=70, anchor=tk.CENTER)
        self.tree.heading("T.Inicio", text="T.Inicio")

        self.tree.column("T.Final", width=70, anchor=tk.CENTER)
        self.tree.heading("T.Final", text="T.Final")

        self.tree.column("T.Espera", width=70, anchor=tk.CENTER)
        self.tree.heading("T.Espera", text="T.Espera")

        self.tree.column("T.Retorno", width=70, anchor=tk.CENTER)
        self.tree.heading("T.Retorno", text="T.Retorno")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y = ttk.Scrollbar(frame_table, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll_y.set)

        # FRAME BOTONES
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Button(frame_buttons, text="Comparar Todos", bg="#9c27b0", fg="white",
                  command=self.compare_all).pack(side=tk.LEFT, padx=5)
        tk.Label(frame_buttons, text="(Cada Algoritmo trabaja solo con sus procesos)").pack(side=tk.LEFT, padx=5)
        # Botón para limpiar la tabla y la lista de procesos
        tk.Button(frame_buttons, text="Limpiar", bg="#f44336", fg="white",
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        # Botón para salir de la aplicación
        tk.Button(frame_buttons, text="Salir", bg="#4caf50", fg="white",
                  command=self.root.destroy).pack(side=tk.LEFT, padx=5)

        # FRAME de Promedios
        frame_labels = tk.LabelFrame(self.root, text="Promedios por Algoritmo")
        frame_labels.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        row = 0
        tk.Label(frame_labels, text="FCFS - Espera:").grid(row=row, column=0, sticky=tk.E, padx=5, pady=3)
        tk.Label(frame_labels, textvariable=self.var_fcfs_wait, width=8, fg="blue").grid(row=row, column=1, padx=5, pady=3)
        tk.Label(frame_labels, text="Retorno:").grid(row=row, column=2, sticky=tk.E, padx=5, pady=3)
        tk.Label(frame_labels, textvariable=self.var_fcfs_turn, width=8, fg="blue").grid(row=row, column=3, padx=5, pady=3)

        row = 1
        tk.Label(frame_labels, text="SJF - Espera:").grid(row=row, column=0, sticky=tk.E, padx=5, pady=3)
        tk.Label(frame_labels, textvariable=self.var_sjf_wait, width=8, fg="blue").grid(row=row, column=1, padx=5, pady=3)
        tk.Label(frame_labels, text="Retorno:").grid(row=row, column=2, sticky=tk.E, padx=5, pady=3)
        tk.Label(frame_labels, textvariable=self.var_sjf_turn, width=8, fg="blue").grid(row=row, column=3, padx=5, pady=3)

        row = 2
        tk.Label(frame_labels, text="Prioridad - Espera:").grid(row=row, column=0, sticky=tk.E, padx=5, pady=3)
        tk.Label(frame_labels, textvariable=self.var_pri_wait, width=8, fg="blue").grid(row=row, column=1, padx=5, pady=3)
        tk.Label(frame_labels, text="Retorno:").grid(row=row, column=2, sticky=tk.E, padx=5, pady=3)
        tk.Label(frame_labels, textvariable=self.var_pri_turn, width=8, fg="blue").grid(row=row, column=3, padx=5, pady=3)

        row = 3
        tk.Label(frame_labels, text="Híbrido - Espera:").grid(row=row, column=0, sticky=tk.E, padx=5, pady=3)
        tk.Label(frame_labels, textvariable=self.var_hyb_wait, width=8, fg="blue").grid(row=row, column=1, padx=5, pady=3)
        tk.Label(frame_labels, text="Retorno:").grid(row=row, column=2, sticky=tk.E, padx=5, pady=3)
        tk.Label(frame_labels, textvariable=self.var_hyb_turn, width=8, fg="blue").grid(row=row, column=3, padx=5, pady=3)

    def on_alg_selected(self, event=None):
        """Habilita o deshabilita el campo Prioridad según el algoritmo."""
        algoritmo = self.var_alg.get()
        if algoritmo in ("Prioridad", "Híbrido"):
            # habilitar
            self.entry_prioridad.configure(state="normal")
        else:
            # deshabilitar
            self.entry_prioridad.configure(state="disabled")
            self.var_prioridad.set("")

    # --------------------------------------------------------------------
    #  MÉTODOS DE LÓGICA
    # --------------------------------------------------------------------
    def add_process(self):
        try:
            nombre = self.var_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre no puede quedar vacío.")
                return

            alg = self.var_alg.get()
            llegada = int(self.var_llegada.get().strip()) if self.var_llegada.get() else 0
            duracion = int(self.var_duracion.get().strip()) if self.var_duracion.get() else 1

            # Si el campo prioridad está deshabilitado, se asume 1
            if alg in ("Prioridad", "Híbrido"):
                prioridad = int(self.var_prioridad.get().strip()) if self.var_prioridad.get() else 1
            else:
                prioridad = 0  # o 1, como prefieras

            new_proc = {
                'nombre': nombre,
                'alg': alg,
                'llegada': llegada,
                'duracion': duracion,
                'prioridad': prioridad
            }

            self.processes.append(new_proc)

            # Insertar fila en Treeview con T.Inicio, T.Final, T.Espera, T.Retorno = "-"
            self.tree.insert("", "end",
                values=(nombre, alg, llegada, duracion, prioridad, "-", "-", "-", "-")
            )

            # Limpiar campos
            self.var_nombre.set("")
            self.var_llegada.set("")
            self.var_duracion.set("")
            self.var_prioridad.set("")

        except ValueError:
            messagebox.showerror("Error", "Llegada, Duración y Prioridad deben ser enteros válidos.")

    def compare_all(self):
        """
        Para cada algoritmo: toma SOLO sus procesos, ejecuta, actualiza T.Inicio, T.Final, T.Espera, T.Retorno.
        Y muestra los promedios en la parte de abajo.
        """
        # Filtrar procesos por algoritmo
        fcfs_list = [p for p in self.processes if p['alg'] == "FCFS"]
        sjf_list = [p for p in self.processes if p['alg'] == "SJF"]
        pri_list = [p for p in self.processes if p['alg'] == "Prioridad"]
        hyb_list = [p for p in self.processes if p['alg'] == "Híbrido"]

        # FCFS
        fcfs_e, fcfs_r, fcfs_start, fcfs_finish = self.run_for_algorithm(fcfs, fcfs_list)
        self.var_fcfs_wait.set(fcfs_e)
        self.var_fcfs_turn.set(fcfs_r)
        self.update_tree_rows(fcfs_start, fcfs_finish, fcfs_list, "FCFS")

        # SJF
        sjf_e, sjf_r, sjf_start, sjf_finish = self.run_for_algorithm(sjf, sjf_list)
        self.var_sjf_wait.set(sjf_e)
        self.var_sjf_turn.set(sjf_r)
        self.update_tree_rows(sjf_start, sjf_finish, sjf_list, "SJF")

        # Prioridad
        pri_e, pri_r, pri_start, pri_finish = self.run_for_algorithm(priority_scheduling, pri_list)
        self.var_pri_wait.set(pri_e)
        self.var_pri_turn.set(pri_r)
        self.update_tree_rows(pri_start, pri_finish, pri_list, "Prioridad")

        # Híbrido
        hyb_e, hyb_r, hyb_start, hyb_finish = self.run_for_algorithm(hybrid_scheduling, hyb_list)
        self.var_hyb_wait.set(hyb_e)
        self.var_hyb_turn.set(hyb_r)
        self.update_tree_rows(hyb_start, hyb_finish, hyb_list, "Híbrido")

        messagebox.showinfo("Comparación",
            "Se han calculado y actualizado los tiempos (T.Inicio, T.Final, T.Espera, T.Retorno) en la tabla.\n"
            "Promedios mostrados en la parte inferior.")

    def run_for_algorithm(self, func_alg, procs_list):
        """
        Ejecuta la función de scheduling (fcfs, sjf, priority, hybrid) sobre la lista procs_list.
        Retorna: (prom_espera_str, prom_retorno_str, dict_start, dict_finish)
        donde cada dict es {nombre: valor}.
        """
        if not procs_list:
            return ("---", "---", {}, {})

        # Copiamos la lista
        local_copy = copy.deepcopy(procs_list)
        # El algoritmo ahora retorna 4 dicts: start, finish, espera, retorno
        dict_start, dict_finish, dict_espera, dict_retorno = func_alg(local_copy)

        n = len(local_copy)
        prom_e = sum(dict_espera.values()) / n
        prom_r = sum(dict_retorno.values()) / n

        return (f"{prom_e:.2f}", f"{prom_r:.2f}", dict_start, dict_finish)

    def update_tree_rows(self, dict_start, dict_finish, procs_list, alg):
        """
        Actualiza las columnas T.Inicio, T.Final, T.Espera y T.Retorno en la tabla principal
        para cada proceso de procs_list (que pertenece a 'alg').
        Buscamos el item de la fila por nombre. 
        """
        for proc in procs_list:
            nombre = proc['nombre']
            start = dict_start.get(nombre, 0)
            finish = dict_finish.get(nombre, 0)
            # Espera
            espera = start - proc['llegada']
            # Retorno
            retorno = finish - proc['llegada']

            # Buscar la fila
            item_id = self.find_tree_item(nombre)
            if item_id:
                vals = list(self.tree.item(item_id, "values"))
                # columns = ("Nombre", "Alg", "Llegada", "Duración", "Prioridad", 
                #            "T.Inicio", "T.Final", "T.Espera", "T.Retorno")
                vals[5] = str(start)   # T.Inicio
                vals[6] = str(finish)  # T.Final
                vals[7] = str(espera)  # T.Espera
                vals[8] = str(retorno) # T.Retorno

                self.tree.item(item_id, values=vals)

    def find_tree_item(self, nombre):
        """
        Busca en el Treeview la fila cuyo 'Nombre' (columna 0) coincida con 'nombre'.
        Retorna el 'item_id' o None si no se encontró.
        """
        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            # vals[0] = Nombre
            if vals and vals[0] == nombre:
                return item
        return None

    def clear_all(self):
        """
        Limpia la lista de procesos, la tabla y resetea los promedios.
        """
        self.processes = []
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.var_fcfs_wait.set("---")
        self.var_fcfs_turn.set("---")
        self.var_sjf_wait.set("---")
        self.var_sjf_turn.set("---")
        self.var_pri_wait.set("---")
        self.var_pri_turn.set("---")
        self.var_hyb_wait.set("---")
        self.var_hyb_turn.set("---")


# ------------------------------------------------------------------------
# EJECUCIÓN
# ------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessSchedulerGUI(root)
    root.mainloop()