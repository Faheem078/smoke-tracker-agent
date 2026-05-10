import smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.image     import MIMEImage
from datetime             import datetime
from config               import (SMTP_HOST, SMTP_PORT, SMTP_USER,
                                   SMTP_PASS, ALERT_RECIPIENT, ALERT_COOLDOWN)

_last_alert_time = 0   # module-level cooldown tracker

# ── Validation ──────────────────────────────────────────────
def validate_credentials():
    """Check if email credentials are properly configured."""
    errors = []
    if not SMTP_USER:
        errors.append("❌ EMAIL_USER not set in .env")
    if not SMTP_PASS:
        errors.append("❌ EMAIL_PASS not set in .env (or empty after stripping spaces)")
    if not ALERT_RECIPIENT:
        errors.append("❌ ALERT_EMAIL not set in .env")
    if len(SMTP_PASS) < 16 and SMTP_PASS:
        errors.append(f"⚠️  EMAIL_PASS appears short ({len(SMTP_PASS)} chars). Gmail App Passwords should be 16 chars (without spaces).")
    
    if errors:
        print("\n[alerter] Configuration Errors:")
        for err in errors:
            print(f"         {err}")
        print("\n[alerter] Please check your .env file and follow the setup guide in readme.md\n")
        return False
    
    print(f"[alerter] ✅ Credentials validated:")
    print(f"         From: {SMTP_USER}")
    print(f"         To:   {ALERT_RECIPIENT}")
    print(f"         Pass: {'*' * (len(SMTP_PASS) - 4)}{SMTP_PASS[-4:]}")
    return True

SEVERITY_COLOR = {
    "low":    "#f0ad4e",
    "medium": "#e67e22",
    "high":   "#e74c3c",
    "none":   "#27ae60"
}

def _build_html(result: dict, timestamp: str, image_cid: str) -> str:
    color = SEVERITY_COLOR.get(result.get("severity","none"), "#888")
    return f"""
<html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto">
  <div style="background:{color};color:#fff;padding:20px;border-radius:8px 8px 0 0">
    <h2 style="margin:0">🔥 Fire / Smoke Alert Detected</h2>
    <p style="margin:4px 0 0;opacity:.9">Severity: <strong>{result.get('severity','?').upper()}</strong></p>
  </div>
  <div style="border:1px solid #ddd;border-top:none;padding:20px;border-radius:0 0 8px 8px">
    <table style="width:100%;border-collapse:collapse">
      <tr><td style="padding:6px;font-weight:bold;width:140px">⏰ Time</td>
          <td style="padding:6px">{timestamp}</td></tr>
      <tr style="background:#f9f9f9">
          <td style="padding:6px;font-weight:bold">🚨 Hazard type</td>
          <td style="padding:6px">{result.get('hazard_type','?').capitalize()}</td></tr>
      <tr><td style="padding:6px;font-weight:bold">📊 Confidence</td>
          <td style="padding:6px">{result.get('confidence',0):.0%}</td></tr>
      <tr style="background:#f9f9f9">
          <td style="padding:6px;font-weight:bold">📝 Description</td>
          <td style="padding:6px">{result.get('description','')}</td></tr>
    </table>
    <h3 style="margin-top:20px">📸 Snapshot</h3>
    <img src="cid:{image_cid}" style="width:100%;border-radius:4px;border:1px solid #ddd"/>
    <p style="color:#888;font-size:12px;margin-top:16px">
      Automated alert from Smoke Tracker Agent — {timestamp}
    </p>
  </div>
</body></html>"""


def send_alert(result: dict, snapshot_path: str, timestamp: str) -> bool:
    """Send email alert. Returns True if sent, False if skipped (cooldown)."""
    global _last_alert_time
    
    # Validate credentials before attempting to send
    if not validate_credentials():
        return False
    
    now = time.time()
    if now - _last_alert_time < ALERT_COOLDOWN:
        print(f"[alerter] ⏱️  Cooldown active — skipping email ({ALERT_COOLDOWN}s)")
        return False

    msg = MIMEMultipart("related")
    msg["Subject"] = (f"🔥 ALERT [{result.get('severity','?').upper()}] "
                      f"Smoke/Fire detected — {timestamp}")
    msg["From"]    = SMTP_USER
    msg["To"]      = ALERT_RECIPIENT

    cid = "snapshot001"
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText("Fire/Smoke alert triggered. See attached image.", "plain"))
    alt.attach(MIMEText(_build_html(result, timestamp, cid), "html"))
    msg.attach(alt)

    # attach snapshot image
    with open(snapshot_path, "rb") as f:
        img = MIMEImage(f.read(), name="snapshot.jpg")
        img.add_header("Content-ID", f"<{cid}>")
        img.add_header("Content-Disposition", "inline", filename="snapshot.jpg")
        msg.attach(img)

    try:
        print(f"[alerter] 🔗 Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
            print(f"[alerter] 🔒 Starting TLS encryption...")
            s.starttls()
            print(f"[alerter] 🔑 Authenticating as {SMTP_USER}...")
            s.login(SMTP_USER, SMTP_PASS)
            print(f"[alerter] 📧 Sending email to {ALERT_RECIPIENT}...")
            s.sendmail(SMTP_USER, ALERT_RECIPIENT, msg.as_string())
        _last_alert_time = now
        print(f"[alerter] ✅ Alert email sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"[alerter] ❌ Authentication Failed: {e}")
        print(f"[alerter]    Check your EMAIL_USER and EMAIL_PASS in .env")
        print(f"[alerter]    Gmail App Password should be 16 chars (no spaces)")
        print(f"[alerter]    See: https://support.google.com/accounts/answer/185833")
        return False
    except smtplib.SMTPException as e:
        print(f"[alerter] ❌ SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"[alerter] ❌ Unexpected error: {e}")
        return False
