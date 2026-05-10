import streamlit as st
import cv2
import winsound
import threading
import os
from datetime import datetime
from detector import get_detector, is_threat
from alerter import send_alert
from config import SNAPSHOT_DIR

st.set_page_config(page_title="Smoke Tracker Agent", page_icon="🔥", layout="wide")

# Initialize session state variables
if "running" not in st.session_state:
    st.session_state.running = False
if "alarm_muted" not in st.session_state:
    st.session_state.alarm_muted = False
if "cap" not in st.session_state:
    st.session_state.cap = None

@st.cache_resource
def load_model():
    return get_detector()

def play_alarm():
    try:
        # Play the downloaded custom siren audio file
        winsound.PlaySound("alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    except:
        pass

# Sidebar Layout
st.sidebar.title("Options")
mode = st.sidebar.selectbox("Select Mode", ["Live Camera", "Test Video"])
use_ml = st.sidebar.checkbox("Use ML Model", value=True)

if use_ml:
    st.sidebar.success("ML Model Loaded")

st.sidebar.markdown("---")
st.sidebar.markdown("### Alarm Control")
if st.sidebar.button("🛑 STOP ALARM"):
    st.session_state.alarm_muted = True

# Main Layout
st.markdown("### 🔥 Fire & Smoke Detection System")

col1, col2 = st.columns([1, 10])
with col1:
    if st.button("Start"):
        st.session_state.running = True
        st.session_state.alarm_muted = False
        if st.session_state.cap is not None:
            st.session_state.cap.release()
        if mode == "Live Camera":
            import os
            if os.name == 'nt':
                st.session_state.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            else:
                st.session_state.cap = cv2.VideoCapture(0)
        else:
            st.session_state.cap = cv2.VideoCapture("test_video.mp4")
        st.rerun()

with col2:
    if st.button("Stop"):
        st.session_state.running = False
        if st.session_state.cap is not None:
            st.session_state.cap.release()
            st.session_state.cap = None
        st.rerun()

# Video Placeholder
stframe = st.empty()

# Processing Loop using st.rerun
if st.session_state.running and st.session_state.cap is not None:
    try:
        ok, frame = st.session_state.cap.read()
        
        if ok:
            display_frame = frame
            
            if use_ml:
                detector = load_model()
                result = detector.analyze(frame)
                
                if "annotated_frame" in result:
                    display_frame = result["annotated_frame"]
                    
                if is_threat(result):
                    st.sidebar.error("⚠️ THREAT DETECTED")
                    
                    if not st.session_state.alarm_muted:
                        threading.Thread(target=play_alarm, daemon=True).start()
                        
                    # Save annotated snapshot
                    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                    hazard = result.get('hazard_type', 'alert')
                    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{hazard}_{ts_str}.jpg")
                    # Burn timestamp into the image before saving
                    cv2.putText(display_frame, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imwrite(snapshot_path, display_frame)
                    
                    # Send email alert (alerter has built-in cooldown to prevent spam)
                    ts_human = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    threading.Thread(target=send_alert, args=(result, snapshot_path, ts_human), daemon=True).start()
            
            display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            stframe.image(display_frame, channels="RGB", width='stretch')
            
            import time
            time.sleep(0.05)
            
            # Continuously rerun to fetch the next frame and keep the UI responsive
            st.rerun()
        else:
            st.warning("Camera stream ended or failed.")
            st.session_state.running = False
            st.session_state.cap.release()
            st.session_state.cap = None
            st.rerun()
    except Exception as e:
        st.error(f"Error in video processing loop: {str(e)}")
        st.session_state.running = False
        st.session_state.cap.release()
        st.session_state.cap = None
