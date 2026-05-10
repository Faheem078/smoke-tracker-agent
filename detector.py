import anthropic, json
from config import ANTHROPIC_KEY, CONFIDENCE_THR, USE_CLAUDE, YOLO_MODEL_PATH

# ── Claude Vision detector ───────────────────────────────
class ClaudeDetector:
    PROMPT = """Analyze this camera frame for smoke or fire hazards.
Return ONLY valid JSON with this exact structure:
{
  "detected": true | false,
  "confidence": 0.0 to 1.0,
  "hazard_type": "smoke" | "fire" | "both" | "none",
  "description": "one sentence",
  "severity": "low" | "medium" | "high" | "none"
}"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    def analyze(self, b64_image: str) -> dict:
        msg = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=256,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image",
                     "source": {"type": "base64",
                                "media_type": "image/jpeg",
                                "data": b64_image}},
                    {"type": "text", "text": self.PROMPT}
                ]
            }]
        )
        raw = msg.content[0].text.strip()
        # strip markdown fences if present
        raw = raw.replace("```json","").replace("```","").strip()
        return json.loads(raw)


# ── YOLOv12/v8 detector (local, no API cost) ────────────────
class YOLODetector:
    CLASSES = {"fire": True, "smoke": True, "fire-smoke": True, "factory-smoke": True}   # adjust to your model labels

    def __init__(self, model_path=None):
        if model_path is None:
            model_path = YOLO_MODEL_PATH
        from ultralytics import YOLO
        self.model = YOLO(model_path)          # use fine-tuned fire/smoke model

    def analyze(self, frame) -> dict:
        results  = self.model(frame, verbose=False)[0]
        detected = False
        best_conf = 0.0
        h_type    = "none"

        for box in results.boxes:
            label = results.names[int(box.cls)]
            conf  = float(box.conf)
            if label.lower() in self.CLASSES and conf > best_conf:
                best_conf = conf
                detected  = True
                h_type    = label.lower()

        severity = ("none" if best_conf < 0.4
                    else "low" if best_conf < 0.6
                    else "medium" if best_conf < 0.8
                    else "high")
        return {
            "detected":    detected,
            "confidence":  round(best_conf, 3),
            "hazard_type": h_type,
            "description": f"{h_type} detected at {best_conf:.0%}" if detected else "Clear",
            "severity":    severity,
            "annotated_frame": results.plot()
        }


# ── Factory ──────────────────────────────────────────────
def get_detector():
    return ClaudeDetector() if USE_CLAUDE else YOLODetector(model_path=YOLO_MODEL_PATH)


def is_threat(result: dict) -> bool:
    return result.get("detected", False) and \
           result.get("confidence", 0) >= CONFIDENCE_THR
