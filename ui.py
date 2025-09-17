from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit,
    QComboBox, QPushButton, QLabel, QSplitter, QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

class LiveCaptionUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("🎤 VerbaLive - Live Speech Recognition & Translation")
        self.setGeometry(100, 100, 1600, 1000)
        self.setMinimumSize(QSize(1200, 800))
        
        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(4)
        
        # Koyu tema kontrol bar
        control_bar = self.create_dark_control_bar()
        main_layout.addWidget(control_bar)
        
        # İnce ayırıcı
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setObjectName("darkSeparator")
        main_layout.addWidget(separator)
        
        # Metin alanları (ana alan) - ultra ince splitter'larla
        text_area = self.create_ultra_thin_text_areas()
        main_layout.addWidget(text_area)
        
        # Koyu durum çubuğu
        status_bar = self.create_dark_status_bar()
        main_layout.addWidget(status_bar)
        
        self.setLayout(main_layout)
    
    def create_dark_control_bar(self):
        """Koyu tema minimal kontrol bar"""
        bar = QFrame()
        bar.setObjectName("darkControlBar")
        bar.setFrameStyle(QFrame.NoFrame)
        bar.setMaximumHeight(44)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(20)
        
        # VerbaLive başlık - koyu tema
        title_label = QLabel("🎤 VerbaLive")
        title_label.setObjectName("darkTitle")
        
        # Service selection - koyu tema
        service_label = QLabel("Service")
        service_label.setObjectName("darkLabel")
        self.service_combo = QComboBox()
        self.service_combo.setObjectName("darkCombo")
        self.service_combo.addItems(["Google Translate", "DeepL"])
        self.service_combo.setMinimumWidth(140)
        self.service_combo.setMaximumHeight(28)
        
        # Language selection - koyu tema
        lang_label = QLabel("Language")
        lang_label.setObjectName("darkLabel")
        self.lang_combo = QComboBox()
        self.lang_combo.setObjectName("darkCombo")
        self.lang_combo.setMinimumWidth(150)
        self.lang_combo.setMaximumHeight(28)
        
        languages = [
            ("tr", "🇹🇷 Türkçe"), 
            ("fr", "🇫🇷 Français"), 
            ("de", "🇩🇪 Deutsch"),
            ("es", "🇪🇸 Español"), 
            ("it", "🇮🇹 Italiano"), 
            ("ru", "🇷🇺 Русский"),
            ("ja", "🇯🇵 日本語"), 
            ("zh-CN", "🇨🇳 中文"), 
            ("ar", "🇸🇦 العربية"),
            ("pt", "🇵🇹 Português"),
            ("nl", "🇳🇱 Nederlands"),
            ("ko", "🇰🇷 한국어")
        ]
        
        for code, name in languages:
            self.lang_combo.addItem(name, code)
        
        # API key input - koyu tema
        api_label = QLabel("API Key")
        api_label.setObjectName("darkLabel")
        self.deepl_key_input = QTextEdit()
        self.deepl_key_input.setObjectName("darkApiInput")
        self.deepl_key_input.setMaximumHeight(28)
        self.deepl_key_input.setMinimumWidth(280)
        self.deepl_key_input.setMaximumWidth(280)
        self.deepl_key_input.setPlaceholderText("Enter DeepL API key here...")
        self.deepl_key_input.hide()
        
        # Clear button - koyu tema
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("darkClearButton")
        self.clear_button.setMaximumHeight(28)
        self.clear_button.setMinimumWidth(80)
        
        # Layout
        layout.addWidget(title_label)
        layout.addWidget(self.create_dark_vertical_separator())
        layout.addWidget(service_label)
        layout.addWidget(self.service_combo)
        layout.addWidget(lang_label)
        layout.addWidget(self.lang_combo)
        layout.addWidget(api_label)
        layout.addWidget(self.deepl_key_input)
        layout.addStretch()
        layout.addWidget(self.clear_button)
        
        bar.setLayout(layout)
        return bar
    
    def create_dark_vertical_separator(self):
        """Koyu tema dikey ayırıcı"""
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setObjectName("darkVerticalSeparator")
        separator.setMaximumHeight(20)
        return separator
    
    def create_ultra_thin_text_areas(self):
        """Ultra ince splitter'larla metin alanları"""
        # Ana splitter - 0.5px kalınlık
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setChildrenCollapsible(False)
        main_splitter.setHandleWidth(1)  # Ultra ince
        main_splitter.setObjectName("ultraThinSplitter")
        
        # Sol panel (İngilizce) 
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(1, 1, 1, 1)
        
        self.english_text = self.create_dark_text_group(
            "🇺🇸 English Speech", 
            "Microphone audio will appear here...",
            is_source=True
        )
        left_layout.addWidget(self.english_text["group"])
        left_panel.setLayout(left_layout)
        
        # Sağ panel (Çeviriler)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(1, 1, 1, 1)
        
        # Çeviri splitter - 0.5px kalınlık
        translation_splitter = QSplitter(Qt.Vertical)
        translation_splitter.setChildrenCollapsible(False)
        translation_splitter.setHandleWidth(1)  # Ultra ince
        translation_splitter.setObjectName("ultraThinSplitter")
        
        # Anlık çeviri
        self.realtime_text = self.create_dark_text_group(
            "⚡ Live Translation", 
            "Live translations will appear here line by line..."
        )
        
        # Detaylı çeviri
        self.batch_text = self.create_dark_text_group(
            "📝 Detailed Translation", 
            "Completed sentences will appear here in detail..."
        )
        
        translation_splitter.addWidget(self.realtime_text["group"])
        translation_splitter.addWidget(self.batch_text["group"])
        translation_splitter.setSizes([400, 500])
        
        right_layout.addWidget(translation_splitter)
        right_panel.setLayout(right_layout)
        
        # Ana splitter'a ekle
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([500, 900])  # Çeviri alanı daha geniş
        
        return main_splitter
    
    def create_dark_text_group(self, title, placeholder="", is_source=False):
        """Koyu tema metin grubu"""
        group = QGroupBox(title)
        group.setObjectName("darkTextGroup")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 12, 8, 8)
        
        # Metin editörü - koyu tema
        text_edit = QTextEdit()
        text_edit.setObjectName("darkTextEditor" if not is_source else "darkSourceTextEditor")
        text_edit.setReadOnly(True)
        text_edit.setPlaceholderText(placeholder)
        
        # Font
        font = QFont("Segoe UI", 15)
        if is_source:
            font.setWeight(QFont.Medium)
        text_edit.setFont(font)
        
        # Minimum yükseklik
        text_edit.setMinimumHeight(250)
        
        layout.addWidget(text_edit)
        group.setLayout(layout)
        
        return {"group": group, "text": text_edit}
    
    def create_dark_status_bar(self):
        """Koyu tema durum çubuğu"""
        status_bar = QFrame()
        status_bar.setObjectName("darkStatusBar")
        status_bar.setFrameStyle(QFrame.NoFrame)
        status_bar.setMaximumHeight(28)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 4, 16, 4)
        
        # Durum etiketi
        status_label = QLabel("🟢 Ready - You can start speaking")
        status_label.setObjectName("darkStatusLabel")
        
        # Sürüm bilgisi
        version_label = QLabel("v2.1")
        version_label.setObjectName("darkVersionLabel")
        version_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(status_label)
        layout.addStretch()
        layout.addWidget(version_label)
        
        status_bar.setLayout(layout)
        return status_bar
