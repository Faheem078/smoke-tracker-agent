import cv2, time, os, base64
from datetime import datetime
from config import CAMERA_SOURCE, FRAME_WIDTH, FRAME_HEIGHT, SNAPSHOT_DIR

os.makedirs(SNAPSHOT_DIR, exist_ok=True)

class CameraCapture:
    def __init__(self):
        if os.name == 'nt' and isinstance(CAMERA_SOURCE, int):
            self.cap = cv2.VideoCapture(CAMERA_SOURCE, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(CAMERA_SOURCE)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    def grab_frame(self):
        """Read one frame; returns (frame_bgr, timestamp_str)."""
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Camera read failed — check CAMERA_SOURCE")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return frame, ts

    def frame_to_base64(self, frame) -> str:
        """Encode BGR frame as JPEG base64 string for API calls."""
        _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return base64.b64encode(buf).decode("utf-8")

    def save_snapshot(self, frame, label="alert") -> str:
        """Save annotated snapshot and return the file path."""
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(SNAPSHOT_DIR, f"{label}_{ts}.jpg")
        # burn timestamp onto image
        cv2.putText(frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imwrite(path, frame)
        return path

    def release(self):
        self.cap.release()
