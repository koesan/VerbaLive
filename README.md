# VerbaLive — Real-time English Captions & Translation  

**EN:**  
VerbaLive is a simple desktop app that listens to **any sound from your microphone** — whether it's your voice, someone else's, or even a video playing — and instantly turns English speech into text.  
It uses the **April-ASR** offline speech recognition model, so it works even without an internet connection for recognition. If you want, it can also **translate** the recognized text into other languages in real-time using Google or DeepL.  

**TR:**  
VerbaLive, **mikrofonunuzdan gelen her türlü sesi** — ister kendi sesiniz, ister başkasının konuşması, hatta bilgisayarınızdan çalan bir video — anında yazıya dönüştüren basit bir masaüstü uygulamasıdır.  
**April-ASR** çevrimdışı konuşma tanıma modeli sayesinde internet olmasa bile İngilizce konuşmayı algılar. İsterseniz tanınan metni Google veya DeepL kullanarak **gerçek zamanlı olarak** başka dillere çevirebilir.  

---

## ✨ Features — Özellikler  
- **Offline recognition:** No internet needed for speech-to-text (April-ASR).  
  **TR:** Çevrimdışı konuşma tanıma (April-ASR), internet gerekmez.  
- **Real-time captions:** Shows text instantly as you speak.  
  **TR:** Konuşurken anında altyazı oluşturur.  
- **Partial & final captions:** Bold for partial text, normal for final sentences.  
  **TR:** Kısmi metinler kalın, tamamlanan cümleler normal görünür.  
- **Optional translation:** Translates recognized text into your chosen language.  
  **TR:** Tanınan metni seçtiğiniz dile çevirir.  
- **Any sound source:** Works with your voice, others’ voices, or any audio coming into your microphone.  
  **TR:** Kendi sesiniz, başkasının sesi veya mikrofona gelen herhangi bir ses ile çalışır.  

---

## 🧰 Tech & Model — Teknoloji ve Model  
- **ASR Library:** `april-asr` (import as `april_asr`)  
- **Model:** `april-english-dev-01110_en.april` — trained with numbers & punctuation  
- **Download model:** [Click here to download](https://abb128.github.io/april-asr/models.html)  
  After downloading, **place the file in your project folder next to `app.py`**.  

---

## 📦 Requirements — Gereksinimler  
- Python 3.8+  
- `april-asr`, `sounddevice`, `PyQt5`, `numpy`  
- Optional: `googletrans`, `deepl` for translations  
- **Note:** On macOS/Linux, PortAudio may need to be installed:  
  - macOS: `brew install portaudio`  
  - Ubuntu/Debian: `sudo apt-get install portaudio19-dev`  

---

## 🔧 Installation — Kurulum  
```bash
# 1) Create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Download and place the model
# From: https://abb128.github.io/april-asr/models.html
# File: april-english-dev-01110_en.april
# Put it next to app.py
```

---

## ▶️ Run — Çalıştırma  
```bash
python app.py
```  
- **EN:** Speak English or play English audio — captions will appear instantly, translations will show if enabled.  
- **TR:** İngilizce konuşun veya İngilizce ses çalın — altyazılar anında çıkar, çeviri açıksa çevrilir.  

---

## 🌍 Translation — Çeviri  
- **Google:** Works without an API key (`googletrans`)  
- **DeepL:** Requires API key (`deepl` package)  

---

## 🙏 Credits — Teşekkür  
- Based on: **LiveCaptions** by abb128  
- ASR: **april-asr** + **april-english-dev-01110_en.april**  
