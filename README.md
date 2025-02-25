Planificador de Procesos con Tkinter

Este proyecto es una interfaz gráfica en Python utilizando la biblioteca Tkinter para simular y comparar distintos algoritmos de planificación de procesos en sistemas operativos. La aplicación permite agregar procesos con diferentes parámetros y observar cómo se comportan bajo los algoritmos FCFS, SJF, Prioridad y un algoritmo híbrido.

Características

Implementación de los algoritmos de planificación:

First Come First Served (FCFS)

Shortest Job First (SJF)

Planificación por Prioridad

Planificación Híbrida (considera prioridad y duración)

Cálculo y visualización de:

Tiempo de Inicio

Tiempo de Finalización

Tiempo de Espera

Tiempo de Retorno

Comparación de los algoritmos con sus respectivos tiempos promedio.

Interfaz gráfica amigable con Tkinter y ttk.

Tabla para visualizar los procesos con sus tiempos.

Opción para limpiar la lista de procesos y reiniciar los cálculos.

Requisitos

Para ejecutar este proyecto necesitas:

Python 3.x

tkinter (incluido por defecto en la mayoría de las instalaciones de Python)

Instalación

Clona este repositorio o copia los archivos en tu sistema:

$ git clone https://github.com/tu_usuario/planificador-procesos.git
$ cd planificador-procesos

Uso

Ejecuta el script principal:

$ python planificador.py

Interacción con la aplicación

Añadir procesos

Ingresa el nombre del proceso.

Selecciona el algoritmo de planificación.

Especifica los valores de llegada, duración y prioridad (si aplica).

Presiona el botón "Añadir".

Comparar algoritmos

Presiona el botón "Comparar Todos" para calcular los tiempos de inicio, finalización, espera y retorno.

Limpiar la tabla

Usa el botón "Limpiar" para reiniciar la simulación.

Salir de la aplicación

Presiona el botón "Salir".

Estructura del Código

Algoritmos de planificación: Definidos como funciones que calculan los tiempos según el tipo de algoritmo.

Interfaz gráfica: Implementada en la clase ProcessSchedulerGUI.

Manejo de eventos: Métodos que actualizan la UI y procesan los datos ingresados.

Capturas de Pantalla

(Opcional: Agregar capturas de la aplicación en ejecución.)

Mejoras Futuras

Implementar algoritmos con planificación con Round Robin.

Agregar una opción para guardar los resultados en un archivo CSV o JSON.

Mejorar el diseño visual con bibliotecas como tkinter.ttk o customtkinter.

Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo y modificarlo libremente.

Desarrollado por:

1.	Esteban Xavier Bermeo Parra

2.	Josselyne Michelle Calderon Plua

3.	Patricio David Fierro Garcia

4.	Edilson Francisco Guillin Carrion

5.	Alvaro Isaac Mullo Guerrero

6.	Jorge Luis Nacipucha Garcia

