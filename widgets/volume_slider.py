from PySide6.QtWidgets import QSlider, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPixmap

class VolumeSlider(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Wow window")

        layout = QHBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setFixedHeight(20)
        self.slider.setFixedWidth(120)
        self.slider.setAttribute(Qt.WA_Hover, True)
        self.slider.installEventFilter(self)
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_stylesheet(False)

        self.image_label = QLabel()
        pixmap = QPixmap("Assets/volume_half.png")
        scaled_pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Scale image
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setFixedSize(25, 25)

        layout.addWidget(self.image_label)
        layout.addWidget(self.slider)
        self.setLayout(layout)
        self.setFixedSize(200, 50)

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

    def slider_value_changed(self, value):
        if value == 0:
            pixmap = QPixmap("Assets/volume_mute.png")
        elif value < 25:
            pixmap = QPixmap("Assets/volume_one.png")
        elif value < 75:
            pixmap = QPixmap("Assets/volume_half.png")
        else:
            pixmap = QPixmap("Assets/volume_max.png")
        
        if pixmap.isNull():
            print("Error: Failed to load image")
        else:
            scaled_pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)