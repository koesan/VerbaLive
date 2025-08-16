import sys
import time
import threading
import april_asr as april
import sounddevice as sd
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QFont

from ui import LiveCaptionUI

# Çeviri servisleri
try:
    from googletrans import Translator
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False

class SimpleTranslator:
    def __init__(self):
        self.google_translator = None
        self.deepl_translator = None

    def translate(self, text, target_lang, service="Google", deepl_key=""):
        try:
            if service == "Google" and GOOGLE_TRANSLATE_AVAILABLE:
                if self.google_translator is None:
                    self.google_translator = Translator()
                result = self.google_translator.translate(text, dest=target_lang)
                return result.text
            elif service == "DeepL" and DEEPL_AVAILABLE and deepl_key:
                if self.deepl_translator is None:
                    self.deepl_translator = deepl.Translator(deepl_key)
                result = self.deepl_translator.translate_text(text, target_lang=target_lang)
                return result.text
            return f"[{service} not available]"
        except Exception:
            return f"[Translation error]"

class TranslationThread(QThread):
    translation_ready = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.translator = SimpleTranslator()
        self.queue = []
        self.lock = threading.Lock()
        self.running = True

    def add_task(self, text, target_lang, service, deepl_key="", prefix=""):
        with self.lock:
            self.queue.append((text, target_lang, service, deepl_key, prefix))

    def run(self):
        while self.running:
            task = None
            with self.lock:
                if self.queue:
                    task = self.queue.pop(0)
            if task:
                text, target_lang, service, deepl_key, prefix = task
                try:
                    result = self.translator.translate(text, target_lang, service, deepl_key)
                    self.translation_ready.emit(prefix, result)
                except Exception:
                    self.translation_ready.emit(prefix, "[Translation failed]")
            self.msleep(50)

    def stop(self):
        self.running = False

class LiveCaptionApp(LiveCaptionUI):
    asr_ready = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet(open("style.css").read())

        self.batch_buffer = ""
        self.last_speech_time = time.time()
        self.silence_threshold_ms = 2000

        self.translation_thread = TranslationThread()
        self.translation_thread.translation_ready.connect(self.handle_translation)
        self.translation_thread.start()

        self.asr_ready.connect(self.handle_asr_result)

        self.clear_button.clicked.connect(self.clear_all)
        self.service_combo.currentTextChanged.connect(
            lambda s: self.deepl_key_input.show() if s == "DeepL" else self.deepl_key_input.hide()
        )

        self.silence_timer = QTimer(self)
        self.silence_timer.timeout.connect(self.check_for_silence)
        self.silence_timer.start(250)

        self.init_asr()

    def init_asr(self):
        model_path = "april-english-dev-01110_en.april"
        self.model = april.Model(model_path)

        def asr_handler(result_type, tokens):
            text = "".join(token.token for token in tokens).strip()
            if not text:
                return
            self.last_speech_time = time.time()
            if result_type == april.Result.PARTIAL_RECOGNITION:
                self.asr_ready.emit(text, "partial")
            elif result_type == april.Result.FINAL_RECOGNITION:
                self.asr_ready.emit(text, "final")

        self.session = april.Session(self.model, asr_handler, asynchronous=True)

        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            pcm16 = (indata * 32767).astype("short").astype("<u2").tobytes()
            self.session.feed_pcm16(pcm16)

        sr = self.model.get_sample_rate()
        self.audio_stream = sd.InputStream(
            samplerate=sr, channels=1, dtype='float32', callback=audio_callback
        )
        self.audio_stream.start()

    def handle_asr_result(self, text, result_type):
        if result_type == "partial":
            self.update_english(text, is_final=False)
        elif result_type == "final":
            self.update_english(text, is_final=True)
            self.batch_buffer += text + " "
            self.translate_text(text, prefix="FINAL:")

    def check_for_silence(self):
        if self.batch_buffer.strip() and (time.time() - self.last_speech_time) * 1000 > self.silence_threshold_ms:
            self.translate_text(self.batch_buffer.strip(), prefix="BATCH:")
            self.batch_buffer = ""

    def translate_text(self, text, prefix):
        service = self.service_combo.currentText()
        target_lang = self.lang_combo.currentData()
        deepl_key = self.deepl_key_input.toPlainText().strip()
        self.translation_thread.add_task(text, target_lang, service, deepl_key, prefix)

    def update_english(self, text, is_final):
        cursor = self.english_text["text"].textCursor()
        cursor.movePosition(QTextCursor.End)
        if not is_final:
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            bold_format = QTextCharFormat()
            bold_format.setFontWeight(QFont.Bold)
            cursor.insertText(text, bold_format)
        else:
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            normal_format = QTextCharFormat()
            cursor.setCharFormat(normal_format)
            cursor.insertText(text + "\n")
        self.english_text["text"].setTextCursor(cursor)
        self.english_text["text"].ensureCursorVisible()

    def handle_translation(self, prefix, translated_text):
        if prefix == "BATCH:":
            cursor = self.batch_text["text"].textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText("\n" + "="*40 + "\n")
            cursor.insertText(translated_text + "\n")
            cursor.insertText("="*40 + "\n\n")
            self.batch_text["text"].setTextCursor(cursor)
            self.batch_text["text"].ensureCursorVisible()
        elif prefix == "FINAL:":
            cursor = self.realtime_text["text"].textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(translated_text + " ")
            self.realtime_text["text"].setTextCursor(cursor)
            self.realtime_text["text"].ensureCursorVisible()

    def clear_all(self):
        self.english_text["text"].clear()
        self.realtime_text["text"].clear()
        self.batch_text["text"].clear()
        self.batch_buffer = ""

    def closeEvent(self, event):
        if hasattr(self, 'audio_stream'):
            self.audio_stream.stop()
            self.audio_stream.close()
        self.translation_thread.stop()
        self.translation_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LiveCaptionApp()
    window.show()
    sys.exit(app.exec_())
