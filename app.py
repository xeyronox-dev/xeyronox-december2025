"""
⚡ GARDIO - Text Intelligence Suite
Author: Xeyronox | Version: 2.2.0
Design: Clean, Robust, Mobile-First
"""

import gradio as gr
import random
import re
from collections import Counter
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 CONSTANTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERSION = "2.2.0"
DEBUG = True

STOP_WORDS = {
    "the", "and", "a", "to", "of", "in", "it", "is", "i", "that", 
    "on", "for", "was", "with", "as", "be", "at", "by", "this"
}

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
# 🔧 HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def log_debug(func_name: str, message: str) -> None:
    """Debug logging for HF Spaces logs."""
    if DEBUG:
        print(f"[DEBUG] {func_name}: {message}")

def validate_text(text: str) -> tuple:
    """Validate text input. Returns (is_valid, cleaned_text)."""
    if text is None:
        return False, ""
    cleaned = text.strip()
    if not cleaned:
        return False, ""
    if len(cleaned) > 50000:
        cleaned = cleaned[:50000]
    return True, cleaned

def html_empty(message: str = "Enter text to begin...") -> str:
    """Return styled empty state HTML."""
    return f'<div class="empty-state">📝 {message}</div>'

def html_error(message: str = "An error occurred") -> str:
    """Return styled error state HTML."""
    return f'<div class="error-state">⚠️ {message}</div>'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 CORE LOGIC - TEXT ANALYTICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def analyze_text(text: str) -> str:
    """Analyze text and return statistics HTML."""
    try:
        is_valid, cleaned = validate_text(text)
        if not is_valid:
            return html_empty("Enter text to see analytics...")
        
        log_debug("analyze_text", f"Processing {len(cleaned)} chars")
        
        words = cleaned.split()
        chars = len(cleaned)
        lines = len(cleaned.splitlines())
        word_count = len(words)
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
    except Exception as e:
        log_debug("analyze_text", f"ERROR: {e}")
        return html_error("Analysis failed")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📈 CORE LOGIC - WORD FREQUENCY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def count_frequency(text: str) -> str:
    """Count word frequency with stop word filtering."""
    try:
        is_valid, cleaned = validate_text(text)
        if not is_valid:
            return html_empty("Enter text to analyze frequency...")
        
        clean_text = re.sub(r'[^\w\s]', '', cleaned.lower())
        words = clean_text.split()
        filtered = [w for w in words if w not in STOP_WORDS and len(w) > 1]
        
        if not filtered:
            return html_empty("No significant words found")
        
        counter = Counter(filtered)
        total = len(filtered)
        top_5 = counter.most_common(5)
        
        html = '<div class="freq-panel"><p class="freq-note">Stop words filtered</p>'
        for i, (word, count) in enumerate(top_5, 1):
            pct = (count / total) * 100
            html += f'<div class="freq-row"><span class="rank">#{i}</span><span class="word">{word}</span><span class="count">{count}</span><div class="bar-bg"><div class="bar-fill" style="width:{pct}%"></div></div></div>'
        html += '</div>'
        return html
    except Exception as e:
        log_debug("count_frequency", f"ERROR: {e}")
        return html_error("Frequency analysis failed")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔄 CORE LOGIC - TEXT TRANSFORMER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def transform_text(text: str, mode: str) -> str:
    """Transform text based on selected mode."""
    try:
        is_valid, cleaned = validate_text(text)
        if not is_valid:
            return ""
        
        log_debug("transform_text", f"Mode: {mode}")
        
        ops = {
            "Reverse": lambda t: t[::-1],
            "UPPERCASE": lambda t: t.upper(),
            "lowercase": lambda t: t.lower(),
            "Title Case": lambda t: t.title(),
            "Sentence Case": lambda t: t.capitalize(),
            "No Spaces": lambda t: t.replace(" ", ""),
            "No Punctuation": lambda t: re.sub(r'[^\w\s]', '', t),
            "Shuffle Words": lambda t: " ".join(random.sample(t.split(), len(t.split())) if t.split() else [])
        }
        return ops.get(mode, lambda t: t)(cleaned)
    except Exception as e:
        log_debug("transform_text", f"ERROR: {e}")
        return "Error"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔢 CORE LOGIC - CALCULATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calculate(a: float, op: str, b: float) -> str:
    """Perform basic math operations."""
    try:
        log_debug("calculate", f"{a} {op} {b}")
        if op == "+": result = a + b
        elif op == "-": result = a - b
        elif op == "×": result = a * b
        elif op == "÷": return "Error: Div by 0" if b == 0 else str(a / b)
        elif op == "^": result = a ** b
        elif op == "%": return "Error: Mod by 0" if b == 0 else str(a % b)
        else: return "Error"
        return str(int(result)) if result == int(result) else f"{result:.4g}"
    except Exception as e:
        log_debug("calculate", f"ERROR: {e}")
        return "Error"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📏 CORE LOGIC - QUICK STATS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def quick_stats(text: str) -> tuple:
    """Quick text statistics."""
    try:
        if not text:
            return "", "", "", ""
        chars = str(len(text))
        words = str(len(text.split()))
        lines = str(len(text.splitlines()))
        vowels = str(sum(1 for c in text.lower() if c in 'aeiou'))
        return chars, words, lines, vowels
    except:
        return "Err", "Err", "Err", "Err"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔍 CORE LOGIC - FIND & REPLACE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def find_replace(text: str, find: str, replace: str) -> str:
    """Find and replace text."""
    if not text or not find:
        return text or ""
    return text.replace(find, replace)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧹 CORE LOGIC - REMOVE DUPLICATES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def remove_duplicates(text: str) -> str:
    """Remove duplicate lines from text."""
    if not text:
        return ""
    lines = text.splitlines()
    seen = set()
    unique = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique.append(line)
    return "\n".join(unique)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 CORE LOGIC - WORD COUNTER (NEW)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def word_counter(text: str) -> tuple:
    """Detailed word statistics."""
    try:
        if not text:
            return "", "", "", ""
        words = text.split()
        total = str(len(words))
        unique = str(len(set(words)))
        longest = max(words, key=len) if words else ""
        avg_len = f"{sum(len(w) for w in words) / len(words):.1f}" if words else "0"
        return total, unique, longest, avg_len
    except:
        return "Err", "Err", "Err", "Err"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔢 CORE LOGIC - NUMBER EXTRACTOR (NEW)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def extract_numbers(text: str) -> str:
    """Extract all numbers from text."""
    if not text:
        return ""
    numbers = re.findall(r'-?\d+\.?\d*', text)
    return ", ".join(numbers) if numbers else "No numbers found"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔗 CORE LOGIC - URL EXTRACTOR (NEW)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def extract_urls(text: str) -> str:
    """Extract all URLs from text."""
    if not text:
        return ""
    urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)
    return "\n".join(urls) if urls else "No URLs found"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✂️ CORE LOGIC - TEXT TRIMMER (NEW)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def trim_text(text: str) -> str:
    """Remove extra whitespace and empty lines."""
    if not text:
        return ""
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📋 PYTHON DATA STRUCTURES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def text_to_list(text: str) -> str:
    """Convert text lines to Python list."""
    if not text:
        return "[]"
    items = [line.strip() for line in text.splitlines() if line.strip()]
    return str(items)

def text_to_tuple(text: str) -> str:
    """Convert text lines to Python tuple."""
    if not text:
        return "()"
    items = [line.strip() for line in text.splitlines() if line.strip()]
    return str(tuple(items))

def text_to_dict(text: str) -> str:
    """Convert key:value lines to Python dict."""
    if not text:
        return "{}"
    result = {}
    for line in text.splitlines():
        if ':' in line:
            key, val = line.split(':', 1)
            result[key.strip()] = val.strip()
    return str(result)

def string_ops(text: str, op: str) -> str:
    """String operations."""
    if not text:
        return ""
    ops = {
        "Length": str(len(text)),
        "Split (comma)": str(text.split(',')),
        "Split (space)": str(text.split()),
        "Join (-)": "-".join(text.split()),
        "Strip": text.strip(),
        "Is Alpha": str(text.isalpha()),
        "Is Digit": str(text.isdigit()),
        "Is Alnum": str(text.isalnum())
    }
    return ops.get(op, text)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 💬 CORE LOGIC - CHAT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def chat_respond(message: str, history: list) -> tuple:
    """Enhanced keyword-based chat."""
    try:
        is_valid, cleaned = validate_text(message)
        if not is_valid:
            return history, ""
        
        log_debug("chat_respond", f"Input: {cleaned[:30]}...")
        msg = cleaned.lower()
        response = ""
        
        # Greetings (multi-language)
        if any(x in msg for x in ["hello", "hi", "hey", "good morning", "good evening"]):
            response = random.choice(["Hello! 👋", "Hey there! 🌟", "Hi! Type 'help' for commands!"])
        elif "hola" in msg:
            response = "¡Hola! 👋 Bienvenido a Gardio!"
        elif "bonjour" in msg:
            response = "Bonjour! 👋 Bienvenue à Gardio!"
        elif "namaste" in msg:
            response = "नमस्ते! 🙏 Gardio में स्वागत है!"
        
        # Help
        elif any(x in msg for x in ["help", "commands", "what can you do"]):
            response = """📋 **Commands:**
• `hello/hola/bonjour` - Greetings
• `help` - This menu
• `time/date` - Current time/date
• `joke` - Random joke
• `quote` - Inspirational quote
• `author` - Who made me
• `version` - App info
• `tips` - Usage tips
• `bye` - Goodbye"""
        
        # Time/Date
        elif "time" in msg:
            response = f"🕐 **{datetime.now().strftime('%H:%M:%S')}**"
        elif "date" in msg:
            response = f"📅 **{datetime.now().strftime('%A, %B %d, %Y')}**"
        
        # Info
        elif any(x in msg for x in ["who made", "author", "creator"]):
            response = "🚀 Built by **Xeyronox** in the December Lab!"
        elif "version" in msg:
            response = f"📦 **Gardio v{VERSION}**\n• Gradio 5.9.1\n• Python 3.10+"
        
        # Fun
        elif "joke" in msg:
            response = random.choice(JOKES)
        elif "quote" in msg:
            response = random.choice(QUOTES)
        
        # Tips
        elif "tip" in msg:
            tips = [
                "💡 Use Analytics for detailed text stats!",
                "💡 Frequency filters out common stop words!",
                "💡 Try Remove Duplicates to clean lists!",
                "💡 Number Extractor finds all numbers in text!"
            ]
            response = random.choice(tips)
        
        # Thanks/Bye
        elif any(x in msg for x in ["thank", "thanks"]):
            response = "You're welcome! 😊"
        elif any(x in msg for x in ["bye", "goodbye"]):
            response = "Goodbye! 👋 See you soon!"
        
        # Clear
        elif "clear" in msg:
            return [], ""
        
        # Fallback
        else:
            response = f"🤔 Try 'help' for commands!"
        
        history.append({"role": "user", "content": cleaned})
        history.append({"role": "assistant", "content": response})
        return history, ""
    except Exception as e:
        log_debug("chat_respond", f"ERROR: {e}")
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "⚠️ Error occurred"})
        return history, ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg: #050508;
    --surface: rgba(15, 15, 20, 0.8);
    --glass: rgba(255, 255, 255, 0.03);
    --border: rgba(255, 255, 255, 0.08);
    --accent: #8b5cf6;
    --accent2: #06b6d4;
    --text: #f8fafc;
    --muted: #94a3b8;
    --gradient: linear-gradient(135deg, #8b5cf6, #06b6d4);
}

body, .gradio-container {
    background: var(--bg) !important;
    background-image: radial-gradient(ellipse at 20% 0%, rgba(139,92,246,0.15) 0%, transparent 50%),
                      radial-gradient(ellipse at 80% 100%, rgba(6,182,212,0.1) 0%, transparent 50%) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}

.block, .form {
    background: var(--surface) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
}

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 12px; padding: 12px; }
.stat-card { background: var(--glass); border: 1px solid var(--border); border-radius: 12px; padding: 16px; text-align: center; }
.stat-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.stat-card.highlight { border-color: var(--accent2); }
.stat-card .label { display: block; font-size: 0.65rem; color: var(--muted); text-transform: uppercase; margin-bottom: 6px; }
.stat-card .value { font-size: 1.5rem; font-weight: 700; background: var(--gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.freq-panel { padding: 16px; }
.freq-note { font-size: 0.7rem; color: var(--muted); margin-bottom: 12px; }
.freq-row { display: grid; grid-template-columns: 30px 1fr 40px; gap: 8px; align-items: center; margin-bottom: 10px; padding: 8px; background: var(--glass); border-radius: 8px; }
.rank { color: var(--accent); font-weight: 700; }
.word { color: var(--text); }
.count { color: var(--accent2); text-align: right; }
.bar-bg { grid-column: 1 / -1; height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px; }
.bar-fill { height: 100%; background: var(--gradient); border-radius: 2px; }

.empty-state, .error-state { padding: 32px; text-align: center; color: var(--muted); border: 1px dashed var(--border); border-radius: 12px; }
.error-state { border-color: rgba(239,68,68,0.4); color: #fca5a5; }

textarea, input { background: rgba(0,0,0,0.4) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; color: var(--text) !important; }
textarea:focus, input:focus { border-color: var(--accent) !important; }

button.primary { background: var(--gradient) !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; }
button.primary:hover { transform: translateY(-2px) !important; }

.chatbot { height: 400px !important; }

@media (max-width: 768px) { .stats-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 APP LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with gr.Blocks(title="Gardio - Text Intelligence") as demo:
    gr.HTML(CSS)
    gr.HTML(f'<div style="text-align:center;padding:20px"><h1 style="font-size:2.5rem;margin:0">⚡ GARDIO</h1><p style="color:#94a3b8">Text Intelligence v{VERSION}</p></div>')
    
    with gr.Tabs():
        # 💬 Chat
        with gr.Tab("💬 Chat"):
            chatbot = gr.Chatbot(show_label=False, elem_classes="chatbot")
            with gr.Row():
                msg = gr.Textbox(placeholder="Say hello...", show_label=False, scale=4)
                send_btn = gr.Button("Send", variant="primary", scale=1)
            msg.submit(fn=chat_respond, inputs=[msg, chatbot], outputs=[chatbot, msg])
            send_btn.click(fn=chat_respond, inputs=[msg, chatbot], outputs=[chatbot, msg])
        
        # 📊 Analytics
        with gr.Tab("📊 Analytics"):
            with gr.Row():
                with gr.Column():
                    txt_in = gr.Textbox(label="Input Text", lines=6, placeholder="Paste text...")
                    analyze_btn = gr.Button("Analyze", variant="primary")
                with gr.Column():
                    stats_out = gr.HTML()
            txt_in.change(fn=analyze_text, inputs=[txt_in], outputs=[stats_out])
            analyze_btn.click(fn=analyze_text, inputs=[txt_in], outputs=[stats_out])
        
        # 📈 Frequency
        with gr.Tab("📈 Frequency"):
            with gr.Row():
                with gr.Column():
                    freq_in = gr.Textbox(label="Input Text", lines=5, placeholder="Enter text...")
                    freq_btn = gr.Button("Find Keywords", variant="primary")
                with gr.Column():
                    freq_out = gr.HTML()
            freq_in.change(fn=count_frequency, inputs=[freq_in], outputs=[freq_out])
            freq_btn.click(fn=count_frequency, inputs=[freq_in], outputs=[freq_out])
        
        # 🛠️ Toolbox
        with gr.Tab("🛠️ Toolbox"):
            with gr.Tabs():
                # Transform
                with gr.Tab("🔄 Transform"):
                    t_in = gr.Textbox(label="Input", lines=3, placeholder="Enter text...")
                    t_mode = gr.Radio(["Reverse", "UPPERCASE", "lowercase", "Title Case", "Sentence Case", "No Spaces", "No Punctuation", "Shuffle Words"], value="Reverse", label="Mode")
                    t_out = gr.Textbox(label="Output", lines=3)
                    t_btn = gr.Button("Transform", variant="primary")
                    t_in.change(fn=transform_text, inputs=[t_in, t_mode], outputs=[t_out])
                    t_mode.change(fn=transform_text, inputs=[t_in, t_mode], outputs=[t_out])
                    t_btn.click(fn=transform_text, inputs=[t_in, t_mode], outputs=[t_out])
                
                # Calculator
                with gr.Tab("🔢 Calculator"):
                    with gr.Row():
                        num_a = gr.Number(value=0, label="A")
                        op = gr.Radio(["+", "-", "×", "÷", "^", "%"], value="+", label="Op")
                        num_b = gr.Number(value=0, label="B")
                    calc_out = gr.Textbox(label="Result")
                    calc_btn = gr.Button("Calculate", variant="primary")
                    calc_btn.click(fn=calculate, inputs=[num_a, op, num_b], outputs=[calc_out])
                
                # Word Counter (NEW)
                with gr.Tab("📊 Word Counter"):
                    wc_in = gr.Textbox(label="Input", lines=4, placeholder="Enter text...")
                    with gr.Row():
                        wc_total = gr.Textbox(label="Total Words")
                        wc_unique = gr.Textbox(label="Unique Words")
                        wc_longest = gr.Textbox(label="Longest Word")
                        wc_avg = gr.Textbox(label="Avg Length")
                    wc_btn = gr.Button("Count Words", variant="primary")
                    wc_in.change(fn=word_counter, inputs=[wc_in], outputs=[wc_total, wc_unique, wc_longest, wc_avg])
                    wc_btn.click(fn=word_counter, inputs=[wc_in], outputs=[wc_total, wc_unique, wc_longest, wc_avg])
                
                # Number Extractor (NEW)
                with gr.Tab("🔢 Numbers"):
                    ne_in = gr.Textbox(label="Input", lines=4, placeholder="Text with numbers...")
                    ne_out = gr.Textbox(label="Extracted Numbers", lines=2)
                    ne_btn = gr.Button("Extract Numbers", variant="primary")
                    ne_in.change(fn=extract_numbers, inputs=[ne_in], outputs=[ne_out])
                    ne_btn.click(fn=extract_numbers, inputs=[ne_in], outputs=[ne_out])
                
                # URL Extractor (NEW)
                with gr.Tab("🔗 URLs"):
                    ue_in = gr.Textbox(label="Input", lines=4, placeholder="Text with URLs...")
                    ue_out = gr.Textbox(label="Extracted URLs", lines=3)
                    ue_btn = gr.Button("Extract URLs", variant="primary")
                    ue_in.change(fn=extract_urls, inputs=[ue_in], outputs=[ue_out])
                    ue_btn.click(fn=extract_urls, inputs=[ue_in], outputs=[ue_out])
                
                # Text Trimmer (NEW)
                with gr.Tab("✂️ Trimmer"):
                    tr_in = gr.Textbox(label="Input", lines=4, placeholder="Text with extra spaces...")
                    tr_out = gr.Textbox(label="Trimmed Output", lines=4)
                    tr_btn = gr.Button("Trim Text", variant="primary")
                    tr_in.change(fn=trim_text, inputs=[tr_in], outputs=[tr_out])
                    tr_btn.click(fn=trim_text, inputs=[tr_in], outputs=[tr_out])
                
                # Find & Replace
                with gr.Tab("🔍 Replace"):
                    fr_text = gr.Textbox(label="Text", lines=3, placeholder="Your text...")
                    with gr.Row():
                        fr_find = gr.Textbox(label="Find", placeholder="Search...")
                        fr_replace = gr.Textbox(label="Replace", placeholder="Replace with...")
                    fr_out = gr.Textbox(label="Result", lines=3)
                    fr_btn = gr.Button("Replace All", variant="primary")
                    fr_btn.click(fn=find_replace, inputs=[fr_text, fr_find, fr_replace], outputs=[fr_out])
                
                # Remove Duplicates
                with gr.Tab("🧹 Duplicates"):
                    rd_in = gr.Textbox(label="Input", lines=4, placeholder="Lines with duplicates...")
                    rd_out = gr.Textbox(label="Unique Lines", lines=4)
                    rd_btn = gr.Button("Remove Duplicates", variant="primary")
                    rd_in.change(fn=remove_duplicates, inputs=[rd_in], outputs=[rd_out])
                    rd_btn.click(fn=remove_duplicates, inputs=[rd_in], outputs=[rd_out])
                
                # To List (NEW)
                with gr.Tab("📋 List"):
                    list_in = gr.Textbox(label="Input (one item per line)", lines=4, placeholder="apple\nbanana\ncherry")
                    list_out = gr.Textbox(label="Python List", lines=2)
                    list_btn = gr.Button("Convert to List", variant="primary")
                    list_in.change(fn=text_to_list, inputs=[list_in], outputs=[list_out])
                    list_btn.click(fn=text_to_list, inputs=[list_in], outputs=[list_out])
                
                # To Tuple (NEW)
                with gr.Tab("📦 Tuple"):
                    tuple_in = gr.Textbox(label="Input (one item per line)", lines=4, placeholder="x\ny\nz")
                    tuple_out = gr.Textbox(label="Python Tuple", lines=2)
                    tuple_btn = gr.Button("Convert to Tuple", variant="primary")
                    tuple_in.change(fn=text_to_tuple, inputs=[tuple_in], outputs=[tuple_out])
                    tuple_btn.click(fn=text_to_tuple, inputs=[tuple_in], outputs=[tuple_out])
                
                # To Dict (NEW)
                with gr.Tab("📖 Dict"):
                    dict_in = gr.Textbox(label="Input (key:value per line)", lines=4, placeholder="name: John\nage: 25\ncity: NYC")
                    dict_out = gr.Textbox(label="Python Dict", lines=2)
                    dict_btn = gr.Button("Convert to Dict", variant="primary")
                    dict_in.change(fn=text_to_dict, inputs=[dict_in], outputs=[dict_out])
                    dict_btn.click(fn=text_to_dict, inputs=[dict_in], outputs=[dict_out])
                
                # String Ops (NEW)
                with gr.Tab("🔤 String"):
                    str_in = gr.Textbox(label="Input String", lines=2, placeholder="Hello World")
                    str_op = gr.Radio(["Length", "Split (comma)", "Split (space)", "Join (-)", "Strip", "Is Alpha", "Is Digit", "Is Alnum"], value="Length", label="Operation")
                    str_out = gr.Textbox(label="Result", lines=2)
                    str_btn = gr.Button("Execute", variant="primary")
                    str_in.change(fn=string_ops, inputs=[str_in, str_op], outputs=[str_out])
                    str_op.change(fn=string_ops, inputs=[str_in, str_op], outputs=[str_out])
                    str_btn.click(fn=string_ops, inputs=[str_in, str_op], outputs=[str_out])
    
    gr.HTML('<div style="text-align:center;padding:20px;color:#6b7280;font-size:0.75rem">Built with ❤️ by Xeyronox</div>')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🏃 LAUNCH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    log_debug("main", f"Starting Gardio v{VERSION}")
    demo.launch()
