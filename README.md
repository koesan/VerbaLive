# 🎤 VerbaLive - Real-Time Speech Recognition and Translation System

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-v5.15+-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

https://github.com/user-attachments/assets/ac5eac05-d56e-4669-a32d-8e81beaa1e6c

[▶demo video](video/video.mp4)

**Gerçek zamanlı İngilizce konuşma tanıma ve çok dilli çeviri sistemi**

*Real-time English speech recognition and multilingual translation system*

[🇹🇷 Türkçe](#türkçe) | [🇺🇸English](#english)

</div>

---

## English

### 🇺🇸

### 🌟 Overview

VerbaLive is an advanced desktop application that can listen to **any sound your microphone can capture**. Whether it's your own voice, someone speaking in the room, a video playing on your computer, or voices from online meetings, it instantly converts English speech to text and translates it into your desired language.

### ✨ Key Features

#### 🎯 Advanced Speech Recognition

* **Offline ASR**: Works without internet using the April-ASR model
* **Real-Time**: Speech is transcribed instantly on screen
* **Smart Detection**: Partial and final results are shown in different formats
* **High Accuracy**: Trained with numbers and punctuation for precise transcription

#### 🌍 Multilingual Translation System

* **Dual Engine**: Supports both Google Translate and DeepL
* **12+ Languages**: Includes Turkish, French, German, Spanish, and more
* **Live Translation**: Line-by-line real-time translation
* **Detailed Translation**: Full sentences are translated once the speaker pauses

#### 🎨 Modern Interface

* Clear, user-friendly design that adapts to different screen sizes

#### 🔧 Advanced Features

* Sentence-based processing, silence detection, and high-performance low-latency translation

### 📦 Installation

#### Step 1: Download Project
```bash
git clone https://github.com/your-username/VerbaLive.git
cd VerbaLive
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv verbaenv
verbaenv\Scripts\activate

# macOS/Linux
python3 -m venv verbaenv
source verbaenv/bin/activate
```

#### Step 3: Install System Dependencies

**Windows:**
```bash
# With Chocolatey
choco install portaudio

# Or manual download may be required
```

**macOS:**
```bash
brew install portaudio
```

**Ubuntu/Debian based**

```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyqt5 python3-pyqt5.qtmultimedia
```
 
**Arch Based**

```bash
sudo pacman -Syu
sudo pacman -S portaudio python-pyqt5 python-pyqt5-multimedia
```

**Fedora Based**

```bash
sudo dnf update
sudo dnf install portaudio-devel python3-qt5 python3-qt5-multimedia
```

#### Step 4: Install Python Packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 5: Download ASR Model
1. Visit [April-ASR Model Page](https://abb128.github.io/april-asr/models.html)
2. Download `april-english-dev-01110_en.april` file
3. Place the downloaded file in the project root directory (same folder as `app.py`)

### 🎯 Usage

#### Basic Usage
```bash
python app.py
```

#### Interface Usage

1. **Select Translation Service**
   - Google Translate (free, no API key required)
   - DeepL (higher quality, API key required)

2. **Choose Target Language**
   - 12+ language options(Visual representation with flags)

3. **DeepL Usage** (optional)
   - Create [DeepL API](https://www.deepl.com/en/pro-api) account
   - Enter your API key in the interface

4. **Start Speaking**
   - Microphone automatically becomes active
   - Speak in English or play English audio
   - Text starts appearing instantly

#### Text Areas

**🇺🇸 English Speech:** Real-time transcription of microphone input

**⚡ Instant Translation:** Line-by-line live translation of ongoing speech

**📝 Detailed Translation:** After a 2-second pause, the entire completed speech is fully translated

### 🛠️ Advanced Configuration

#### Translation Engine Settings
```python
# Configurable settings in app.py
self.silence_threshold_ms = 1500  # Silence threshold (ms)
self.realtime_timer.start(500)   # Live translation frequency (ms)
```

### 🔧 Troubleshooting

#### Common Issues

**1. Microphone Not Detected**
```bash
# Windows
Check microphone permission in sound settings

# macOS
System Preferences > Security & Privacy > Privacy > Microphone

# Linux
pulseaudio --check && echo "PulseAudio running"
```

**2. Google Translate "[Google not available]" Error**
```bash
Solution 1: Check your internet connection
Solution 2: Reinstall googletrans package
pip uninstall googletrans
pip install googletrans==3.1.0a0
```

---

## Türkçe

### 🇹🇷

### 🌟 Genel Bakış

VerbaLive, mikrofonunuzdan gelen **her türlü sesi** dinleyebilen gelişmiş bir masaüstü uygulamasıdır. Kendi sesiniz, odadaki başka birinin konuşması, bilgisayardan çalan bir video veya çevrim içi toplantılardan gelen sesleri anlık olarak metne dönüştürür ve istediğiniz dile çevirir.

### ✨ Temel Özellikler

#### 🎯 Gelişmiş Konuşma Tanıma

* **Çevrimdışı ASR**: April-ASR modeli ile internet bağlantısı olmadan çalışır
* **Gerçek Zamanlı**: Konuşma anında metin ekrana yansır
* **Akıllı Algılama**: Kısmi ve final sonuçlar ayrı formatlarda gösterilir
* **Yüksek Doğruluk**: Sayılar ve noktalama işaretleri dahil kapsamlı eğitim

#### 🌍 Çok Dilli Çeviri Sistemi

* **Çifte Motor**: Google Translate ve DeepL desteği
* **12+ Dil Desteği**: Türkçe, Fransızca, Almanca, İspanyolca ve diğerleri
* **Anlık Çeviri**: Satır satır gerçek zamanlı çeviri
* **Detaylı Çeviri**: Konuşma tamamlandığında kapsamlı çeviri

#### 🎨 Modern Arayüz

* Okunabilir, kullanıcı dostu ve farklı ekran boyutlarına uyumlu tasarım

#### 🔧 Gelişmiş Özellikler

* Cümle bazlı işlem, sessizlik algılama ve düşük gecikmeli yüksek performanslı çeviri

### 📦 Kurulum

#### Adım 1: Projeyi İndirin
```bash
git clone https://github.com/your-username/VerbaLive.git
cd VerbaLive
```

#### Adım 2: Sanal Ortam Oluşturun
```bash
# Windows
python -m venv verbaenv
verbaenv\Scripts\activate

# macOS/Linux
python3 -m venv verbaenv
source verbaenv/bin/activate
```

#### Adım 3: Sistem Bağımlılıklarını Yükleyin

**Windows:**
```bash
# Chocolatey ile
choco install portaudio

# Veya manuel indirme gerekebilir
```

**macOS:**
```bash
brew install portaudio
```

**Ubuntu/Debian based**

```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyqt5 python3-pyqt5.qtmultimedia
```
 
**Arch Based**

```bash
sudo pacman -Syu
sudo pacman -S portaudio python-pyqt5 python-pyqt5-multimedia
```

**Fedora Based**

```bash
sudo dnf update
sudo dnf install portaudio-devel python3-qt5 python3-qt5-multimedia
```

#### Adım 4: Python Paketlerini Yükleyin
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Adım 5: ASR Modelini İndirin
1. [April-ASR Model Sayfası](https://abb128.github.io/april-asr/models.html) adresini ziyaret edin
2. `april-english-dev-01110_en.april` dosyasını indirin
3. İndirilen dosyayı proje ana dizinine (`app.py` ile aynı klasöre) yerleştirin

### 🎯 Kullanım

#### Temel Kullanım
```bash
python app.py
```

#### Arayüz Kullanımı

1. **Çeviri Servisi Seçin**
   - Google Translate (ücretsiz, API anahtarı gerektirmez)
   - DeepL (daha kaliteli, API anahtarı gerektirir)

2. **Hedef Dili Seçin**
   - 12+ dil seçeneği(Bayraklı görsel gösterim)
  
3. **DeepL Kullanımı** (isteğe bağlı)
   - [DeepL API](https://www.deepl.com/en/pro-api) hesabı oluşturun
   - API anahtarınızı arayüzde ilgili alana girin

4. **Konuşmaya Başlayın**
   - Mikrofonunuz otomatik olarak aktif olur
   - İngilizce konuşun veya İngilizce ses çalın
   - Metinler anında görünmeye başlar

#### Metin Alanları

**🇺🇸 İngilizce Konuşma:** Mikrofonla alınan sesin metne anlık dönüşümü

**⚡ Anlık Çeviri:** Sesin satır satır gerçek zamanlı çevirisi

**📝 Detaylı Çeviri:** Konuşma tamamlanınca 2 saniyelik duraklamadan sonra tüm konuşmanın kapsamlı çevirisi

### 🛠️ Gelişmiş Yapılandırma

#### Çeviri Motoru Ayarları
```python
# app.py içinde değiştirilebilir ayarlar
self.silence_threshold_ms = 1500  # Sessizlik eşiği (ms)
self.realtime_timer.start(500)   # Anlık çeviri sıklığı (ms)
```

### 🔧 Sorun Giderme

#### Sık Karşılaşılan Sorunlar

**1. Mikrofon Algılanmıyor**
```bash
# Windows
Ses ayarlarından mikrofon iznini kontrol edin

# macOS
Sistem Tercihleri > Güvenlik ve Gizlilik > Gizlilik > Mikrofon

# Linux
pulseaudio --check && echo "PulseAudio çalışıyor"
```

**2. Google Translate "[Google not available]" Hatası**
```bash
Çözüm 1: İnternet bağlantınızı kontrol edin
Çözüm 2: googletrans paketini yeniden yükleyin
pip uninstall googletrans
pip install googletrans==3.1.0a0
```

---

### 🙏 Acknowledgments

- **April-ASR**: Offline speech recognition engine

---

### 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.
