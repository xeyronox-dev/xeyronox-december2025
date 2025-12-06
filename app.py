"""
⚡ GARDIO - Premium Glass Edition
Author: Xeyronox | Version: 5.9.1
Design: Premium Glassmorphism + Robust Chat + Micro-Polish
"""

import gradio as gr
import random
import re
from collections import Counter
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 CORE LOGIC
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def chat_fn(message, history):
    """
    Robust Chat Function
    - Handles basic conversational intents
    - details: Simple keyword matching for responsiveness
    """
    if not message or not message.strip():
        return history, ""
    
    msg = message.lower().strip()
    
    # Basic Intelligence Layer
    if any(x in msg for x in ["hello", "hi", "hey"]):
        content = "Hello! 👋 I'm Gardio. Ready to analyze your text."
    elif "name" in msg:
        content = "I am Gardio (v5.9.1). I'm a specialized text intelligence interface."
    elif any(x in msg for x in ["work", "job", "can do", "help", "capability"]):
        content = "I can help you with:\n• 📊 Text Analysis\n• 📈 Word Frequency\n• 🔄 Text Transformation\n\nJust use the tabs above!"
    elif any(x in msg for x in ["made", "create", "author", "dev", "who are you"]):
        content = "I was designed and built by Xeyronox in the December Lab! 🧪"
    elif "joke" in msg:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "I told my CSS joke to a backend developer... but they didn't see the style. 🎨",
            "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?' 🧩"
        ]
        content = random.choice(jokes)
    elif "quote" in msg:
        quotes = [
            "“Code is like humor. When you have to explain it, it’s bad.” – Cory House",
            "“First, solve the problem. Then, write the code.” – John Johnson",
            "“Simplicity is the soul of efficiency.” – Austin Freeman"
        ]
        content = f"{random.choice(quotes)} 📜"
    elif "time" in msg:
        content = f"Current system time is {datetime.now().strftime('%H:%M')} 🕐"
    else:
        content = f"Input received: '{message}' 🟢\n(Advanced definition modules are in standby)"

    # Gradio 5.x 'messages' format
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": content})
    
    return history, ""

def analyze_text(text):
    if not text or not text.strip():
        return '<div class="empty-state">📝 Enter text to see analytics...</div>', ""
    
    words = text.split()
    chars = len(text)
    lines = len(text.splitlines())
    avg = sum(len(w) for w in words) / len(words) if words else 0
    read_time = round(len(words) / 200, 1) # Avg 200 wpm
    if read_time < 0.1: read_time = "< 0.1"
    
    html = f"""
    <div class="stats-grid">
        <div class="glass-card stat-card">
            <span class="label">Total Characters</span>
            <span class="value">{chars:,}</span>
        </div>
        <div class="glass-card stat-card">
            <span class="label">Word Count</span>
            <span class="value">{len(words):,}</span>
        </div>
        <div class="glass-card stat-card">
            <span class="label">Line Count</span>
            <span class="value">{lines:,}</span>
        </div>
        <div class="glass-card stat-card">
            <span class="label">Avg Word Len</span>
            <span class="value">{avg:.1f}</span>
        </div>
        <div class="glass-card stat-card" style="border-color: rgba(6,182,212,0.3);">
            <span class="label">Reading Time</span>
            <span class="value">{read_time} m</span>
        </div>
    </div>
    """
    return html

def count_frequency(text):
    if not text or not text.strip():
        return '<div class="empty-state">📊 Enter text to analyze frequency...</div>'
    
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    words = clean_text.split()
    
    # Core Logic Upgrade: Stop Words
    stop_words = {"the", "and", "a", "to", "of", "in", "it", "is", "i", "that", "on", "for"}
    filtered = [w for w in words if w not in stop_words]
    
    if not filtered:
        return '<div class="empty-state">⚠️ No significant words found</div>'
    
    counter = Counter(filtered)
    total = len(filtered)
    top_5 = counter.most_common(5)
    
    html = '<div class="glass-panel freq-panel">'
    html += '<div style="font-size:0.8rem; color:#9ca3af; margin-bottom:12px;">(Common stop words filtered)</div>'
    for i, (word, count) in enumerate(top_5, 1):
        pct = (count / total) * 100
        html += f"""
        <div class="freq-row">
            <div class="freq-info">
                <span class="rank">#{i}</span>
                <span class="word">{word}</span>
                <span class="count">{count}</span>
            </div>
            <div class="progress-bg">
                <div class="progress-fill" style="width: {pct}%"></div>
            </div>
        </div>
        """
    html += '</div>'
    return html

# ... (Transform & Math functions) ...

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 PREMIUM GLASS CSS (POLISHED)
# ...

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def transform_text(text, mode):
    """
    Text Transformation Logic
    - Clean dictionary-based dispatch
    """
    if not text: 
        return ""
    
    # Transformation Operations
    operations = {
        "Reverse 🔄": lambda t: t[::-1],
        "UPPERCASE 🔼": lambda t: t.upper(),
        "lowercase 🔽": lambda t: t.lower(),
        "Title Case 🎯": lambda t: t.title(),
        "Sentence Case 📝": lambda t: t.capitalize(),
        "No Spaces 📏": lambda t: t.replace(" ", ""),
        "No Punctuation 🚫": lambda t: re.sub(r'[^\w\s]', '', t),
        "Shuffle 🔀": lambda t: " ".join(random.sample(t.split(), len(t.split())))
    }
    
    # Execute selected operation
    transformer = operations.get(mode, lambda t: t)
    return transformer(text)

def math_calc(a, op, b):
    try:
        a, b = float(a), float(b)
        res = 0
        if op == "+": res = a + b
        elif op == "-": res = a - b
        elif op == "×": res = a * b
        elif op == "÷": res = "Error" if b == 0 else a / b
        elif op == "^": res = a ** b
        elif op == "%": res = a % b
        
        return str(res) if res == "Error" else f"{res:,.4g}"
    except: return "Invalid Input"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 PREMIUM GLASS CSS (POLISHED)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-color: #050505;
    --glass-bg: rgba(20, 20, 20, 0.7);
    --glass-border: rgba(255, 255, 255, 0.08);
    --accent: #8b5cf6;
    --accent-glow: rgba(139, 92, 246, 0.4);
    --text-primary: #f3f4f6;
    --text-secondary: #9ca3af;
}

body, .gradio-container {
    background-color: var(--bg-color) !important;
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(76, 29, 149, 0.1), transparent 40%), 
        radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.1), transparent 40%) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Glass Panels with improved padding/spacing */
.glass-panel, .glass-card, .block, .gradio-accordion {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    padding: 24px !important; /* A: More breathing room */
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}

.glass-card:hover {
    box-shadow: 0 8px 32px 0 rgba(139, 92, 246, 0.15) !important;
}

/* Typography Polish */
h1, h2, h3, h4, h5, h6 { font-weight: 600 !important; letter-spacing: -0.5px !important; }

/* Inputs - C: Improved Placeholders & Focus */
textarea, input, .gr-input {
    background: rgba(10, 10, 10, 0.6) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
    transition: all 0.25s ease !important;
}

textarea:focus, input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
    transform: translateY(-1px);
}

textarea::placeholder, input::placeholder {
    color: rgba(156, 163, 175, 0.6) !important;
}

/* Buttons - D: Light Animation */
button.primary {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
}

button.primary:hover {
    transform: translateY(-2px) !important;
    filter: brightness(1.1) !important;
    box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.4) !important;
}

/* Stats Grid - A: Spacing */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* Better responsiveness */
    gap: 20px;
    margin-top: 10px;
}

.stat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 24px !important;
}

.stat-card .label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

.stat-card .value {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(to right, #fff, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Frequency Bars */
.freq-panel { padding: 24px !important; }
.freq-row { margin-bottom: 20px; }
.freq-info { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.95rem; }
.rank { color: var(--accent); font-weight: 700; width: 30px; }
.word { color: var(--text-primary); font-weight: 500; }
.count { color: var(--text-secondary); font-variant-numeric: tabular-nums; }
.progress-bg { height: 6px; background: rgba(255, 255, 255, 0.05); border-radius: 10px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--accent), #22d3ee); border-radius: 10px; }

/* Tabs - B: Better Labels Styling */
.tab-nav {
    background: rgba(0,0,0,0.2) !important;
    border-radius: 16px !important;
    padding: 6px !important;
    margin-bottom: 32px !important;
    border: 1px solid rgba(255,255,255,0.03) !important;
    gap: 4px;
}

button.selected {
    background: var(--glass-bg) !important;
    color: #fff !important;
    border: 1px solid var(--accent) !important;
    box-shadow: 0 0 20px var(--accent-glow) !important;
}

/* Chatbot Area */
.chatbot { height: 500px !important; border-radius: 16px !important; overflow: hidden !important; }
.header-row { margin-bottom: 20px !important; }
</style>
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 APP LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with gr.Blocks(title="Gardio Premium") as demo:
    gr.HTML(CSS)
    
    # ⚡ Header
    with gr.Row(elem_classes="header-row"):
        gr.HTML("""
        <div style="text-align: center; padding: 40px 0 30px;">
            <h1 style="font-size: 4rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #a78bfa, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -2px; filter: drop-shadow(0 0 20px rgba(139,92,246,0.2));">
                GARDIO
            </h1>
            <p style="color: #9ca3af; font-size: 1.2rem; margin-top: 12px; font-weight: 300; letter-spacing: 1px;">Premium Text Intelligence Lab</p>
        </div>
        """)

    # 🗂️ Main Tabs - Clean & Consistent
    with gr.Tabs():
        
        # 💬 Chat
        with gr.Tab("💬 Assistant"):
            with gr.Row():
                with gr.Column(scale=1):
                    chatbot = gr.Chatbot(
                        label="System Chat", 
                        show_label=False,
                        avatar_images=(None, "https://www.gradio.app/favicon.ico"),
                        elem_classes="chatbot"
                    )
                    with gr.Row():
                        msg_input = gr.Textbox(
                            placeholder="Type a command or say hello...", 
                            show_label=False, 
                            scale=9, 
                            container=False,
                            autofocus=True
                        )
                        send_btn = gr.Button("➤", variant="primary", scale=1, min_width=80)
            
            msg_input.submit(chat_fn, [msg_input, chatbot], [chatbot, msg_input])
            send_btn.click(chat_fn, [msg_input, chatbot], [chatbot, msg_input])

        # � Stats
        with gr.Tab("📊 Analytics"):
            with gr.Row():
                with gr.Column(scale=1):
                    txt_input = gr.Textbox(
                        label="Input Text", 
                        lines=12, 
                        placeholder="Paste your content here for deep analysis (Articles, Essays, Code)...",
                        show_label=False
                    )
                    analyze_btn = gr.Button("Analyze Content ⚡", variant="primary")
                
                with gr.Column(scale=1):
                    stats_output = gr.HTML(label="Statistics")
            
            analyze_btn.click(analyze_text, inputs=[txt_input], outputs=[stats_output, txt_input])

        # 📈 Frequency
        with gr.Tab("📈 Frequency"):
            with gr.Row():
                with gr.Column(scale=1):
                    freq_input = gr.Textbox(
                        label="Input Text", 
                        lines=10, 
                        placeholder="Enter text to extract top keywords...",
                        show_label=False
                    )
                    freq_btn = gr.Button("Scan Keywords 🔍", variant="primary")
                
                with gr.Column(scale=1):
                    freq_output = gr.HTML(label="Keywords")
            
            freq_btn.click(count_frequency, inputs=[freq_input], outputs=[freq_output])

        # 🛠️ Tools
        with gr.Tab("🛠️ Toolbox"):
            with gr.Row():
                # Transformer
                with gr.Column():
                    gr.Markdown("### 🔄 Text Transformer")
                    t_in = gr.Textbox(label="Original", lines=4, placeholder="Type text to transform...", show_label=False)
                    t_mode = gr.Dropdown([
                        "Reverse 🔄", "UPPERCASE 🔼", "lowercase 🔽", 
                        "Title Case 🎯", "Sentence Case 📝",
                        "No Spaces 📏", "No Punctuation 🚫", "Shuffle 🔀"
                    ], label="Operation", value="Reverse 🔄", show_label=False, container=False, filterable=False)
                    t_out = gr.Textbox(label="Result", lines=4, interactive=False, show_label=False)
                    
                    # Binding changes
                    t_mode.change(transform_text, [t_in, t_mode], t_out)
                    t_in.change(transform_text, [t_in, t_mode], t_out)
                    gr.Button("Apply Transform ✨", variant="primary").click(transform_text, [t_in, t_mode], t_out)
                
                # Calculator
                with gr.Column():
                    gr.Markdown("### 🔢 Quick Math")
                    with gr.Row():
                        num_a = gr.Number(label="A", value=0, show_label=False)
                        op_sel = gr.Dropdown(
                            ["+", "-", "×", "÷", "^ (Power)", "% (Mod)"], 
                            value="+", label="Op", container=False, show_label=False, filterable=False
                        )
                        num_b = gr.Number(label="B", value=0, show_label=False)
                    calc_res = gr.Textbox(label="Result", interactive=False, show_label=False, placeholder="0")
                    gr.Button("Calculate 🧮", variant="primary").click(math_calc, [num_a, op_sel, num_b], calc_res)
    
    # Footer
    gr.HTML("""
    <div style="text-align: center; padding: 40px; color: #4b5563; font-size: 0.8rem; border-top: 1px solid rgba(255,255,255,0.05); margin-top: 60px;">
        <p style="opacity: 0.6;">Gardio v5.9.1 • Micro-Polished • Xeyronox</p>
    </div>
    """)

if __name__ == "__main__":
    demo.launch()
