
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QComboBox,
                             QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QSizePolicy)


class App(QWidget):
    def __init__(self, data_fetcher):
        super().__init__()
        self.setWindowTitle('Galletas')
        self.setFixedSize(600, 400)
        self.data_fetcher = data_fetcher  # Guardamos la referencia al data_fetcher
        self.load_initial_data()

    def load_initial_data(self):
        """Carga los datos iniciales y actualiza el combo box"""
        self.data = self.data_fetcher.fetch_data()

    def update_combo_box(self):
        """Actualiza el contenido del combo box con los datos más recientes"""
        self.combo_box.clear()
        self.combo_box.addItem("Seleccionar un registro")
        for registro in self.data:
            self.combo_box.addItem(registro["nombre"], registro)

    def initialize(self):
        """Método para configurar y mostrar la ventana de la aplicación."""
        layout = QVBoxLayout()

        # Crear el menú desplegable
        self.combo_box = QComboBox()
        self.update_combo_box()  # Inicializar el combo box con los datos

        layout.addWidget(self.combo_box)

        # Crear el botón
        self.show_all_button = QPushButton('Mostrar Todos los Registros')
        self.show_all_button.clicked.connect(self.refresh_and_show_all)
        layout.addWidget(self.show_all_button)

        # crear la tabla
        self.table = QTableWidget(self)

        # propiedades
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Numero","Nombre", "Precio", "Código Barra", "Color"])
        #tabla no editable
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.table.verticalHeader().setVisible(False)


        #agregar al layout
        layout.addWidget(self.table)


        # Conectar el cambio de selección en el menú desplegable
        self.combo_box.currentIndexChanged.connect(self.show_selected_record)

        # Configurar el layout
        self.setLayout(layout)
        self.show()  # Mostrar la ventana
        self.adjustSize()

    def refresh_and_show_all(self):
        """Actualiza los datos desde la API y muestra todos los registros."""
        self.data = self.data_fetcher.fetch_data()  # Obtener datos frescos
        self.update_combo_box()  # Actualizar el combo box con los nuevos datos
        self.populate_table(self.data)  # Mostrar los datos en la tabla

    def show_selected_record(self):
        """Muestra solo el registro seleccionado en el menú desplegable."""
        selected_item = self.combo_box.currentData()
        if selected_item:
            self.populate_table([selected_item])

    def populate_table(self, data):
        """Llena la tabla con los datos proporcionados."""
        self.table.setRowCount(len(data))

        for i, registro in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(registro["id"]))
            self.table.setItem(i, 1, QTableWidgetItem(registro["nombre"]))
            self.table.setItem(i, 2, QTableWidgetItem(str(registro["precio"])))
            self.table.setItem(i, 3, QTableWidgetItem(registro["codigo_barra"]))
            self.table.setItem(i, 4, QTableWidgetItem(registro["color"]))