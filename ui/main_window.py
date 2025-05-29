# ui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox,
    QPushButton, QLabel, QTextEdit, QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui.styles import load_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GreenWave - Crypto Indicator Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        self.setStyleSheet(load_stylesheet())

        self.init_ui()

    def init_ui(self):
        # Main layout using QSplitter
        splitter = QSplitter(Qt.Horizontal)
        sidebar = self.init_sidebar()
        chart_area = self.init_chart_area()

        splitter.addWidget(sidebar)
        splitter.addWidget(chart_area)
        splitter.setStretchFactor(1, 4)  # Chart area gets more space

        # Set central widget
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(self.init_footer())

        container.setLayout(layout)
        self.setCentralWidget(container)

    def init_sidebar(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Coin selection
        self.coin_dropdown = QComboBox()
        self.coin_dropdown.addItems(["BTC", "ETH", "SOL", "DOGE"])
        layout.addWidget(QLabel("Select Cryptocurrency:"))
        layout.addWidget(self.coin_dropdown)

        # Timeframe selection
        self.timeframe_dropdown = QComboBox()
        self.timeframe_dropdown.addItems(["1D", "1W", "1M", "6M", "1Y"])
        layout.addWidget(QLabel("Select Timeframe:"))
        layout.addWidget(self.timeframe_dropdown)

        # Indicator checkboxes
        layout.addWidget(QLabel("Indicators:"))
        self.rsi_checkbox = QCheckBox("RSI")
        self.macd_checkbox = QCheckBox("MACD")
        self.sma_checkbox = QCheckBox("SMA / EMA")

        layout.addWidget(self.rsi_checkbox)
        layout.addWidget(self.macd_checkbox)
        layout.addWidget(self.sma_checkbox)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def init_chart_area(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Chart placeholder
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_title("Price Chart")
        self.ax.plot([], [])  # Placeholder

        # Alerts box
        self.alerts = QTextEdit()
        self.alerts.setReadOnly(True)
        self.alerts.setPlaceholderText("Signals and alerts will appear here...")

        layout.addWidget(self.canvas)
        layout.addWidget(self.alerts)

        widget.setLayout(layout)
        return widget

    def init_footer(self):
        layout = QHBoxLayout()

        self.refresh_btn = QPushButton("Refresh Data")
        self.export_btn = QPushButton("Export Report")
        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(self.close)

        layout.addStretch()
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.quit_btn)

        return layout
