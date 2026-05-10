import time, signal, sys, winsound
from camera   import CameraCapture
from detector import get_detector, is_threat
from alerter  import send_alert
from config   import FRAME_INTERVAL, USE_CLAUDE
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

running = True

def shutdown(sig, frame):
    global running
    print("\n[main] Shutting down...")
    running = False

signal.signal(signal.SIGINT,  shutdown)
signal.signal(signal.SIGTERM, shutdown)

def run():
    print("=" * 55)
    print("   🔥 Smoke Tracker Agent — Starting")
    print(f"   Mode     : {'Claude Vision' if USE_CLAUDE else 'YOLO Local (v8/v12)'}")
    print(f"   Interval : {FRAME_INTERVAL}s per frame")
    print("=" * 55)

    cam      = CameraCapture()
    detector = get_detector()
    cycle    = 0

    while running:
        cycle += 1
        try:
            frame, ts = cam.grab_frame()
            print(f"\n[{ts}] Cycle #{cycle} — analyzing frame...")

            # ── Run AI detection ────────────────────────────────
            if USE_CLAUDE:
                b64 = cam.frame_to_base64(frame)
                result = detector.analyze(b64)
            else:
                result = detector.analyze(frame)

            conf = result.get("confidence", 0)
            haz  = result.get("hazard_type", "none")
            sev  = result.get("severity", "none")
            print(f"   Hazard: {haz:8s}  Confidence: {conf:.0%}  Severity: {sev}")

            # ── Trigger alert if threat ──────────────────────────
            if is_threat(result):
                print(f"   ⚠️  THREAT DETECTED — saving snapshot + sending email...")
                try:
                    winsound.Beep(1000, 1500)  # 1000Hz for 1500ms
                except Exception:
                    pass  # Fallback if audio fails
                path = cam.save_snapshot(frame, label=haz)
                send_alert(result, path, ts)
            else:
                print("   ✅ Clear")

        except Exception as e:
            print(f"[main] Error: {e}")

        time.sleep(FRAME_INTERVAL)

    cam.release()
    print("[main] Agent stopped.")

if __name__ == "__main__":
    run()
