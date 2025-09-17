import sys
import time
import threading
import april_asr as april
import sounddevice as sd
import requests
import re
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QFont

from ui import LiveCaptionUI

# Google çeviri için farklı yaklaşım deneyelim
try:
    # Önce googletrans'ı yeniden yükle
    import subprocess
    import sys
    
    # googletrans'ı yeniden yükle
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--force-reinstall', 'googletrans==4.0.0rc1'])
    
    from googletrans import Translator
    GOOGLE_TRANSLATE_AVAILABLE = True
    print("Google Translate loaded successfully")
except Exception as e:
    print(f"Google Translate loading error: {e}")
    try:
        # Alternatif - eski versiyon dene
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--force-reinstall', 'googletrans==3.1.0a0'])
        from googletrans import Translator
        GOOGLE_TRANSLATE_AVAILABLE = True
        print("Google Translate loaded with fallback version")
    except:
        GOOGLE_TRANSLATE_AVAILABLE = False
        print("Google Translate completely failed to load")

try:
    import deepl
    DEEPL_AVAILABLE = True
except ImportError:
    DEEPL_AVAILABLE = False

class SimpleGoogleTranslator:
    """Basit Google Translate implementation"""
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def translate(self, text, target_lang='tr', source_lang='en'):
        try:
            # Google Translate API URL
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': source_lang,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0 and len(result[0]) > 0:
                    translated_text = ''.join([item[0] for item in result[0] if item[0]])
                    return translated_text
            
            return None
            
        except Exception as e:
            print(f"Simple Google Translate error: {e}")
            return None

class ImprovedTranslator:
    def __init__(self):
        self.google_translator = None
        self.simple_translator = SimpleGoogleTranslator()
        self.deepl_translator = None
        
    def translate(self, text, target_lang, service="Google Translate", deepl_key=""):
        if not text or not text.strip():
            return ""
            
        try:
            # Metin temizleme
            cleaned_text = self._clean_text(text)
            
            if service == "Google Translate":
                return self._google_translate(cleaned_text, target_lang)
            elif service == "DeepL" and DEEPL_AVAILABLE and deepl_key:
                return self._deepl_translate(cleaned_text, target_lang, deepl_key)
            else:
                return f"[{service} not available]"
                
        except Exception as e:
            print(f"Translation error: {e}")
            return f"[Translation error: {str(e)[:50]}...]"
    
    def _clean_text(self, text):
        # Metni temizle ve normalize et
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)  # Çoklu boşlukları tek boşluğa çevir
        return text
    
    def _google_translate(self, text, target_lang):
        # Önce basit translator'ı dene
        try:
            result = self.simple_translator.translate(text, target_lang)
            if result:
                print(f"Simple translator success: {result[:50]}...")
                return result
        except Exception as e:
            print(f"Simple translator failed: {e}")
        
        # Sonra googletrans'ı dene
        if GOOGLE_TRANSLATE_AVAILABLE:
            try:
                if self.google_translator is None:
                    self.google_translator = Translator()
                
                result = self.google_translator.translate(text, dest=target_lang, src='en')
                if result and result.text:
                    print(f"Googletrans success: {result.text[:50]}...")
                    return result.text
                    
            except Exception as e:
                print(f"Googletrans failed: {e}")
                # Yeni translator instance dene
                try:
                    self.google_translator = Translator()
                    result = self.google_translator.translate(text, dest=target_lang, src='en')
                    if result and result.text:
                        return result.text
                except Exception as e2:
                    print(f"Googletrans retry failed: {e2}")
        
        return "[Google translation failed]"
    
    def _deepl_translate(self, text, target_lang, deepl_key):
        try:
            if self.deepl_translator is None:
                self.deepl_translator = deepl.Translator(deepl_key)
            
            # DeepL dil kodlarını ayarla
            deepl_lang_map = {
                'tr': 'TR', 'fr': 'FR', 'de': 'DE', 'es': 'ES', 
                'it': 'IT', 'ru': 'RU', 'ja': 'JA', 'zh-CN': 'ZH'
            }
            deepl_target = deepl_lang_map.get(target_lang, target_lang.upper())
            
            result = self.deepl_translator.translate_text(text, target_lang=deepl_target)
            return result.text if result else "[DeepL no result]"
            
        except Exception as e:
            print(f"DeepL translation error: {e}")
            return f"[DeepL error]"

class TranslationThread(QThread):
    translation_ready = pyqtSignal(str, str, str)  # prefix, translated_text, original_text

    def __init__(self):
        super().__init__()
        self.translator = ImprovedTranslator()
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
                    self.translation_ready.emit(prefix, result, text)
                except Exception as e:
                    print(f"Translation thread error: {e}")
                    self.translation_ready.emit(prefix, f"[Translation failed]", text)
            self.msleep(100)

    def stop(self):
        self.running = False

class LiveCaptionApp(LiveCaptionUI):
    asr_ready = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setStyleSheet(open("style.css").read())

        # Gelişmiş buffer yönetimi
        self.batch_buffer = ""
        self.sentence_buffer = []  # Cümle bazında buffer
        self.last_speech_time = time.time()
        self.silence_threshold_ms = 1500  # Daha kısa sessizlik eşiği
        
        # Anlık çeviri için satır bazında takip
        self.current_sentence = ""
        self.last_translated_sentence = ""
        self.processed_sentences = set()  # Tekrar önlemek için
        self.translated_realtime_sentences = set()  # Anlık çeviri tekrarını önlemek için
        self.batch_counter = 0  # Toplu çeviri sayacı

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
        self.silence_timer.start(200)  # Daha sık kontrol

        self.init_asr()

    def init_asr(self):
        model_path = "april-english-dev-01110_en.april"
        try:
            self.model = april.Model(model_path)
        except Exception as e:
            print(f"Model loading error: {e}")
            return

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
                print(f"Audio status: {status}")
            try:
                pcm16 = (indata * 32767).astype("short").astype("<u2").tobytes()
                self.session.feed_pcm16(pcm16)
            except Exception as e:
                print(f"Audio callback error: {e}")

        sr = self.model.get_sample_rate()
        self.audio_stream = sd.InputStream(
            samplerate=sr, channels=1, dtype='float32', callback=audio_callback
        )
        self.audio_stream.start()

    def handle_asr_result(self, text, result_type):
        if result_type == "partial":
            self.current_sentence = text
            self.update_english(text, is_final=False)
        elif result_type == "final":
            self.current_sentence = text
            self.update_english(text, is_final=True)
            
            # Her final cümle için anlık çeviri yap - tekrar kontrolü ile
            if text.strip() and text not in self.translated_realtime_sentences:
                self.translate_text(text, prefix="REALTIME:")
                self.translated_realtime_sentences.add(text)
                
            # Cümleyi buffer'a ekle - toplu çeviri için
            if text.strip() and text not in self.processed_sentences:
                self.sentence_buffer.append(text.strip())
                self.batch_buffer += text + " "
                self.processed_sentences.add(text)

    def check_for_silence(self):
        if self.sentence_buffer and (time.time() - self.last_speech_time) * 1000 > self.silence_threshold_ms:
            # Biriken cümleleri toplu çeviri için gönder
            batch_text = " ".join(self.sentence_buffer)
            if batch_text.strip():
                self.batch_counter += 1
                self.translate_text(batch_text, prefix=f"BATCH:{self.batch_counter}")
                self.sentence_buffer = []
                self.batch_buffer = ""

    def translate_text(self, text, prefix):
        if not text or not text.strip():
            return
            
        service = self.service_combo.currentText()
        target_lang = self.lang_combo.currentData()
        deepl_key = self.deepl_key_input.toPlainText().strip()
        
        print(f"Starting translation: {service} -> {target_lang} : {text[:50]}...")
        self.translation_thread.add_task(text, target_lang, service, deepl_key, prefix)

    def update_english(self, text, is_final):
        cursor = self.english_text["text"].textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if not is_final:
            # Geçerli satırı temizle ve yeni metni kalın olarak ekle
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            bold_format = QTextCharFormat()
            bold_format.setFontWeight(QFont.Bold)
            bold_format.setForeground(self.english_text["text"].palette().highlight())
            cursor.insertText(text, bold_format)
        else:
            # Final metni normal format ile ekle
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            normal_format = QTextCharFormat()
            normal_format.setFontWeight(QFont.Normal)
            cursor.insertText(text + "\n", normal_format)
            
        self.english_text["text"].setTextCursor(cursor)
        self.english_text["text"].ensureCursorVisible()

    def handle_translation(self, prefix, translated_text, original_text):
        if not translated_text or translated_text.startswith("["):
            print(f"Translation failed: {translated_text}")
            return
            
        print(f"Translation completed [{prefix}]: {translated_text}")
            
        if prefix.startswith("BATCH:"):
            # Detaylı çeviri - ayırıcılarla
            cursor = self.batch_text["text"].textCursor()
            cursor.movePosition(QTextCursor.End)
            
            # Ayırıcı ekle
            separator = "━" * 50
            cursor.insertText(f"\n{separator}\n")
            cursor.insertText(f"Translation #{prefix.split(':')[1]}\n")
            cursor.insertText(f"{separator}\n")
            
            # Sadece çevrilen metni ekle
            cursor.insertText(f"{translated_text}\n\n")
            
            self.batch_text["text"].setTextCursor(cursor)
            self.batch_text["text"].ensureCursorVisible()
            
        elif prefix == "REALTIME:":
            # Anlık çeviri - her satır için
            cursor = self.realtime_text["text"].textCursor()            
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(translated_text + "\n")
                
            self.realtime_text["text"].setTextCursor(cursor)
            self.realtime_text["text"].ensureCursorVisible()

    def clear_all(self):
        """Tüm metinleri ve buffer'ları temizle"""
        self.english_text["text"].clear()
        self.realtime_text["text"].clear()
        self.batch_text["text"].clear()
        
        # Buffer'ları sıfırla
        self.batch_buffer = ""
        self.sentence_buffer = []
        self.current_sentence = ""
        self.last_translated_sentence = ""
        self.processed_sentences.clear()
        self.translated_realtime_sentences.clear()
        self.batch_counter = 0
        
        print("All data cleared")

    def closeEvent(self, event):
        """Uygulama kapatılırken temizlik işlemleri"""
        try:
            if hasattr(self, 'audio_stream'):
                self.audio_stream.stop()
                self.audio_stream.close()
                
            if hasattr(self, 'translation_thread'):
                self.translation_thread.stop()
                self.translation_thread.wait(1000)  # 1 saniye bekle
                
            if hasattr(self, 'session'):
                self.session = None
                
        except Exception as e:
            print(f"Cleanup error: {e}")
        finally:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern görünüm için
    
    window = LiveCaptionApp()
    window.show()
    
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Application terminated by user")
        window.close()
