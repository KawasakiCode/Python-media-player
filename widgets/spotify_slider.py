from PySide6.QtWidgets import QSlider, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QEvent, QTimer

class Widget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Wow window")

        layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(0)
        self.slider.setValue(0)
        self.slider.setFixedHeight(20)
        self.slider.setFixedWidth(656)
        self.slider.setAttribute(Qt.WA_Hover, True)
        self.slider.installEventFilter(self)
        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_stylesheet(False)

        self.start_label = QLabel()
        self.start_label.setText("0:00")
        self.start_label.setStyleSheet("font-size: 13px; color: gray;")

        self.end_label = QLabel()
        self.end_label.setText("0:00")
        self.end_label.setStyleSheet("font-size: 13px; color: gray;")


        layout.addWidget(self.start_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.end_label)
        layout.addStretch()
        self.setLayout(layout)
        self.setFixedSize(900, 50)

    def eventFilter(self, obj, event):
        if obj == self.slider:
            if event.type() == QEvent.HoverEnter:
                self.update_stylesheet(True)
            elif event.type() == QEvent.HoverLeave:
                self.update_stylesheet(False)
        return super().eventFilter(obj, event)

    def update_stylesheet(self, hovered):
        handle_color = "white"
        subpage_color = "green" if hovered else "white"

        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: #333;
                height: 5px;
                border-radius: 2px;
            }}
            QSlider::sub-page:horizontal {{
                background: {subpage_color};
                height: 5px;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {handle_color};
                width: 11px;
                height: 11px;
                border-radius: 5px;
                margin: -3px 0;
            }}
        """)

    def update_slider(self):
        self.slider.setValue(self.slider.value() + 1)
        self.start_label.setText(self.string_text()) 

    def string_text(self):
        minutes = self.slider.value() // 60
        seconds = self.slider.value() - minutes * 60
        if seconds < 10:
            return f"{minutes}:0{seconds}"
        return f"{minutes}:{seconds}"