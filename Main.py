import sys
from PyQt6.QtWidgets import QApplication
from DataFetcher import DataFetcher
from AppWindow import App


url = "https://671be41a2c842d92c381a4df.mockapi.io/test"  # Reemplaza con tu URL real
app = QApplication(sys.argv)
data_fetcher = DataFetcher(url)
window = App(data_fetcher)
window.initialize()
sys.exit(app.exec())



