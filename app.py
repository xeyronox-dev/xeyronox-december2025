"""
⚡ GARDIO - Text Intelligence Suite
Author: Xeyronox | Version: 2.1.0
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

VERSION = "2.1.0"
DEBUG = True

STOP_WORDS = {
    "the", "and", "a", "to", "of", "in", "it", "is", "i", "that", 
    "on", "for", "was", "with", "as", "be", "at", "by", "this"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def log_debug(func_name: str, message: str):
    """Debug logging for HF Spaces logs."""
    if DEBUG:
        print(f"[DEBUG] {func_name}: {message}")

def validate_text(text: str) -> tuple[bool, str]:
    """Validate text input. Returns (is_valid, cleaned_text)."""
    if text is None:
        return False, ""
    cleaned = text.strip()
    if not cleaned:
        return False, ""
    if len(cleaned) > 50000:
        log_debug("validate_text", "Input too long, truncating")
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
        read_time = round(word_count / 200, 1)  # 200 wpm average
        
        return f"""
        <div class="stats-grid">
            <div class="stat-card">
                <span class="label">Characters</span>
                <span class="value">{chars:,}</span>
            </div>
            <div class="stat-card">
                <span class="label">Words</span>
                <span class="value">{word_count:,}</span>
            </div>
            <div class="stat-card">
                <span class="label">Lines</span>
                <span class="value">{lines:,}</span>
            </div>
            <div class="stat-card">
                <span class="label">Avg Length</span>
                <span class="value">{avg_len:.1f}</span>
            </div>
            <div class="stat-card highlight">
                <span class="label">Read Time</span>
                <span class="value">{read_time}m</span>
            </div>
        </div>
        """
    except Exception as e:
        log_debug("analyze_text", f"ERROR: {e}")
        return html_error("Analysis failed. Please try again.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📈 CORE LOGIC - WORD FREQUENCY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def count_frequency(text: str) -> str:
    """Count word frequency with stop word filtering."""
    try:
        is_valid, cleaned = validate_text(text)
        if not is_valid:
            return html_empty("Enter text to analyze frequency...")
        
        log_debug("count_frequency", f"Processing {len(cleaned)} chars")
        
        # Clean and tokenize
        clean_text = re.sub(r'[^\w\s]', '', cleaned.lower())
        words = clean_text.split()
        
        # Filter stop words
        filtered = [w for w in words if w not in STOP_WORDS and len(w) > 1]
        
        if not filtered:
            return html_empty("No significant words found")
        
        counter = Counter(filtered)
        total = len(filtered)
        top_5 = counter.most_common(5)
        
        html = '<div class="freq-panel">'
        html += '<p class="freq-note">Stop words filtered</p>'
        for i, (word, count) in enumerate(top_5, 1):
            pct = (count / total) * 100
            html += f"""
            <div class="freq-row">
                <span class="rank">#{i}</span>
                <span class="word">{word}</span>
                <span class="count">{count}</span>
                <div class="bar-bg"><div class="bar-fill" style="width:{pct}%"></div></div>
            </div>
            """
        html += '</div>'
        return html
        
    except Exception as e:
        log_debug("count_frequency", f"ERROR: {e}")
        return html_error("Frequency analysis failed.")

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
        
        operations = {
            "Reverse": lambda t: t[::-1],
            "UPPERCASE": lambda t: t.upper(),
            "lowercase": lambda t: t.lower(),
            "Title Case": lambda t: t.title(),
            "Sentence Case": lambda t: t.capitalize(),
            "No Spaces": lambda t: t.replace(" ", ""),
            "No Punctuation": lambda t: re.sub(r'[^\w\s]', '', t),
            "Shuffle Words": lambda t: " ".join(random.sample(t.split(), len(t.split())) if t.split() else [])
        }
        
        transformer = operations.get(mode, lambda t: t)
        return transformer(cleaned)
        
    except Exception as e:
        log_debug("transform_text", f"ERROR: {e}")
        return "Error: Transformation failed"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔢 CORE LOGIC - QUICK MATH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calculate(a: float, op: str, b: float) -> str:
    """Perform basic math operations."""
    try:
        log_debug("calculate", f"{a} {op} {b}")
        
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "×":
            result = a * b
        elif op == "÷":
            if b == 0:
                return "Error: Division by zero"
            result = a / b
        elif op == "^":
            result = a ** b
        elif op == "%":
            if b == 0:
                return "Error: Modulo by zero"
            result = a % b
        else:
            return "Error: Unknown operator"
        
        # Format result
        if result == int(result):
            return str(int(result))
        return f"{result:,.4g}"
        
    except Exception as e:
        log_debug("calculate", f"ERROR: {e}")
        return "Error: Calculation failed"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# � CORE LOGIC - QUICK STATS
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
    except Exception as e:
        log_debug("quick_stats", f"ERROR: {e}")
        return "Error", "Error", "Error", "Error"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔍 CORE LOGIC - FIND & REPLACE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def find_replace(text: str, find: str, replace: str) -> str:
    """Find and replace text."""
    try:
        if not text or not find:
            return text or ""
        return text.replace(find, replace)
    except Exception as e:
        log_debug("find_replace", f"ERROR: {e}")
        return text or ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧹 CORE LOGIC - REMOVE DUPLICATES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def remove_duplicates(text: str) -> str:
    """Remove duplicate lines from text."""
    try:
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
    except Exception as e:
        log_debug("remove_duplicates", f"ERROR: {e}")
        return text or ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# �💬 CORE LOGIC - SIMPLE CHAT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def chat_respond(message: str, history: list) -> tuple[list, str]:
    """Enhanced keyword-based chat assistant."""
    try:
        is_valid, cleaned = validate_text(message)
        if not is_valid:
            return history, ""
        
        log_debug("chat_respond", f"Input: {cleaned[:50]}...")
        
        msg = cleaned.lower()
        response = ""
        
        # Greetings
        if any(x in msg for x in ["hello", "hi", "hey", "good morning", "good evening"]):
            greetings = [
                "Hello! 👋 I'm Gardio. Ready to analyze your text!",
                "Hey there! 🌟 What would you like to do today?",
                "Hi! I'm your text assistant. Type 'help' for commands!"
            ]
            response = random.choice(greetings)
        
        # Identity
        elif any(x in msg for x in ["your name", "who are you", "what are you"]):
            response = f"I'm **Gardio v{VERSION}** - a text intelligence assistant built with Gradio! 🤖"
        
        # Help / Commands
        elif any(x in msg for x in ["help", "commands", "what can you do", "features"]):
            response = """📋 **Available Commands:**
• `hello` - Greet me
• `help` - Show this menu
• `time` - Current time
• `date` - Today's date
• `joke` - Random joke
• `quote` - Inspirational quote
• `author` - Who made me
• `version` - App version
• `tips` - Text analysis tips
• `bye` - Say goodbye"""
        
        # Time
        elif "time" in msg:
            response = f"🕐 Current time: **{datetime.now().strftime('%H:%M:%S')}**"
        
        # Date
        elif "date" in msg:
            response = f"� Today is: **{datetime.now().strftime('%A, %B %d, %Y')}**"
        
        # Author / Creator
        elif any(x in msg for x in ["who made", "created", "author", "developer", "built by"]):
            response = "🚀 I was built by **Xeyronox** in the December Lab!"
        
        # Version
        elif "version" in msg:
            response = f"📦 **Gardio v{VERSION}**\n• Framework: Gradio 5.9.1\n• Python 3.10+"
        
        # Jokes
        elif "joke" in msg:
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "There are 10 types of people: those who understand binary and those who don't. 💻",
                "A SQL query walks into a bar and asks two tables: 'Can I join you?' 🍺",
                "Why do Java developers wear glasses? Because they can't C#! 👓",
                "What's a programmer's favorite hangout? Foo Bar! 🍸",
                "How do you comfort a JavaScript bug? You console it! 🖥️"
            ]
            response = random.choice(jokes)
        
        # Quotes
        elif "quote" in msg:
            quotes = [
                "'Code is like humor. When you have to explain it, it's bad.' - Cory House 📝",
                "'First, solve the problem. Then, write the code.' - John Johnson 💡",
                "'Simplicity is the soul of efficiency.' - Austin Freeman ✨",
                "'Programs must be written for people to read.' - Harold Abelson 📖",
                "'Good programmers write code that humans can understand.' - Martin Fowler 🧠"
            ]
            response = random.choice(quotes)
        
        # Tips
        elif "tip" in msg:
            tips = [
                "💡 **Tip:** Use the Analytics tab for detailed text statistics!",
                "💡 **Tip:** The Frequency tab filters out common stop words for better insights!",
                "💡 **Tip:** Try the 'Remove Duplicates' tool for cleaning up lists!",
                "💡 **Tip:** Use 'Find & Replace' for bulk text editing!"
            ]
            response = random.choice(tips)
        
        # Thanks
        elif any(x in msg for x in ["thank", "thanks", "thx"]):
            response = "You're welcome! 😊 Let me know if you need anything else!"
        
        # Goodbye
        elif any(x in msg for x in ["bye", "goodbye", "exit", "quit"]):
            response = "Goodbye! 👋 Come back anytime you need text help!"
        
        # Clear
        elif "clear" in msg:
            history = []
            response = "🧹 Chat cleared! Fresh start!"
            history.append({"role": "assistant", "content": response})
            return history, ""
        
        # Fallback
        else:
            fallbacks = [
                f"I received: '{cleaned[:25]}...'\n💡 Try typing 'help' to see what I can do!",
                f"Hmm, I don't understand '{cleaned[:20]}...'\nType 'commands' for a list of things I can help with!",
                f"🤔 Not sure about that. Type 'help' for available commands!"
            ]
            response = random.choice(fallbacks)
        
        # Append to history (Gradio 5.x format)
        history.append({"role": "user", "content": cleaned})
        history.append({"role": "assistant", "content": response})
        
        return history, ""
        
    except Exception as e:
        log_debug("chat_respond", f"ERROR: {e}")
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "⚠️ Sorry, I encountered an error. Please try again."})
        return history, ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 CSS - PREMIUM GLASS EDITION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --bg: #050508;
    --surface: rgba(15, 15, 20, 0.8);
    --glass: rgba(255, 255, 255, 0.03);
    --border: rgba(255, 255, 255, 0.08);
    --border-glow: rgba(139, 92, 246, 0.3);
    --accent: #8b5cf6;
    --accent-secondary: #06b6d4;
    --text: #f8fafc;
    --muted: #94a3b8;
    --gradient: linear-gradient(135deg, #8b5cf6, #06b6d4);
}

/* Base */
body, .gradio-container {
    background: var(--bg) !important;
    background-image: 
        radial-gradient(ellipse at 20% 0%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, rgba(6, 182, 212, 0.1) 0%, transparent 50%) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: var(--text) !important;
    min-height: 100vh;
}

/* Glass Panels */
.block, .form, .gradio-accordion {
    background: var(--surface) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    box-shadow: 
        0 4px 30px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    transition: all 0.3s ease !important;
}

.block:hover {
    border-color: var(--border-glow) !important;
    box-shadow: 
        0 8px 40px rgba(139, 92, 246, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 16px;
    padding: 12px;
}

.stat-card {
    background: var(--glass) !important;
    backdrop-filter: blur(10px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 12px 40px rgba(139, 92, 246, 0.2);
}

.stat-card.highlight {
    border-color: var(--accent-secondary);
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), transparent) !important;
}

.stat-card .label {
    display: block;
    font-size: 0.65rem;
    font-weight: 500;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.stat-card .value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    background: var(--gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Frequency Bars */
.freq-panel {
    padding: 20px;
    background: var(--glass);
    border-radius: 14px;
}

.freq-note {
    font-size: 0.7rem;
    color: var(--muted);
    margin-bottom: 16px;
    padding: 8px 12px;
    background: rgba(139, 92, 246, 0.1);
    border-radius: 8px;
    display: inline-block;
}

.freq-row {
    display: grid;
    grid-template-columns: 32px 1fr 50px;
    gap: 12px;
    align-items: center;
    margin-bottom: 16px;
    padding: 12px;
    background: var(--glass);
    border-radius: 10px;
    transition: all 0.2s ease;
}

.freq-row:hover {
    background: rgba(139, 92, 246, 0.08);
}

.rank { 
    color: var(--accent); 
    font-weight: 700; 
    font-size: 0.9rem;
}
.word { 
    color: var(--text); 
    font-weight: 500;
}
.count { 
    color: var(--accent-secondary); 
    text-align: right;
    font-weight: 600;
    font-family: 'Space Grotesk', monospace;
}

.bar-bg {
    grid-column: 1 / -1;
    height: 6px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 3px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: var(--gradient);
    border-radius: 3px;
    box-shadow: 0 0 12px rgba(139, 92, 246, 0.4);
    animation: fillBar 0.8s ease-out;
}

@keyframes fillBar {
    from { width: 0 !important; }
}

/* Empty & Error States */
.empty-state, .error-state {
    padding: 48px 24px;
    text-align: center;
    color: var(--muted);
    border: 1px dashed var(--border);
    border-radius: 16px;
    background: var(--glass);
    font-size: 0.95rem;
}

.error-state {
    border-color: rgba(239, 68, 68, 0.4);
    color: #fca5a5;
    background: rgba(239, 68, 68, 0.05);
}

/* Inputs */
textarea, input, select {
    background: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.25s ease !important;
}

textarea:focus, input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
    outline: none !important;
}

textarea::placeholder, input::placeholder {
    color: var(--muted) !important;
    opacity: 0.6 !important;
}

/* Buttons */
button.primary {
    background: var(--gradient) !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
}

button.primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
    filter: brightness(1.1) !important;
}

button.secondary {
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

/* Tabs */
.tab-nav {
    background: rgba(0, 0, 0, 0.3) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    border: 1px solid var(--border) !important;
    margin-bottom: 24px !important;
}

.tab-nav button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

button.selected {
    background: var(--surface) !important;
    border: 1px solid var(--accent) !important;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3) !important;
}

/* Chatbot */
.chatbot {
    height: 450px !important;
    background: transparent !important;
    border-radius: 16px !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--glass);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #a78bfa;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }
    .stat-card {
        padding: 14px 10px;
    }
    .stat-card .value {
        font-size: 1.4rem;
    }
}

/* Dropdown */
.gr-dropdown {
    background: var(--surface) !important;
}
</style>
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 APP LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with gr.Blocks(title="Gardio - Text Intelligence") as demo:
    gr.HTML(CSS)
    
    # Header
    gr.HTML(f"""
    <div style="text-align:center; padding:24px 0;">
        <h1 style="font-size:2.5rem; font-weight:700; margin:0; color:#fff;">
            ⚡ GARDIO
        </h1>
        <p style="color:#9ca3af; margin-top:8px;">Text Intelligence Suite v{VERSION}</p>
    </div>
    """)
    
    with gr.Tabs():
        
        # 💬 Chat Tab
        with gr.Tab("💬 Chat"):
            chatbot = gr.Chatbot(show_label=False, elem_classes="chatbot")
            with gr.Row():
                msg = gr.Textbox(placeholder="Say hello...", show_label=False, scale=4)
                send = gr.Button("Send", variant="primary", scale=1)
            
            msg.submit(chat_respond, [msg, chatbot], [chatbot, msg])
            send.click(chat_respond, [msg, chatbot], [chatbot, msg])
        
        # 📊 Analytics Tab
        with gr.Tab("📊 Analytics"):
            with gr.Row():
                with gr.Column():
                    txt_in = gr.Textbox(
                        label="Input Text", 
                        lines=8, 
                        placeholder="Paste text here..."
                    )
                    analyze_btn = gr.Button("Analyze", variant="primary")
                with gr.Column():
                    stats_out = gr.HTML()
            
            txt_in.change(analyze_text, inputs=[txt_in], outputs=[stats_out])
            analyze_btn.click(analyze_text, inputs=[txt_in], outputs=[stats_out])
        
        # 📈 Frequency Tab
        with gr.Tab("📈 Frequency"):
            with gr.Row():
                with gr.Column():
                    freq_in = gr.Textbox(
                        label="Input Text", 
                        lines=6, 
                        placeholder="Enter text to find keywords..."
                    )
                    freq_btn = gr.Button("Find Keywords", variant="primary")
                with gr.Column():
                    freq_out = gr.HTML()
            
            freq_in.change(count_frequency, inputs=[freq_in], outputs=[freq_out])
            freq_btn.click(count_frequency, inputs=[freq_in], outputs=[freq_out])
        
        # 🛠️ Toolbox Tab - Multiple Sections
        with gr.Tab("🛠️ Toolbox"):
            
            with gr.Tabs():
                
                # 🔄 Transform Sub-Tab
                with gr.Tab("🔄 Transform"):
                    gr.HTML('<p style="color:#94a3b8; margin-bottom:16px;">Transform your text instantly</p>')
                    t_in = gr.Textbox(
                        label="Input Text", 
                        lines=4, 
                        placeholder="Enter text to transform..."
                    )
                    t_mode = gr.Radio(
                        choices=[
                            "Reverse", "UPPERCASE", "lowercase", 
                            "Title Case", "Sentence Case", 
                            "No Spaces", "No Punctuation", "Shuffle Words"
                        ],
                        value="Reverse",
                        label="Transformation"
                    )
                    t_out = gr.Textbox(label="Result", lines=4, interactive=True)
                    gr.Button("Transform ✨", variant="primary").click(
                        transform_text, [t_in, t_mode], t_out
                    )
                    t_in.change(transform_text, [t_in, t_mode], t_out)
                    t_mode.change(transform_text, [t_in, t_mode], t_out)
                
                # 🔢 Calculator Sub-Tab
                with gr.Tab("🔢 Calculator"):
                    gr.HTML('<p style="color:#94a3b8; margin-bottom:16px;">Quick math operations</p>')
                    with gr.Row():
                        num_a = gr.Number(value=0, label="Number A")
                        op = gr.Radio(
                            choices=["+", "-", "×", "÷", "^", "%"], 
                            value="+", 
                            label="Operator"
                        )
                        num_b = gr.Number(value=0, label="Number B")
                    calc_out = gr.Textbox(label="Result", interactive=True, placeholder="0")
                    gr.Button("Calculate 🧮", variant="primary").click(
                        calculate, [num_a, op, num_b], calc_out
                    )
                
                # 📏 Quick Stats Sub-Tab
                with gr.Tab("📏 Quick Stats"):
                    gr.HTML('<p style="color:#94a3b8; margin-bottom:16px;">Instant text measurements</p>')
                    qs_in = gr.Textbox(
                        label="Input Text", 
                        lines=4, 
                        placeholder="Paste text here..."
                    )
                    with gr.Row():
                        qs_chars = gr.Textbox(label="Characters", interactive=True)
                        qs_words = gr.Textbox(label="Words", interactive=True)
                        qs_lines = gr.Textbox(label="Lines", interactive=True)
                        qs_vowels = gr.Textbox(label="Vowels", interactive=True)
                    
                    qs_in.change(quick_stats, [qs_in], [qs_chars, qs_words, qs_lines, qs_vowels])
                    qs_btn = gr.Button("Count 📊", variant="primary")
                    qs_btn.click(quick_stats, [qs_in], [qs_chars, qs_words, qs_lines, qs_vowels])
                
                # 🔍 Find & Replace Sub-Tab
                with gr.Tab("🔍 Find & Replace"):
                    gr.HTML('<p style="color:#94a3b8; margin-bottom:16px;">Search and replace text</p>')
                    fr_text = gr.Textbox(label="Text", lines=4, placeholder="Your text here...")
                    with gr.Row():
                        fr_find = gr.Textbox(label="Find", placeholder="Search for...", interactive=True)
                        fr_replace = gr.Textbox(label="Replace with", placeholder="Replace with...", interactive=True)
                    fr_out = gr.Textbox(label="Result", lines=4, interactive=True)
                    
                    fr_btn = gr.Button("Replace All 🔄", variant="primary")
                    fr_btn.click(find_replace, [fr_text, fr_find, fr_replace], fr_out)
                
                # 🧹 Remove Duplicates Sub-Tab
                with gr.Tab("🧹 Remove Duplicates"):
                    gr.HTML('<p style="color:#94a3b8; margin-bottom:16px;">Remove duplicate lines from text</p>')
                    rd_in = gr.Textbox(label="Input Text", lines=6, placeholder="Paste text with duplicate lines...")
                    rd_out = gr.Textbox(label="Result (Unique Lines)", lines=6, interactive=True)
                    
                    rd_btn = gr.Button("Remove Duplicates 🧹", variant="primary")
                    rd_btn.click(remove_duplicates, [rd_in], rd_out)
                    rd_in.change(remove_duplicates, [rd_in], rd_out)
    
    # Footer
    gr.HTML("""
    <div style="text-align:center; padding:24px; color:#6b7280; font-size:0.75rem;">
        Built with ❤️ by Xeyronox
    </div>
    """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🏃 LAUNCH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    log_debug("main", f"Starting Gardio v{VERSION}")
    demo.launch()
