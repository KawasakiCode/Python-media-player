from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget
from PySide6.QtCore import Qt

class QueueBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(250, 300)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Search bar
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Add to queue")
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #1E1E1E;
                border-radius: 20px;
                padding: 10px 15px;
                font-size: 16px;
                color: white;
                border: none;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
            """
        )
        
        # Result list (hidden by default)
        self.result_list = QListWidget(self)
        self.result_list.hide()
        self.result_list.setFixedHeight(250)
        self.result_list.setStyleSheet(
            """
            QListWidget {
                background-color: #252525;
                border-radius: 5px;
                padding: 5px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item:hover {
                background-color: #333333;
            }
            QListWidget::item:selected {
                background-color: #4A90E2;
            }
            """
        )

        # Add widgets to layout
        layout.addWidget(self.search_input, alignment = Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.result_list)
        self.setLayout(layout)