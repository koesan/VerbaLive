# VerbaLive — Real-time English Captions & Translation  

**EN:**  
VerbaLive is a friendly desktop app that listens to **anything your microphone can hear** — your voice, someone speaking in the room, a video playing on your computer, or even voices from an online meeting.  
It instantly turns English speech into text using the **April-ASR** offline model, so you don’t need internet for recognition.  
If you want, it can also **translate** what’s said into other languages in real time using Google or DeepL.  

**TR:**  
VerbaLive, **mikrofonunuzun duyabildiği her sesi** — kendi sesiniz, odadaki başka birinin konuşması, bilgisayardan çalan bir video ya da çevrim içi bir toplantıdan gelen sesler — dinler.  
İngilizce konuşmayı **April-ASR** çevrimdışı modeli ile anında yazıya çevirir; tanıma için internete gerek yoktur.  
İsterseniz duyulanları Google veya DeepL kullanarak **gerçek zamanlı olarak** başka dillere çevirebilir.  

---

## ✨ What it can do — Neler yapabilir  
- **Works offline:** Speech-to-text without internet (April-ASR).  
  **TR:** İnternetsiz konuşma tanıma (April-ASR).  
- **Real-time captions:** Text appears instantly as words are spoken.  
  **TR:** Konuşma anında ekrana yansır.  
- **Partial & final captions:** Bold for live text, normal for finished sentences.  
  **TR:** Canlı metinler kalın, tamamlanan cümleler normal görünür.  
- **Optional translation:** Translate into your chosen language instantly.  
  **TR:** Tanınan metni seçtiğiniz dile anında çevirir.  
- **Hears everything:** From in-person conversations to remote meetings and videos.  
  **TR:** Yüz yüze konuşmalardan çevrim içi toplantılara ve videolara kadar her sesi işler.  

---

## 🧰 Tech & Model — Teknoloji ve Model  
- **ASR Library:** `april-asr` (Python binding for April-ASR)  
- **Model:** `april-english-dev-01110_en.april` — trained with numbers & punctuation  
- **Download model:** [Official model page](https://abb128.github.io/april-asr/models.html)  
  After downloading, **place the file in your project folder next to `app.py`**.  

---

## 📦 Requirements — Gereksinimler  
- Python 3.8+  
- `april-asr`, `sounddevice`, `PyQt5`, `numpy`  
- Optional: `googletrans`, `deepl` for translations  
- **Note:** On macOS/Linux, you may need to install PortAudio:  
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
- **EN:** Speak English, play a video, or join a meeting — captions will appear instantly, and translations will show if enabled.  
- **TR:** İngilizce konuşun, video oynatın veya toplantıya katılın — altyazılar anında çıkar, çeviri açıksa ekranda görünür.  

---

## 🌍 Translation — Çeviri  
- **Google:** Works without an API key (`googletrans`)  
- **DeepL:** Requires API key (`deepl` package)  

---

## 🙏 Credits — Teşekkür  
- Based on: **LiveCaptions** by abb128  
- ASR: **april-asr** + **april-english-dev-01110_en.april**

---

[▶ Watch the demo video](video/video.mp4)


