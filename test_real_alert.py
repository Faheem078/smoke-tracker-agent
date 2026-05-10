"""
Real-time alert test - captures actual frames and sends real alerts with real data
"""
import os
import cv2
from datetime import datetime
from config import SNAPSHOT_DIR, CAMERA_SOURCE, FRAME_WIDTH, FRAME_HEIGHT
from alerter import send_alert, validate_credentials

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

def test_real_alert():
    print("=" * 60)
    print("🔥 REAL ALERT TEST - Capturing Live Camera Data")
    print("=" * 60)
    
    # Validate email config first
    if not validate_credentials():
        print("\n❌ Email configuration failed. Fix your .env file.")
        return False
    
    # Try to open camera
    print(f"\n[camera] Opening camera source: {CAMERA_SOURCE}")
    if isinstance(CAMERA_SOURCE, int):
        cap = cv2.VideoCapture(CAMERA_SOURCE, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(CAMERA_SOURCE)
    
    if not cap.isOpened():
        print("❌ Failed to open camera!")
        print(f"   Tried source: {CAMERA_SOURCE}")
        print(f"   Make sure your webcam is connected and not in use")
        return False
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    
    print("✅ Camera opened successfully")
    print("\n" + "=" * 60)
    print("📸 Capturing frame from camera...")
    print("=" * 60)
    
    ok, frame = cap.read()
    if not ok:
        print("❌ Failed to read frame from camera")
        cap.release()
        return False
    
    cap.release()
    
    # Save the captured frame as snapshot
    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"real_test_{ts_str}.jpg")
    
    # Burn timestamp onto frame
    cv2.putText(frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imwrite(snapshot_path, frame)
    
    print(f"✅ Frame captured and saved: {snapshot_path}")
    print(f"   Frame size: {frame.shape}")
    print(f"   Frame type: {frame.dtype}")
    
    # Create realistic alert data
    print("\n" + "=" * 60)
    print("🔥 Creating REALISTIC Alert Data")
    print("=" * 60)
    
    result = {
        "detected": True,
        "confidence": 0.92,
        "hazard_type": "fire",
        "description": "Heavy smoke detected in upper-left corner with flickering orange glow indicating active fire",
        "severity": "high"
    }
    
    ts_human = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\nAlert Details:")
    print(f"  📊 Hazard:     {result['hazard_type'].upper()}")
    print(f"  🎯 Confidence: {result['confidence']:.0%}")
    print(f"  ⚠️  Severity:   {result['severity'].upper()}")
    print(f"  📝 Description: {result['description']}")
    print(f"  ⏰ Timestamp:   {ts_human}")
    print(f"  📸 Snapshot:    {snapshot_path}")
    
    # Send the real alert with real data
    print("\n" + "=" * 60)
    print("📧 SENDING REAL ALERT WITH REAL CAMERA DATA")
    print("=" * 60)
    
    success = send_alert(result, snapshot_path, ts_human)
    
    if success:
        print("\n✅ SUCCESS! Real alert sent with actual camera frame!")
        print(f"   Check your email at: mf3250791@gmail.com")
        return True
    else:
        print("\n❌ FAILED to send real alert")
        return False


if __name__ == "__main__":
    try:
        success = test_real_alert()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
