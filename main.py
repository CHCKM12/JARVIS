import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import urllib.parse
import time
import os

# ==========================================
# 1. PAGE SETUP & CSS INJECTION
# ==========================================
st.set_page_config(page_title="J.A.R.V.I.S. // MK-IV", layout="wide", page_icon="🤖")

st.markdown("""
<style>
    /* Dark Theme & Sci-Fi Font */
    body, .stApp {
        background-color: #02060a;
        color: #00f3ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Hide Streamlit Default UI Elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Button Styling */
    div.stButton > button {
        background-color: rgba(0, 243, 255, 0.1);
        color: #00f3ff;
        border: 1px solid #00f3ff;
        padding: 15px 40px;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #00f3ff;
        color: #02060a;
        box-shadow: 0 0 20px #00f3ff;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INITIALIZE SESSION STATE & AUDIO ENGINE
# ==========================================
if 'logs' not in st.session_state:
    st.session_state.logs =[]
if 'is_awake' not in st.session_state:
    st.session_state.is_awake = False
if 'mode' not in st.session_state:
    st.session_state.mode = "standard"

# Cache the Text-to-Speech engine so it doesn't crash Streamlit
@st.cache_resource
def get_tts_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Try to set Male voice (Windows usually has David or Ravi)
    for v in voices:
        if 'male' in v.name.lower() or 'ravi' in v.name.lower() or 'david' in v.name.lower():
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', 160) # Speed of speech
    return engine

engine = get_tts_engine()

def speak(text):
    update_logs("jarvis", text)
    engine.say(text)
    engine.runAndWait()

# ==========================================
# 3. UI LAYOUT & COMPONENTS
# ==========================================
st.markdown("<h1 style='text-align: center; color: #00f3ff; letter-spacing: 10px; text-shadow: 0 0 10px #00f3ff;'>J.A.R.V.I.S. // MK-IV</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid rgba(0, 243, 255, 0.3);'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1.5, 1])

# --- LEFT PANEL: TELEMETRY ---
with col1:
    st.markdown("<div style='color:#fff; font-weight:bold; margin-bottom:10px;'>> SYS.MONITOR</div>", unsafe_allow_html=True)
    telemetry_box = st.empty()

def update_telemetry():
    hex_val = hex(int(time.time() * 1000))[-6:].upper()
    lat = (time.time() % 100)
    html = f"""
    <div style='border: 1px solid rgba(0, 243, 255, 0.2); background: rgba(0, 243, 255, 0.05); padding: 15px; height: 350px;'>
        <div style='color: rgba(0,243,255,0.7); font-size: 0.9rem;'>[SEC_{hex_val}] LAT:{lat:.4f} // OK</div>
        <div style='color: rgba(0,243,255,0.7); font-size: 0.9rem;'>[SYS_CORE] MEM_ALLOC // STABLE</div>
        <div style='color: rgba(0,243,255,0.7); font-size: 0.9rem;'>[NET_UPLINK] PING: 12ms // ACTIVE</div>
    </div>
    """
    telemetry_box.markdown(html, unsafe_allow_html=True)

# --- CENTER PANEL: REACTOR ---
with col2:
    status_text = st.empty()
    status_text.markdown("<h3 style='text-align:center; color:#ff003c; text-shadow: 0 0 10px #ff003c;'>SYSTEM OFFLINE</h3>", unsafe_allow_html=True)
    
    # Render the CSS Reactor Animation
    st.components.v1.html("""
    <style>
        .reactor { position: relative; width: 300px; height: 300px; margin: auto; display: flex; justify-content: center; align-items: center;}
        .ring { position: absolute; border-radius: 50%; border: 2px solid transparent; }
        .ring-1 { width: 300px; height: 300px; border-top: 3px solid #00f3ff; border-left: 1px dashed #00f3ff; animation: spin 5s linear infinite; }
        .ring-2 { width: 260px; height: 260px; border-right: 4px solid #0055ff; border-bottom: 2px dotted #00f3ff; animation: spin-reverse 3s linear infinite; }
        .ring-3 { width: 220px; height: 220px; border: 1px dashed #00f3ff; animation: spin 2s linear infinite; }
        .core { width: 100px; height: 100px; background: radial-gradient(circle, #00f3ff 0%, transparent 70%); border-radius: 50%; box-shadow: 0 0 60px #00f3ff, inset 0 0 30px #fff; animation: core-pulse 1s infinite alternate; }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        @keyframes spin-reverse { 100% { transform: rotate(-360deg); } }
        @keyframes core-pulse { 0% { transform: scale(0.9); box-shadow: 0 0 20px #00f3ff; } 100% { transform: scale(1.1); box-shadow: 0 0 60px #00f3ff, inset 0 0 30px #fff; } }
    </style>
    <div class="reactor"><div class="ring ring-1"></div><div class="ring ring-2"></div><div class="ring ring-3"></div><div class="core"></div></div>
    """, height=350)

# --- RIGHT PANEL: TERMINAL LOGS ---
with col3:
    st.markdown("<div style='color:#fff; font-weight:bold; margin-bottom:10px;'>> TERMINAL LOGS</div>", unsafe_allow_html=True)
    log_box = st.empty()

def update_logs(sender, message):
    st.session_state.logs.append((sender, message))
    if len(st.session_state.logs) > 8: # Keep terminal clean
        st.session_state.logs.pop(0)
    
    log_html = "<div style='border: 1px solid rgba(0, 243, 255, 0.2); background: rgba(0, 243, 255, 0.05); padding: 15px; height: 350px; overflow-y: auto;'>"
    for s, m in st.session_state.logs:
        if s == "jarvis":
            log_html += f"<div style='color: #00f3ff; margin-bottom: 10px; font-size: 0.9rem;'><b>J.A.R.V.I.S:</b> {m}</div>"
        elif s == "user":
            log_html += f"<div style='color: #fff; margin-bottom: 10px; font-size: 0.9rem; text-align: right; font-style: italic;'><b>USER:</b> {m}</div>"
        else:
            log_html += f"<div style='color: #ff003c; margin-bottom: 10px; font-size: 0.9rem;'><b>ERROR:</b> {m}</div>"
    log_html += "</div>"
    log_box.markdown(log_html, unsafe_allow_html=True)

# Initialize blank UI
if not st.session_state.is_awake:
    telemetry_box.markdown("<div style='border: 1px solid rgba(0, 243, 255, 0.2); background: rgba(0, 243, 255, 0.05); padding: 15px; height: 350px;'><span style='color:#ff003c'>OFFLINE</span></div>", unsafe_allow_html=True)
    update_logs("jarvis", "Awaiting system initialization...")

# ==========================================
# 4. AI COMMAND LOGIC
# ==========================================
def process_command(cmd):
    cmd = cmd.lower()
    
    # 1. DICTATION MODE (Taking Notes)
    if st.session_state.mode == "dictation":
        if any(w in cmd for w in ["cancel", "stop", "band karo"]):
            speak("Note cancelled.")
            st.session_state.mode = "standard"
        else:
            # Writes note directly to your actual computer desktop/folder
            with open("Jarvis_Data.txt", "a") as f:
                f.write(cmd + "\n")
            speak("Yes sir, I have saved your note to Jarvis Data dot text.")
            st.session_state.mode = "standard"
        return True

    # 2. STANDARD COMMANDS
    if any(w in cmd for w in ["hello", "namaste", "hi", "kaise ho"]):
        speak("Hello sir. All systems are running at optimal capacity.")
        
    elif any(w in cmd for w in ["time", "samay", "baj rahe"]):
        t = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the current time is {t}")
        
    elif any(w in cmd for w in["date", "tareekh", "aaj kya hai"]):
        d = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {d}")
        
    elif any(w in cmd for w in ["youtube"]):
        speak("Yes sir, opening YouTube.")
        webbrowser.open("https://youtube.com")
        
    elif any(w in cmd for w in ["google"]):
        speak("Accessing Google mainframe.")
        webbrowser.open("https://google.com")
        
    elif any(w in cmd for w in ["search", "dhundo", "batao"]):
        query = cmd.replace("search", "").replace("for", "").replace("karo", "").replace("dhundo", "").replace("jarvis", "").strip()
        if query:
            speak(f"Searching the web for {query}")
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(query)}")
        else:
            speak("Sir, what would you like me to search for?")
            
    elif any(w in cmd for w in ["note", "likho"]):
        speak("Dictation mode activated. Please tell me, what should I save?")
        st.session_state.mode = "dictation"
        
    elif any(w in cmd for w in["sleep", "so jao", "shut down", "stop listening"]):
        speak("Powering down. Goodbye sir.")
        st.session_state.is_awake = False
        return False # This breaks the loop
        
    else:
        speak("I'm sorry sir, I did not catch that.")
        
    return True

# ==========================================
# 5. MAIN EXECUTION LOOP (Controls bottom)
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    if st.button("INITIALIZE SYSTEM"):
        st.session_state.is_awake = True
        status_text.markdown("<h3 style='text-align:center; color:#00f3ff; text-shadow: 0 0 10px #00f3ff;'>ONLINE // LISTENING...</h3>", unsafe_allow_html=True)
        speak("System online. Hello sir, I am listening.")
        
        # Setup Local Speech Recognition
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Real-time continuous loop
            while st.session_state.is_awake:
                update_telemetry() # Keep UI visually active
                
                try:
                    # Listens in 3-second bursts to keep Streamlit UI responsive
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=10)
                    text = recognizer.recognize_google(audio, language='en-IN')
                    
                    # Remove punctuation
                    clean_text = ''.join(char for char in text if char.isalnum() or char.isspace()).strip()
                    update_logs("user", clean_text)
                    
                    # Process it
                    if not process_command(clean_text):
                        break # Exits loop if told to sleep
                        
                except sr.WaitTimeoutError:
                    # Timeout just means nobody spoke. We loop back to update UI.
                    continue
                except sr.UnknownValueError:
                    # Ignored mumbling
                    continue
                except sr.RequestError as e:
                    update_logs("error", "Network API Error. Check Internet connection.")
                    speak("Sir, I cannot connect to the global speech database.")
                    break
                    
        # When loop breaks (Sleep)
        status_text.markdown("<h3 style='text-align:center; color:#ff003c; text-shadow: 0 0 10px #ff003c;'>SYSTEM OFFLINE</h3>", unsafe_allow_html=True)
        st.rerun() # Refresh page to reset state
