# main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from data.crypto_api import map_symbol_to_id, fetch_market_chart
from charts.plotter import plot_price_with_indicators

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("GreenWave - Crypto Indicator Dashboard")

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
