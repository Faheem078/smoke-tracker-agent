import os
from dotenv import load_dotenv

load_dotenv()

# ── Camera ──────────────────────────────────────────────
_cam_src = os.getenv("CAMERA_SOURCE", "0")
CAMERA_SOURCE   = int(_cam_src) if _cam_src.isdigit() else _cam_src          # 0 = webcam | "rtsp://..." for IP cam
FRAME_INTERVAL  = 3          # seconds between captures
FRAME_WIDTH     = 640
FRAME_HEIGHT    = 480
SNAPSHOT_DIR    = "snapshots"

# ── AI Detection ────────────────────────────────────────
USE_CLAUDE      = False      # True = Claude Vision | False = YOLOv8/YOLOv12
ANTHROPIC_KEY   = os.getenv("ANTHROPIC_API_KEY")
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "models/yolov12n-fire.pt")
CONFIDENCE_THR  = 0.45       # 0.0 – 1.0  (alert only if above this)

# ── Email Alert ─────────────────────────────────────────
SMTP_HOST       = "smtp.gmail.com"
SMTP_PORT       = 587
SMTP_USER       = os.getenv("EMAIL_USER", "").strip()        # your Gmail
SMTP_PASS       = os.getenv("EMAIL_PASS", "").strip().replace(" ", "")  # Gmail App Password (no spaces)
ALERT_RECIPIENT = os.getenv("ALERT_EMAIL", "").strip()       # where to send alerts
ALERT_COOLDOWN  = 60         # seconds — prevent spam alerts

# ── Logging ─────────────────────────────────────────────
LOG_FILE        = "alerts.log"
DB_FILE         = "alerts.db"
