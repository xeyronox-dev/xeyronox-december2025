"""
⚡ GARDIO - Text Intelligence Suite
Author: Xeyronox | Version: 2.3.0
Design: Clean, Robust, Mobile-First
"""

import gradio as gr
import random
import re
import json
import difflib
import base64
import urllib.parse
from collections import Counter
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 CONSTANTS & CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERSION = "2.3.0"
DEBUG = False  # 🚀 TURBO MODE: Logging disabled

STOP_WORDS = {
    "the", "and", "a", "to", "of", "in", "it", "is", "i", "that", 
    "on", "for", "was", "with", "as", "be", "at", "by", "this"
}

# Pre-compiled Regex 🚀
RE_NUMBERS = re.compile(r'-?\d+\.?\d*')
RE_URLS = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
    "There are 10 types of people: those who understand binary and those who don't. 💻",
    "A SQL query walks into a bar and asks two tables: 'Can I join you?' 🍺",
    "Why do Java developers wear glasses? Because they can't C#! 👓",
    "What's a programmer's favorite hangout? Foo Bar! 🍸",
    "How do you comfort a JavaScript bug? You console it! 🖥️",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself! 😢",
    "What's a programmer's favorite snack? Chips and dip... into the codebase! 🍟",
    "Why did the programmer quit? Because he didn't get arrays (a raise)! 💰",
    "What do you call 8 hobbits? A hobbyte! 🧙"
]

QUOTES = [
    "'Code is like humor. When you have to explain it, it's bad.' - Cory House 📝",
    "'First, solve the problem. Then, write the code.' - John Johnson 💡",
    "'Simplicity is the soul of efficiency.' - Austin Freeman ✨",
    "'Programs must be written for people to read.' - Harold Abelson 📖",
    "'Good programmers write code that humans can understand.' - Martin Fowler 🧠",
    "'The best code is no code at all.' - Jeff Atwood 🎯",
    "'It works on my machine.' - Every Developer 😅",
    "'Talk is cheap. Show me the code.' - Linus Torvalds 💬",
    "'Any fool can write code that a computer can understand.' - Martin Fowler 🤖",
    "'Measuring progress by lines of code is like measuring aircraft by weight.' - Bill Gates ✈️"
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚡ CLIENT-SIDE JAVASCRIPT (TURBO MODE)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JS_LOGIC = """
window.js_logic = {
    transform: (text, mode) => {
        if (!text) return "";
        switch(mode) {
            case "Reverse": return text.split("").reverse().join("");
            case "UPPERCASE": return text.toUpperCase();
            case "lowercase": return text.toLowerCase();
            case "Title Case": return text.toLowerCase().split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            case "Sentence Case": return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
            case "No Spaces": return text.replace(/\\s+/g, '');
            case "No Punctuation": return text.replace(/[^\\w\\s]|_/g, "");
            case "Shuffle Words": return text.split(' ').sort(() => Math.random() - 0.5).join(' ');
            default: return text;
        }
    },
    
    wordCount: (text) => {
        if (!text) return ["0", "0", "", "0"];
        const words = text.trim().split(/\\s+/);
        const total = words.length;
        const unique = new Set(words).size;
        const longest = words.reduce((a, b) => a.length > b.length ? a : b, "");
        const avg = total ? (words.join("").length / total).toFixed(1) : "0";
        return [String(total), String(unique), longest, String(avg)];
    },
    
    trim: (text) => {
        if (!text) return "";
        return text.split("\\n").map(l => l.trim()).filter(l => l).join("\\n");
    },
    
    stringOps: (text, op) => {
        if (!text) return "";
        switch(op) {
            case "Length": return String(text.length);
            case "Split (comma)": return JSON.stringify(text.split(","));
            case "Split (space)": return JSON.stringify(text.split(" "));
            case "Join (-)": return text.split(" ").join("-");
            case "Strip": return text.trim();
            case "Is Alpha": return String(/^[a-zA-Z]+$/.test(text));
            case "Is Digit": return String(/^\\d+$/.test(text));
            case "Is Alnum": return String(/^[a-zA-Z0-9]+$/.test(text));
            default: return text;
        }
    }
}
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 PYTHON HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_text(text: str) -> tuple:
    """Validate text input. Returns (is_valid, cleaned_text)."""
    if text is None: return False, ""
    cleaned = text.strip()
    return (True, cleaned[:50000]) if cleaned else (False, "")

def html_empty(message: str = "Enter text to begin...") -> str:
    return f'<div class="empty-state">📝 {message}</div>'

def html_error(message: str = "An error occurred") -> str:
    return f'<div class="error-state">⚠️ {message}</div>'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 ANALYTICS & FREQUENCY (Server-Side)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def analyze_text(text: str) -> str:
    """Analyze text and return statistics HTML."""
    try:
        is_valid, cleaned = validate_text(text)
        if not is_valid: return html_empty("Enter text to see analytics...")
        
        words = cleaned.split()
        chars, lines, word_count = len(cleaned), len(cleaned.splitlines()), len(words)
        avg_len = sum(len(w) for w in words) / word_count if word_count else 0
        read_time = round(word_count / 200, 1)
        
        return f"""
        <div class="stats-grid">
            <div class="stat-card"><span class="label">Characters</span><span class="value">{chars:,}</span></div>
            <div class="stat-card"><span class="label">Words</span><span class="value">{word_count:,}</span></div>
            <div class="stat-card"><span class="label">Lines</span><span class="value">{lines:,}</span></div>
            <div class="stat-card"><span class="label">Avg Length</span><span class="value">{avg_len:.1f}</span></div>
            <div class="stat-card highlight"><span class="label">Read Time</span><span class="value">{read_time}m</span></div>
        </div>
        """
    except: return html_error("Analysis failed")

def count_frequency(text: str) -> str:
    """Count word frequency."""
    try:
        is_valid, cleaned = validate_text(text)
        if not is_valid: return html_empty()
        
        words = re.sub(r'[^\w\s]', '', cleaned.lower()).split()
        filtered = [w for w in words if w not in STOP_WORDS and len(w) > 1]
        
        if not filtered: return html_empty("No significant words found")
        
        top_5 = Counter(filtered).most_common(5)
        total = len(filtered)
        
        html = '<div class="freq-panel"><p class="freq-note">Stop words filtered</p>'
        for i, (word, count) in enumerate(top_5, 1):
            pct = (count / total) * 100
            html += f'<div class="freq-row"><span class="rank">#{i}</span><span class="word">{word}</span><span class="count">{count}</span><div class="bar-bg"><div class="bar-fill" style="width:{pct}%"></div></div></div>'
        html += '</div>'
        return html
    except: return html_error()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛠️ SERVER-SIDE TOOLS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calculate(a: float, op: str, b: float) -> str:
    try:
        if op == "+": res = a + b
        elif op == "-": res = a - b
        elif op == "×": res = a * b
        elif op == "÷": res = a / b if b != 0 else "Err"
        elif op == "^": res = a ** b
        elif op == "%": res = a % b if b != 0 else "Err"
        return str(int(res)) if isinstance(res, (int, float)) and res == int(res) else f"{res:.4g}"
    except: return "Error"

def extract_numbers(text: str) -> str:
    return ", ".join(RE_NUMBERS.findall(text)) if text else ""

def extract_urls(text: str) -> str:
    return "\n".join(RE_URLS.findall(text)) if text else ""

def remove_duplicates(text: str) -> str:
    if not text: return ""
    seen = set()
    return "\n".join([x for x in text.splitlines() if not (x in seen or seen.add(x))])

def find_replace(text: str, find: str, replace: str) -> str:
    return text.replace(find, replace) if text and find else text

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🆕 NEW TOOLS (BATCH 2)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def format_json(text: str) -> str:
    """Pretty print and validate JSON."""
    if not text: return ""
    try:
        parsed = json.loads(text)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"

def diff_text(text_a: str, text_b: str) -> str:
    """Compare two texts."""
    if not text_a or not text_b: return ""
    diff = difflib.unified_diff(
        text_a.splitlines(), 
        text_b.splitlines(), 
        lineterm="", 
        fromfile="Text A", 
        tofile="Text B"
    )
    return "\n".join(diff)

def encode_decode(text: str, mode: str) -> str:
    """Base64 and URL encoding/decoding."""
    if not text: return ""
    try:
        if mode == "Base64 Encode": return base64.b64encode(text.encode()).decode()
        elif mode == "Base64 Decode": return base64.b64decode(text).decode()
        elif mode == "URL Encode": return urllib.parse.quote(text)
        elif mode == "URL Decode": return urllib.parse.unquote(text)
    except: return "Error"
    return ""

def text_to_list(text: str) -> str:
    return str([l.strip() for l in text.splitlines() if l.strip()]) if text else "[]"

def text_to_tuple(text: str) -> str:
    return str(tuple(l.strip() for l in text.splitlines() if l.strip())) if text else "()"

def text_to_dict(text: str) -> str:
    if not text: return "{}"
    return str({k.strip(): v.strip() for line in text.splitlines() for k, v in [line.split(':', 1)] if ':' in line})

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 💬 CHAT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def chat_respond(message: str, history: list) -> tuple:
    try:
        is_valid, cleaned = validate_text(message)
        if not is_valid: return history, ""
        msg = cleaned.lower()
        
        if any(x in msg for x in ["hello", "hi", "hey"]): resp = "Hello! 👋"
        elif "hola" in msg: resp = "¡Hola! 👋"
        elif "bonjour" in msg: resp = "Bonjour! 👋"
        elif "namaste" in msg: resp = "नमस्ते! 🙏"
        elif "version" in msg:
            resp = f"📦 **Gardio v{VERSION}**\n• Gradio 6.1.0\n• Python 3.10+"
        elif "help" in msg: resp = "**Commands:** hello, version, time, date, joke, quote, tips, bye"
        elif "time" in msg: resp = f"🕐 **{datetime.now().strftime('%H:%M:%S')}**"
        elif "date" in msg: resp = f"📅 **{datetime.now().strftime('%A, %B %d, %Y')}**"
        elif "joke" in msg: resp = random.choice(JOKES)
        elif "quote" in msg: resp = random.choice(QUOTES)
        elif "tips" in msg: resp = "💡 Try the new JSON Formatter and Turbo tools!"
        else: resp = "🤔 Try 'help' for commands!"
        
        history.append({"role": "user", "content": cleaned})
        history.append({"role": "assistant", "content": resp})
        return history, ""
    except: return history, ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
:root { --bg:#050508; --surface:rgba(15,15,20,0.8); --glass:rgba(255,255,255,0.03); --border:rgba(255,255,255,0.08); --accent:#8b5cf6; --accent2:#06b6d4; --text:#f8fafc; --gradient:linear-gradient(135deg,#8b5cf6,#06b6d4); }
body,.gradio-container{background:var(--bg)!important;font-family:'Inter',sans-serif!important;color:var(--text)!important}
.block,.form{background:var(--surface)!important;backdrop-filter:blur(20px)!important;border:1px solid var(--border)!important;border-radius:16px!important}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:12px;padding:12px}
.stat-card{background:var(--glass);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center}
.stat-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.stat-card .value{font-size:1.5rem;font-weight:700;background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.freq-row{display:grid;grid-template-columns:30px 1fr 40px;gap:8px;align-items:center;margin-bottom:10px;padding:8px;background:var(--glass);border-radius:8px}
.bar-fill{height:100%;background:var(--gradient);border-radius:2px}
textarea,input{background:rgba(0,0,0,0.4)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--text)!important}
textarea:focus,input:focus{border-color:var(--accent)!important}
button.primary{background:var(--gradient)!important;border:none!important;border-radius:10px!important;font-weight:600!important}
.chatbot{height:400px!important}
.empty-state,.error-state{padding:20px;text-align:center;border-radius:10px;background:var(--glass);border:1px solid var(--border);color:var(--text);font-weight:600}
.error-state{border-color:#ef4444;color:#ef4444}
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 APP LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with gr.Blocks(title="Gardio Turbo", js=JS_LOGIC, css=CSS) as demo:
    gr.HTML(f'<div style="text-align:center;padding:20px"><h1 style="font-size:2.5rem;margin:0">⚡ GARDIO <span style="font-size:1rem;background:#8b5cf6;padding:2px 8px;border-radius:4px;vertical-align:middle">TURBO</span></h1><p style="color:#94a3b8">v{VERSION} | Latency &lt; 0.10s</p></div>')
    
    with gr.Tabs():
        with gr.Tab("💬 Chat"):
            chatbot = gr.Chatbot(show_label=False, elem_classes="chatbot")
            with gr.Row():
                msg = gr.Textbox(placeholder="Say hello...", show_label=False, scale=4)
                send_btn = gr.Button("Send", variant="primary", scale=1)
            msg.submit(fn=chat_respond, inputs=[msg, chatbot], outputs=[chatbot, msg])
            send_btn.click(fn=chat_respond, inputs=[msg, chatbot], outputs=[chatbot, msg])
        
        with gr.Tab("📊 Analytics"):
            with gr.Row():
                with gr.Column():
                    txt_in = gr.Textbox(lines=6, placeholder="Paste text...")
                    analyze_btn = gr.Button("Analyze", variant="primary")
                stats_out = gr.HTML()
            txt_in.change(fn=analyze_text, inputs=[txt_in], outputs=[stats_out])
            analyze_btn.click(fn=analyze_text, inputs=[txt_in], outputs=[stats_out])
        
        with gr.Tab("📈 Frequency"):
            with gr.Row():
                freq_in = gr.Textbox(lines=5, placeholder="Enter text...")
                freq_out = gr.HTML()
            gr.Button("Find Keywords", variant="primary").click(fn=count_frequency, inputs=[freq_in], outputs=[freq_out])
            freq_in.change(fn=count_frequency, inputs=[freq_in], outputs=[freq_out])
        
        with gr.Tab("🛠️ Toolbox"):
            with gr.Tabs():
                # Client-Side Tools (Turbo) ⚡
                with gr.Tab("⚡ Transform"):
                    t_in = gr.Textbox(label="Input", lines=3)
                    t_mode = gr.Radio(["Reverse", "UPPERCASE", "lowercase", "Title Case", "Sentence Case", "No Spaces", "No Punctuation", "Shuffle Words"], value="Reverse")
                    t_out = gr.Textbox(label="Output (Instant)", lines=3)
                    # JS Injection 🚀
                    t_trigger = gr.Button("Transform", variant="primary")
                    t_in.change(None, [t_in, t_mode], t_out, js="(t, m) => js_logic.transform(t, m)")
                    t_mode.change(None, [t_in, t_mode], t_out, js="(t, m) => js_logic.transform(t, m)")
                    t_trigger.click(None, [t_in, t_mode], t_out, js="(t, m) => js_logic.transform(t, m)")

                with gr.Tab("⚡ Word Counter"):
                    wc_in = gr.Textbox(label="Typing...", lines=4)
                    with gr.Row():
                        wc_total = gr.Textbox(label="Total")
                        wc_unique = gr.Textbox(label="Unique")
                        wc_longest = gr.Textbox(label="Longest")
                        wc_avg = gr.Textbox(label="Avg Len")
                    # JS Injection 🚀
                    wc_in.input(None, wc_in, [wc_total, wc_unique, wc_longest, wc_avg], js="(t) => js_logic.wordCount(t)")

                with gr.Tab("⚡ Trimmer"):
                    tr_in = gr.Textbox(label="Input", lines=4)
                    tr_out = gr.Textbox(label="Output", lines=4)
                    tr_in.input(None, tr_in, tr_out, js="(t) => js_logic.trim(t)")
                    
                with gr.Tab("⚡ String"):
                    str_in = gr.Textbox(label="Input")
                    str_op = gr.Radio(["Length", "Split (comma)", "Split (space)", "Join (-)", "Strip", "Is Alpha", "Is Digit", "Is Alnum"], value="Length")
                    str_out = gr.Textbox(label="Result")
                    str_in.change(None, [str_in, str_op], str_out, js="(t, o) => js_logic.stringOps(t, o)")
                    str_op.change(None, [str_in, str_op], str_out, js="(t, o) => js_logic.stringOps(t, o)")

                # Server-Side Tools
                with gr.Tab("🔢 Calculator"):
                    num_a = gr.Number(value=0, label="A")
                    op = gr.Radio(["+", "-", "×", "÷", "^", "%"], value="+")
                    num_b = gr.Number(value=0, label="B")
                    calc_out = gr.Textbox(label="Result")
                    gr.Button("Calculate", variant="primary").click(fn=calculate, inputs=[num_a, op, num_b], outputs=[calc_out])

                # New Tools (Batch 2)
                with gr.Tab("📝 JSON"):
                    json_in = gr.Textbox(lines=6, placeholder='{"key": "value"}')
                    json_out = gr.Textbox(lines=6, label="Pretty JSON")
                    gr.Button("Format", variant="primary").click(fn=format_json, inputs=[json_in], outputs=[json_out])
                
                with gr.Tab("⚖️ Diff"):
                    d_a = gr.Textbox(lines=3, label="Text A")
                    d_b = gr.Textbox(lines=3, label="Text B")
                    d_out = gr.Textbox(lines=6, label="Differences")
                    gr.Button("Compare", variant="primary").click(fn=diff_text, inputs=[d_a, d_b], outputs=[d_out])
                
                with gr.Tab("🔐 Encoder"):
                    enc_in = gr.Textbox(lines=3, placeholder="Text...", label="Input")
                    enc_mode = gr.Radio(["Base64 Encode", "Base64 Decode", "URL Encode", "URL Decode"], value="Base64 Encode", label="Mode")
                    enc_out = gr.Textbox(lines=3, label="Output")
                    gr.Button("Convert", variant="primary").click(fn=encode_decode, inputs=[enc_in, enc_mode], outputs=[enc_out])

                # Standard Tools
                with gr.Tab("🧹 Duplicates"):
                    rd_in = gr.Textbox(lines=4, label="Paste Text")
                    rd_out = gr.Textbox(lines=4, label="Unique Lines")
                    rd_in.change(fn=remove_duplicates, inputs=[rd_in], outputs=[rd_out])

                with gr.Tab("🔢 Numbers"):
                    ne_in = gr.Textbox(lines=4, label="Paste Text")
                    ne_out = gr.Textbox(lines=2, label="Extracted Numbers")
                    ne_in.change(fn=extract_numbers, inputs=[ne_in], outputs=[ne_out])

                with gr.Tab("🔗 URLs"):
                    ue_in = gr.Textbox(lines=4, label="Paste Text")
                    ue_out = gr.Textbox(lines=3, label="Extracted URLs")
                    ue_in.change(fn=extract_urls, inputs=[ue_in], outputs=[ue_out])
                
                with gr.Tab("🔍 Replace"):
                    fr_text = gr.Textbox(lines=3, label="Input Text")
                    with gr.Row():
                        fr_find = gr.Textbox(label="Find")
                        fr_replace = gr.Textbox(label="Replace")
                    fr_out = gr.Textbox(lines=3, label="Result")
                    gr.Button("Replace All", variant="primary").click(fn=find_replace, inputs=[fr_text, fr_find, fr_replace], outputs=[fr_out])

                # Python Data Tools (Simple)
                with gr.Tab("📋 List"):
                    l_in = gr.Textbox(lines=4, label="Items (One per line)")
                    l_out = gr.Textbox(lines=2, label="Python List")
                    gr.Button("Convert").click(fn=text_to_list, inputs=[l_in], outputs=[l_out])
                
                with gr.Tab("📦 Tuple"):
                    tup_in = gr.Textbox(lines=4, label="Items (One per line)")
                    tup_out = gr.Textbox(lines=2, label="Python Tuple")
                    gr.Button("Convert").click(fn=text_to_tuple, inputs=[tup_in], outputs=[tup_out])
                
                with gr.Tab("📖 Dict"):
                    dict_in = gr.Textbox(lines=4, label="Key:Value (One per line)")
                    dict_out = gr.Textbox(lines=2, label="Python Dict")
                    gr.Button("Convert").click(fn=text_to_dict, inputs=[dict_in], outputs=[dict_out])

    gr.HTML('<div style="text-align:center;padding:20px;color:#6b7280;font-size:0.75rem">Built with ❤️ by Xeyronox</div>')

if __name__ == "__main__":
    demo.launch()
