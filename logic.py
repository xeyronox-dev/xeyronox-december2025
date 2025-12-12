"""
Gardio Core Logic
Optimized, strictly typed helper functions.
"""
import random
import json
import re
import difflib
import base64
import urllib.parse
from datetime import datetime
from collections import Counter
from typing import Tuple, List, Any

from constants import STOP_WORDS, JOKES, QUOTES, RE_NUMBERS, RE_URLS, VERSION

def validate_text(text: str) -> Tuple[bool, str]:
    """Validate text input. Returns (is_valid, cleaned_text)."""
    if text is None: return False, ""
    cleaned = text.strip()
    return (True, cleaned[:50000]) if cleaned else (False, "")

def html_empty(message: str = "Enter text to begin...") -> str:
    return f'<div class="empty-state">📝 {message}</div>'

def html_error(message: str = "An error occurred") -> str:
    return f'<div class="error-state">⚠️ {message}</div>'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 ANALYTICS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def analyze_text(text: str) -> str:
    """Analyze text and return statistics HTML."""
    is_valid, cleaned = validate_text(text)
    if not is_valid: return html_empty("Enter text to see analytics...")
    
    try:
        words = cleaned.split()
        word_count = len(words)
        chars = len(cleaned)
        lines = len(cleaned.splitlines())
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
    except Exception: return html_error("Analysis failed")

def count_frequency(text: str) -> str:
    """Count word frequency."""
    is_valid, cleaned = validate_text(text)
    if not is_valid: return html_empty()
    
    try:
        # Optimized: Lowercase once, then split. Using standard string translation for speed could be added but regex is fine.
        # Actually, split then filter is efficient.
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
    except Exception: return html_error()
    
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛠️ TOOLS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calculate(a: float, op: str, b: float) -> str:
    try:
        res = 0
        if op == "+": res = a + b
        elif op == "-": res = a - b
        elif op == "×": res = a * b
        elif op == "÷": res = a / b if b != 0 else "Err"
        elif op == "^": res = a ** b
        elif op == "%": res = a % b if b != 0 else "Err"
        
        # Return int if it's a whole number
        return str(int(res)) if isinstance(res, (int, float)) and res == int(res) else f"{res:.4g}"
    except Exception: return "Error"

def extract_numbers(text: str) -> str:
    return ", ".join(RE_NUMBERS.findall(text)) if text else ""

def extract_urls(text: str) -> str:
    return "\n".join(RE_URLS.findall(text)) if text else ""
    
def remove_duplicates(text: str) -> str:
    if not text: return ""
    # Optimized: Set seen tracking in list comp
    seen = set()
    return "\n".join([x for x in text.splitlines() if not (x in seen or seen.add(x))])

def find_replace(text: str, find: str, replace: str) -> str:
    return text.replace(find, replace) if text and find else text

def format_json(text: str) -> str:
    if not text: return ""
    try:
        return json.dumps(json.loads(text), indent=2)
    except Exception as e:
        return f"Invalid JSON: {str(e)}"

def diff_text(text_a: str, text_b: str) -> str:
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
    if not text: return ""
    try:
        if mode == "Base64 Encode": return base64.b64encode(text.encode()).decode()
        elif mode == "Base64 Decode": return base64.b64decode(text).decode()
        elif mode == "URL Encode": return urllib.parse.quote(text)
        elif mode == "URL Decode": return urllib.parse.unquote(text)
    except Exception: return "Error"
    return ""

def text_to_list(text: str) -> str:
    return str([l.strip() for l in text.splitlines() if l.strip()]) if text else "[]"

def text_to_tuple(text: str) -> str:
    return str(tuple(l.strip() for l in text.splitlines() if l.strip())) if text else "()"

def text_to_dict(text: str) -> str:
    if not text: return "{}"
    try:
        return str({k.strip(): v.strip() for line in text.splitlines() for k, v in [line.split(':', 1)] if ':' in line})
    except ValueError: return "Invalid Format"
    
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 💬 CHAT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def chat_respond(message: str, history: List[dict]) -> Tuple[List[dict], str]:
    try:
        is_valid, cleaned = validate_text(message)
        if not is_valid: return history, ""
        msg_lower = cleaned.lower()
        
        resp = "🤔 Try 'help' for commands!"
        
        if any(x in msg_lower for x in ["hello", "hi", "hey"]): resp = "Hello! 👋"
        elif "hola" in msg_lower: resp = "¡Hola! 👋"
        elif "bonjour" in msg_lower: resp = "Bonjour! 👋"
        elif "namaste" in msg_lower: resp = "नमस्ते! 🙏"
        elif "version" in msg_lower:
            resp = f"📦 **Gardio v{VERSION}**\n• Gradio 6.1.0\n• Python 3.10+"
        elif "help" in msg_lower: resp = "**Commands:** hello, version, time, date, joke, quote, tips, bye"
        elif "time" in msg_lower: resp = f"🕐 **{datetime.now().strftime('%H:%M:%S')}**"
        elif "date" in msg_lower: resp = f"📅 **{datetime.now().strftime('%A, %B %d, %Y')}**"
        elif "joke" in msg_lower: resp = random.choice(JOKES)
        elif "quote" in msg_lower: resp = random.choice(QUOTES)
        elif "tips" in msg_lower: resp = "💡 Try the new JSON Formatter and Turbo tools!"
        
        history.append({"role": "user", "content": cleaned})
        history.append({"role": "assistant", "content": resp})
        return history, ""
    except Exception: return history, ""
