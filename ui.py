from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit,
    QComboBox, QPushButton, QLabel, QSplitter
)
from PyQt5.QtCore import Qt

class LiveCaptionUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Canlı Altyazı")
        self.setGeometry(100, 100, 1200, 700)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        # Kontrol paneli
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)

        # Metin alanları
        splitter = QSplitter(Qt.Vertical)

        self.english_text = self.create_text_group("İngilizce")
        self.realtime_text = self.create_text_group("Anlık Çeviri")
        self.batch_text = self.create_text_group("Toplu Çeviri")

        splitter.addWidget(self.english_text["group"])
        splitter.addWidget(self.realtime_text["group"])
        splitter.addWidget(self.batch_text["group"])
        splitter.setSizes([300, 300, 400])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def create_control_panel(self):
        panel = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 4, 8, 4)

        layout.addWidget(QLabel("Hizmet:"))
        self.service_combo = QComboBox()
        self.service_combo.addItems(["Google", "DeepL"])
        layout.addWidget(self.service_combo)

        layout.addWidget(QLabel("Dil:"))
        self.lang_combo = QComboBox()
        languages = [
            ("tr", "Türkçe"), ("fr", "Fransızca"), ("de", "Almanca"),
            ("es", "İspanyolca"), ("it", "İtalyanca"), ("ru", "Rusça"),
            ("ja", "Japonca"), ("zh-CN", "Çince (Basitleştirilmiş)"), ("ar", "Arapça")
        ]
        for code, name in languages:
            self.lang_combo.addItem(name, code)
        layout.addWidget(self.lang_combo)

        self.clear_button = QPushButton("Temizle")
        layout.addWidget(self.clear_button)

        self.deepl_key_input = QTextEdit()
        self.deepl_key_input.setMaximumHeight(25)
        self.deepl_key_input.setPlaceholderText("DeepL API key")
        self.deepl_key_input.hide()
        layout.addWidget(self.deepl_key_input)

        layout.addStretch()
        panel.setLayout(layout)
        return panel

    def create_text_group(self, title):
        group = QGroupBox(title)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        group.setLayout(layout)
        return {"group": group, "text": text_edit}
