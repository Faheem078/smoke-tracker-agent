# 🔥 Smoke Tracker Agent

An AI-powered real-time smoke and fire detection system using live camera feeds. Automatically sends email alerts with annotated snapshots and timestamps when a threat is detected.

---

## 🚀 Features

- 📷 Live camera support (webcam or RTSP/IP camera)
- 🤖 Dual AI mode — Claude Vision API or YOLOv8 (local)
- 📸 Auto-saves annotated snapshots on detection
- 📧 Sends HTML email alerts with embedded image & timestamp
- ⏱️ Cooldown system to prevent alert spam
- 🧾 Local alert logging (file + SQLite)
- ⚙️ Fully configurable via `.env` file

---

## 🗂️ Project Structure

```
smoke_tracker/
├── main.py          # Main agent loop
├── camera.py        # Camera capture & frame utilities
├── detector.py      # AI detection (Claude Vision / YOLOv8)
├── alerter.py       # Email alert builder & sender
├── config.py        # All settings loaded from .env
├── .env             # Your secrets (never commit this!)
├── .env.example     # Safe template to share
├── snapshots/       # Auto-created — stores alert images
├── alerts.log       # Alert history log
└── requirements.txt # Python dependencies
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourname/smoke-tracker-agent.git
cd smoke-tracker-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your `.env` file

```bash
cp .env.example .env
# Then open .env and fill in your values
```

---

## 🔑 Environment Variables

| Variable            | Required          | Description                               |
| ------------------- | ----------------- | ----------------------------------------- |
| `ANTHROPIC_API_KEY` | Yes (Claude mode) | Your Anthropic API key                    |
| `EMAIL_USER`        | Yes               | Gmail address used to send alerts         |
| `EMAIL_PASS`        | Yes               | Gmail App Password (16-char)              |
| `ALERT_EMAIL`       | Yes               | Recipient email for alerts                |
| `CAMERA_SOURCE`     | No                | `0` for webcam, or RTSP URL               |
| `FRAME_INTERVAL`    | No                | Seconds between captures (default: `3`)   |
| `CONFIDENCE_THR`    | No                | Detection threshold 0–1 (default: `0.75`) |
| `ALERT_COOLDOWN`    | No                | Seconds between emails (default: `60`)    |
| `USE_CLAUDE`        | No                | `true` = Claude API, `false` = YOLOv8     |
| `YOLO_MODEL_PATH`   | No                | Path to YOLOv8 `.pt` model file           |

---

## 📧 Gmail App Password Setup

> Regular Gmail passwords will NOT work. You need an App Password.

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Navigate to **Security → 2-Step Verification** (must be enabled)
3. Scroll down to **App Passwords**
4. Select app: **Mail** — device: **Other (custom name)**
5. Copy the 16-character password into `EMAIL_PASS` in your `.env`

---

## ▶️ Usage

```bash
# On Windows:
.\venv\Scripts\python.exe main.py

# On Linux/macOS
.\venv\Scripts\python.exe -m streamlit run app.py
```

**Expected output:**

```
=======================================================
   🔥 Smoke Tracker Agent — Starting
   Mode     : Claude Vision
   Interval : 3s per frame
=======================================================

[2025-05-08 14:32:01] Cycle #1 — analyzing frame...
   Hazard: none      Confidence:  2%   Severity: none
   ✅ Clear

[2025-05-08 14:32:04] Cycle #2 — analyzing frame...
   Hazard: smoke     Confidence: 89%   Severity: high
   ⚠️  THREAT DETECTED — saving snapshot + sending email...
   ✅ Alert email sent to admin@yoursite.com
```

Press `Ctrl + C` to stop the agent gracefully.

---

## 🤖 AI Detection Modes

### Claude Vision (default)

Uses Anthropic's multimodal API to analyze each frame. No local GPU required. Returns structured JSON with hazard type, confidence, severity, and description.

```env
USE_CLAUDE=true
ANTHROPIC_API_KEY=sk-ant-...
```

### YOLOv8 (local, no API cost)

Runs entirely on your machine. Best used with a fine-tuned fire/smoke model.

```env
USE_CLAUDE=false
YOLO_MODEL_PATH=models/fire_smoke_yolov8n.pt
```

Fine-tuned YOLOv8 models for fire/smoke detection are available on [Roboflow Universe](https://universe.roboflow.com).

---

## 📷 Camera Configuration

| Source               | `CAMERA_SOURCE` value            |
| -------------------- | -------------------------------- |
| Built-in webcam      | `0`                              |
| Second USB camera    | `1`                              |
| IP camera (RTSP)     | `rtsp://192.168.1.10:554/stream` |
| Video file (testing) | `path/to/video.mp4`              |

---

## 📬 Alert Email Preview

When a threat is detected, recipients get:

- 🔴 Color-coded header (red = high, orange = medium, yellow = low)
- ⏰ Exact timestamp of detection
- 🚨 Hazard type (smoke / fire / both)
- 📊 Confidence percentage
- 📝 AI-generated description
- 📸 Annotated camera snapshot embedded inline

---

## 🔧 Customization Tips

**Multiple email recipients:**

```env
ALERT_EMAIL=admin@site.com,security@site.com
```

**Run 24/7 with systemd (Linux):**

```bash
sudo nano /etc/systemd/system/smoke-tracker.service
```

```ini
[Unit]
Description=Smoke Tracker Agent
After=network.target

[Service]
ExecStart=/path/to/venv/bin/python /path/to/main.py
WorkingDirectory=/path/to/smoke_tracker
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable smoke-tracker
sudo systemctl start smoke-tracker
```

---

## 📦 Requirements

```
opencv-python-headless
pillow
anthropic
ultralytics
python-dotenv
schedule
requests
torch
```

---

## 🛡️ Security Notes

- Never commit your `.env` file — it's in `.gitignore` by default
- Use Gmail App Passwords, never your real password
- Store API keys as environment variables, never hardcode them
- Snapshots folder may contain sensitive footage — secure accordingly

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙋 Author

Built with ❤️ using Python, OpenCV, and Anthropic Claude.  
Contributions and issues welcome!
