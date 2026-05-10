# ─────────────────────────────────────────────────────────
#  Smoke Tracker Agent — Environment Variables
#  Copy this file to .env and fill in your real values.
#  NEVER commit .env to Git!
# ─────────────────────────────────────────────────────────

# ── Anthropic API (Claude Vision mode) ───────────────────
# Get your key at: https://console.anthropic.com
ANTHROPIC_API_KEY=sk-ant-your-key-here

# ── Email / SMTP (Gmail) ──────────────────────────────────
# The Gmail account that SENDS the alert emails
EMAIL_USER=yourgmail@gmail.com

# Gmail App Password (16 chars, no spaces)
# How to get one: Google Account → Security → App Passwords
EMAIL_PASS=xxxx xxxx xxxx xxxx

# The email address that RECEIVES the alerts
# Separate multiple addresses with commas
ALERT_EMAIL=receiver@example.com

# ── Camera Settings ───────────────────────────────────────
# 0         = built-in webcam
# 1         = second USB camera
# rtsp://…  = IP / network camera stream
CAMERA_SOURCE=0

# How many seconds between each captured frame
FRAME_INTERVAL=3

# ── AI Detection ─────────────────────────────────────────
# true  = use Claude Vision API (requires ANTHROPIC_API_KEY)
# false = use YOLOv8 locally   (requires YOLO_MODEL_PATH)
USE_CLAUDE=true

# Minimum confidence (0.0 – 1.0) to trigger an alert
# 0.75 means the AI must be at least 75% sure before alerting
CONFIDENCE_THR=0.75

# ── YOLOv8 Settings (only if USE_CLAUDE=false) ───────────
# Path to your fine-tuned fire/smoke YOLOv8 .pt model file
# Download models from: https://universe.roboflow.com
YOLO_MODEL_PATH=models/fire_smoke_yolov8n.pt

# ── Alert Cooldown ────────────────────────────────────────
# Minimum seconds between alert emails (prevents spam)
# 60 = at most one email per minute
ALERT_COOLDOWN=60

# ── Storage Paths (optional overrides) ───────────────────
# SNAPSHOT_DIR=snapshots
# LOG_FILE=alerts.log
# DB_FILE=alerts.db
