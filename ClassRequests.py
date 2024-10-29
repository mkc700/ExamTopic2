# app.py
import sys
import requests
import json
from PyQt6.QtWidgets import *
class DataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        """Obtiene datos de la API y los retorna como una lista de diccionarios."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Verificar si hubo errores en la solicitud
            return response.json()  # Devolver los datos como objeto JSON
        except requests.RequestException as e:
            print(f"Error al obtener datos: {e}")
            return []  # Retorna una lista vacía en caso de error

class App(QWidget):
    def __init__(self, data_fetcher):
        super().__init__()
        self.setWindowTitle('Menú Desplegable y Tabla')
        self.setFixedSize(600, 400)

        # Obtener datos desde el DataFetcher
        self.data = data_fetcher.fetch_data()

    def initialize(self):
        """Método para configurar y mostrar la ventana de la aplicación."""
        layout = QVBoxLayout()

        # Crear el menú desplegable
        self.combo_box = QComboBox()
        self.combo_box.addItem("Seleccionar un registro")  # Opción por defecto
        for registro in self.data:
            self.combo_box.addItem(registro["nombre"], registro)  # Almacena el registro como dato asociado

        layout.addWidget(self.combo_box)

        # Crear el botón
        self.show_all_button = QPushButton('Mostrar Todos los Registros')
        self.show_all_button.clicked.connect(self.show_all_records)
        layout.addWidget(self.show_all_button)

        # Crear la tabla

        self.table = QTableWidget(self)
        self.table.setEnabled(False)
        self.table.verticalHeader().setVisible(False)



        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Color", "Precio", "Código Barra", "Nombre"])
        layout.addWidget(self.table)

        # Conectar el cambio de selección en el menú desplegable
        self.combo_box.currentIndexChanged.connect(self.show_selected_record)

        # Configurar el layout
        self.setLayout(layout)
        self.show()  # Mostrar la ventana

    def show_all_records(self):
        """Muestra todos los registros en la tabla."""
        self.populate_table(self.data)

    def show_selected_record(self):
        """Muestra solo el registro seleccionado en el menú desplegable."""
        selected_item = self.combo_box.currentData()
        if selected_item:
            self.populate_table([selected_item])

    def populate_table(self, data):
        """Llena la tabla con los datos proporcionados."""
        self.table.setRowCount(len(data))

        for i, registro in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(registro["color"]))
            self.table.setItem(i, 1, QTableWidgetItem(str(registro["precio"])))
            self.table.setItem(i, 2, QTableWidgetItem(registro["codigo_barra"]))
            self.table.setItem(i, 3, QTableWidgetItem(registro["nombre"]))

def run_app(url):
    """Función para ejecutar la aplicación completa."""
    app = QApplication(sys.argv)
    data_fetcher = DataFetcher(url)
    window = App(data_fetcher)
    window.initialize()
    sys.exit(app.exec())
