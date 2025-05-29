# ui/styles.py

def load_stylesheet():
    return """
        QWidget {
            background-color: #D3D3D3; /* Light Gray */
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            color: #36454F; /* Charcoal Gray */
        }

        QComboBox, QCheckBox, QPushButton, QTextEdit {
            border: 1px solid #93C572; /* Pistachio Green */
            border-radius: 5px;
            padding: 6px;
        }

        QPushButton {
            background-color: #93C572; /* Primary Green */
            color: white;
        }

        QPushButton:hover {
            background-color: #ADEBB3; /* Mint Green */
            color: #36454F;
        }

        QLabel {
            font-weight: bold;
            padding-top: 10px;
        }

        QTextEdit {
            background-color: #F5F5DC; /* Soft Beige */
        }

        QMainWindow::separator {
            background: #93C572;
            width: 1px;
        }
    """
