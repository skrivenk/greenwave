# ui/main_window.py

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox,
    QPushButton, QLabel, QTextEdit, QSplitter,
    QFileDialog, QMessageBox
)

from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui.styles import load_stylesheet
from data.crypto_api import map_symbol_to_id, fetch_market_chart
from charts.plotter import plot_price_with_indicators
from utils.formatter import analyze_indicators

TIMEFRAMES = {
    "1D": 1,
    "1W": 7,
    "1M": 30,
    "6M": 180,
    "1Y": 365
}

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
        splitter.setStretchFactor(1, 4)

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

        self.indicator_checkboxes = {
            "rsi": self.rsi_checkbox,
            "macd": self.macd_checkbox,
            "sma": self.sma_checkbox
        }

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
        self.refresh_btn.clicked.connect(self.refresh_data)
        self.export_btn.clicked.connect(self.export_to_pdf)

        layout.addStretch()
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.quit_btn)

        return layout

    def export_to_pdf(self):
        try:
            # Step 1: Ask where to save
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Chart to PDF",
                "",
                "PDF Files (*.pdf);;All Files (*)",
                options=options
            )

            if not file_path:
                return  # User cancelled

            # Step 2: Save chart
            self.canvas.figure.savefig(file_path)

            # Optional: Also export signal summaries
            alerts_text = self.alerts.toPlainText()
            if alerts_text:
                # Save as a companion .txt file
                txt_path = file_path.replace(".pdf", "_summary.txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(alerts_text)

            # Step 3: Notify user
            QMessageBox.information(self, "Export Complete", f"Chart saved to:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export chart:\n{str(e)}")

    def refresh_data(self):
        try:
            # Step 1: Get UI selections
            symbol = self.coin_dropdown.currentText()
            timeframe = self.timeframe_dropdown.currentText()
            days = str(TIMEFRAMES.get(timeframe, 30))

            # Step 2: Map symbol to CoinGecko ID
            coin_id = map_symbol_to_id(symbol)

            # Step 3: Fetch historical price data
            df = fetch_market_chart(coin_id, days=days)

            # Step 4: Determine selected indicators
            indicators = {k: cb.isChecked() for k, cb in self.indicator_checkboxes.items()}

            # Step 5: Generate and apply updated chart
            fig = plot_price_with_indicators(df, indicators)
            self.canvas.figure.clf()
            for ax in fig.get_axes():
                self.canvas.figure.add_subplot(ax)
            self.canvas.draw()

            # Step 6: Placeholder alerts
            messages = analyze_indicators(df)
            if messages:
                self.alerts.setPlainText("\n".join(messages))
            else:
                self.alerts.setPlainText("No indicator signals generated.")

        except Exception as e:
            self.alerts.setPlainText(f"Error: {str(e)}")
