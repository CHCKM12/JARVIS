import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. STREAMLIT PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="J.A.R.V.I.S. // MK-IV", layout="wide", page_icon="🤖")

# Hide Streamlit's default menus, headers, and padding to make it a fullscreen app
st.markdown("""
    <style>
        .block-container { padding: 0rem; max-width: 100%; }
        header { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        iframe { border: none; width: 100vw; height: 100vh; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CLOUD-NATIVE HARDWARE ENGINE
# ==========================================
# We embed the UI and Audio engine directly into Streamlit. 
# This forces the Microphone and Speakers to execute on the USER'S browser, 
# completely bypassing the Linux Cloud Server's hardware limitations.

jarvis_cloud_engine = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>J.A.R.V.I.S.</title>
    <style>
        :root { --cyan: #00f3ff; --blue: #0055ff; --red: #ff003c; --bg-dark: #02060a; --glass: rgba(0, 243, 255, 0.05); --scanline: rgba(0, 243, 255, 0.1); }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: var(--bg-dark); color: var(--cyan); font-family: 'Courier New', Courier, monospace; height: 100vh; overflow: hidden; display: flex; justify-content: center; align-items: center; background-image: radial-gradient(circle at center, #051322 0%, #000 100%), linear-gradient(0deg, transparent 24%, var(--scanline) 25%, var(--scanline) 26%, transparent 27%, transparent 74%, var(--scanline) 75%, var(--scanline) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, var(--scanline) 25%, var(--scanline) 26%, transparent 27%, transparent 74%, var(--scanline) 75%, var(--scanline) 76%, transparent 77%, transparent); background-size: 100% 100%, 50px 50px, 50px 50px; }
        #hud-container { width: 95vw; height: 95vh; position: relative; display: grid; grid-template-columns: 250px 1fr 300px; grid-template-rows: 80px 1fr 100px; gap: 20px; border: 1px solid rgba(0, 243, 255, 0.2); padding: 20px; box-shadow: inset 0 0 50px rgba(0, 243, 255, 0.05); }
        #hud-container::before, #hud-container::after { content: ''; position: absolute; width: 40px; height: 40px; border: 3px solid var(--cyan); }
        #hud-container::before { top: -2px; left: -2px; border-right: none; border-bottom: none; }
        #hud-container::after { bottom: -2px; right: -2px; border-left: none; border-top: none; }
        header { grid-column: 1 / 4; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0, 243, 255, 0.3); }
        h1 { font-size: 2rem; letter-spacing: 10px; text-shadow: 0 0 10px var(--cyan); text-transform: uppercase; }
        .status-box { font-size: 1.2rem; color: var(--red); text-shadow: 0 0 10px var(--red); animation: pulse 2s infinite; }
        .telemetry-panel { grid-row: 2 / 3; grid-column: 1 / 2; background: var(--glass); border: 1px solid rgba(0, 243, 255, 0.2); padding: 15px; font-size: 0.8rem; overflow: hidden; display: flex; flex-direction: column; gap: 10px; }
        .telemetry-line { opacity: 0.7; }
        .ai-core-container { grid-row: 2 / 3; grid-column: 2 / 3; display: flex; justify-content: center; align-items: center; position: relative; }
        .reactor { position: relative; width: 300px; height: 300px; display: flex; justify-content: center; align-items: center; }
        .ring { position: absolute; border-radius: 50%; border: 2px solid transparent; }
        .ring-1 { width: 300px; height: 300px; border-top: 3px solid var(--cyan); border-bottom: 3px solid var(--cyan); border-left: 1px dashed var(--cyan); animation: spin 10s linear infinite; }
        .ring-2 { width: 260px; height: 260px; border-right: 4px solid var(--blue); border-left: 4px solid var(--blue); border-bottom: 2px dotted var(--cyan); animation: spin-reverse 6s linear infinite; }
        .ring-3 { width: 220px; height: 220px; border: 1px dashed var(--cyan); animation: spin 4s linear infinite; }
        .core { width: 100px; height: 100px; background: radial-gradient(circle, var(--cyan) 0%, transparent 70%); border-radius: 50%; box-shadow: 0 0 40px var(--cyan), inset 0 0 20px #fff; opacity: 0.2; transition: all 0.3s ease; }
        .listening .core { opacity: 1; animation: core-pulse 1s infinite alternate; }
        .listening .ring-1 { animation: spin 3s linear infinite; box-shadow: 0 0 15px var(--cyan); }
        .listening .ring-2 { animation: spin-reverse 2s linear infinite; }
        .terminal-panel { grid-row: 2 / 3; grid-column: 3 / 4; background: var(--glass); border: 1px solid rgba(0, 243, 255, 0.2); padding: 15px; display: flex; flex-direction: column; overflow-y: auto; backdrop-filter: blur(5px); }
        .log { margin-bottom: 10px; font-size: 0.9rem; line-height: 1.4; word-wrap: break-word;}
        .log-jarvis { color: var(--cyan); } .log-error { color: var(--red); font-weight: bold; } .log-user { color: #fff; text-align: right; font-style: italic; opacity: 0.8; }
        .log-jarvis::before { content: "J.A.R.V.I.S: "; font-weight: bold; } .log-error::before { content: "SYSTEM ERROR: "; font-weight: bold; } .log-user::before { content: "USER: "; font-weight: bold; }
        .control-panel { grid-row: 3 / 4; grid-column: 1 / 4; display: flex; justify-content: center; align-items: center; border-top: 1px solid rgba(0, 243, 255, 0.3); }
        button { background: rgba(0, 243, 255, 0.1); color: var(--cyan); border: 1px solid var(--cyan); padding: 15px 40px; font-size: 1.2rem; text-transform: uppercase; letter-spacing: 3px; cursor: pointer; transition: 0.3s; position: relative; overflow: hidden; }
        button:hover { background: var(--cyan); color: var(--bg-dark); box-shadow: 0 0 20px var(--cyan); }
        @keyframes spin { 100% { transform: rotate(360deg); } } @keyframes spin-reverse { 100% { transform: rotate(-360deg); } } @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } } @keyframes core-pulse { 0% { transform: scale(0.9); box-shadow: 0 0 20px var(--cyan); } 100% { transform: scale(1.1); box-shadow: 0 0 60px var(--cyan), inset 0 0 30px #fff; } }
        .scan-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,243,255,0.1) 50%, rgba(0,243,255,0.1)); background-size: 100% 6px; pointer-events: none; z-index: 100; opacity: 0.4; }
    </style>
</head>
<body>
    <div class="scan-overlay"></div>
    <div id="hud-container">
        <header>
            <h1>J.A.R.V.I.S. // MK-IV</h1>
            <div id="status-text" class="status-box">SYSTEM OFFLINE</div>
        </header>
        <div class="telemetry-panel" id="telemetry">
            <div style="color:#fff; font-weight:bold; margin-bottom:10px;">> SYS.MONITOR</div>
        </div>
        <div class="ai-core-container">
            <div class="reactor" id="reactor">
                <div class="ring ring-1"></div><div class="ring ring-2"></div><div class="ring ring-3"></div><div class="core"></div>
            </div>
        </div>
        <div class="terminal-panel" id="terminal">
            <div class="log log-jarvis">Awaiting system initialization...</div>
        </div>
        <div class="control-panel">
            <button id="power-btn" onclick="toggleSystem()">Initialize System</button>
        </div>
    </div>

<script>
    const terminal = document.getElementById("terminal");
    const reactor = document.getElementById("reactor");
    const statusText = document.getElementById("status-text");
    const powerBtn = document.getElementById("power-btn");
    const telemetry = document.getElementById("telemetry");

    let isAwake = false;
    let currentMode = "standard"; 
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;
    let selectedVoice = null;

    function loadVoices() {
        const voices = window.speechSynthesis.getVoices();
        if(voices.length > 0) {
            selectedVoice = voices.find(v => v.name.includes('Ravi')) || voices.find(v => v.name.includes('Daniel')) || voices.find(v => v.name.toLowerCase().includes('male') && v.lang.includes('en')) || voices[0];
        }
    }
    window.speechSynthesis.onvoiceschanged = loadVoices;
    loadVoices(); 

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-IN'; 

        recognition.onstart = () => {
            reactor.classList.add("listening");
            statusText.innerText = "ONLINE // LISTENING...";
            statusText.style.color = "var(--cyan)";
            powerBtn.innerText = "System Override (Sleep)";
        };

        recognition.onerror = (event) => {
            writeLog("error", "Mic Issue: " + event.error);
        };

        recognition.onend = () => {
            if (isAwake) { setTimeout(() => { try { recognition.start(); } catch(e) {} }, 800); } 
            else { reactor.classList.remove("listening"); statusText.innerText = "SYSTEM OFFLINE"; statusText.style.color = "var(--red)"; powerBtn.innerText = "Initialize System"; }
        };

        recognition.onresult = (event) => {
            let rawTranscript = event.results[event.results.length - 1][0].transcript.toLowerCase();
            writeLog("user", rawTranscript);
            processCommand(rawTranscript.replace(/[.,\\/#!$%\\^&\\*;:{}=\\-_`~()]/g, "").trim());
        };
    } else {
        writeLog("error", "Your browser does not support Speech Recognition. You MUST use Google Chrome.");
    }

    function toggleSystem() {
        if (!SpeechRecognition) { alert("Please use Google Chrome for this to work."); return; }
        if (!isAwake) { isAwake = true; try { recognition.start(); } catch(e) {} startTelemetry(); speak("System online. Hello sir, I am listening."); } 
        else { isAwake = false; recognition.stop(); stopTelemetry(); speak("Powering down. Goodbye sir."); }
    }

    function speak(text) {
        writeLog("jarvis", text);
        const utterance = new SpeechSynthesisUtterance(text);
        if (selectedVoice) utterance.voice = selectedVoice;
        utterance.rate = 1.0; utterance.pitch = 0.8; 
        window.speechSynthesis.speak(utterance);
    }

    function writeLog(sender, text) {
        const div = document.createElement("div");
        div.className = `log log-${sender}`; div.innerText = text;
        terminal.appendChild(div); terminal.scrollTop = terminal.scrollHeight; 
    }

    let telemetryInterval;
    function startTelemetry() {
        telemetryInterval = setInterval(() => {
            if(telemetry.children.length > 15) telemetry.removeChild(telemetry.children[1]); 
            const div = document.createElement("div"); div.className = "telemetry-line";
            div.innerText = `[SEC_${Math.floor(Math.random() * 0xFFFFFF).toString(16).toUpperCase()}] LAT:${(Math.random() * 100).toFixed(4)} // OK`;
            telemetry.appendChild(div);
        }, 800);
    }
    function stopTelemetry() { clearInterval(telemetryInterval); telemetry.innerHTML = '<div style="color:#fff; font-weight:bold; margin-bottom:10px;">> SYS.MONITOR</div><div class="telemetry-line" style="color:var(--red)">OFFLINE</div>'; }

    function processCommand(cmd) {
        if (currentMode === "dictation") {
            if (cmd.includes("cancel") || cmd.includes("stop") || cmd.includes("band karo")) { speak("Note cancelled."); currentMode = "standard"; return; }
            const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([cmd], { type: "text/plain" })); a.download = "Jarvis_Data.txt"; a.click();
            speak("Yes sir, I have saved your note."); currentMode = "standard"; return;
        }
        if (cmd.includes("hello") || cmd.includes("namaste") || cmd.includes("hi")) speak("Hello sir. All systems are running at optimal capacity.");
        else if (cmd.includes("time") || cmd.includes("samay") || cmd.includes("baj rahe")) speak("Sir, the current time is " + new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }));
        else if (cmd.includes("date") || cmd.includes("taarikh") || cmd.includes("aaj kya hai")) speak("Today's date is " + new Date().toLocaleDateString('en-IN'));
        else if (cmd.includes("youtube")) { speak("Yes sir, opening YouTube."); window.open("https://youtube.com", "_blank"); }
        else if (cmd.includes("google")) { speak("Accessing Google mainframe."); window.open("https://google.com", "_blank"); }
        else if (cmd.includes("search") || cmd.includes("dhundo") || cmd.includes("batao")) {
            let query = cmd.replace("search karo", "").replace("search for", "").replace("search", "").replace("dhundo", "").replace("batao", "").replace("jarvis", "").trim();
            if (query) { speak("Searching the web for " + query); window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, "_blank"); } 
            else speak("Sir, what would you like me to search for?");
        }
        else if (cmd.includes("note") || cmd.includes("likho")) { speak("Dictation mode activated. Please tell me, what should I save?"); currentMode = "dictation"; }
        else if (cmd.includes("so jao") || cmd.includes("shut down") || cmd.includes("sleep")) toggleSystem();
        else speak("I did not catch that. Try saying 'Hello', 'What is the time', or 'Open YouTube'.");
    }
</script>
</body>
</html>
"""

# Render the Cloud UI inside Streamlit
components.html(jarvis_cloud_engine, height=1000, scrolling=False)
