"""
⚡ GARDIO - December 2025 Lab
Author: Xeyronox | Version: 5.9.1
"""

import gradio as gr
import random
import re
from collections import Counter
from datetime import datetime

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def welcome(name):
    """👋 Personalized greeting"""
    if not name or not name.strip():
        return "👋 Enter your name!"
    greetings = [f"Welcome {name}! ⚡", f"Hello {name}! 🚀", f"Hey {name}! 🧪"]
    return f"{random.choice(greetings)}\n🕐 {datetime.now().strftime('%H:%M:%S')}"


def calculate(a, op, b):
    """🔢 Basic math"""
    try:
        a, b = float(a), float(b)
    except:
        return "❌ Invalid numbers"
    ops = {"➕ Add": a+b, "➖ Sub": a-b, "✖️ Mul": a*b, "➗ Div": a/b if b else "÷0"}
    result = ops.get(op, "?")
    return f"✅ {result}" if isinstance(result, float) else f"❌ {result}"


def analyze(text):
    """📝 Text stats"""
    if not text or not text.strip():
        return "📝 Enter text."
    words = text.split()
    return f"📊 Chars: {len(text):,} | Words: {len(words):,} | Lines: {len(text.splitlines())}"


def frequency(text):
    """📈 Top 5 words"""
    if not text or not text.strip():
        return "📝 Enter text."
    words = re.sub(r'[^\w\s]', '', text.lower()).split()
    if not words:
        return "⚠️ No words."
    top5 = Counter(words).most_common(5)
    lines = [f"📊 Top 5 ({len(words)} words):"]
    for i, (w, c) in enumerate(top5, 1):
        pct = c / len(words) * 100
        bar = "█" * int(pct/5) + "░" * (20-int(pct/5))
        lines.append(f"{i}. `{w}` → {c} ({pct:.0f}%) {bar}")
    return "\n".join(lines)


def transform(text, mode):
    """🔄 Text transform"""
    if not text:
        return "⚠️ Enter text"
    modes = {
        "🔄 Reverse": text[::-1], "🔼 UPPER": text.upper(), "🔽 lower": text.lower(),
        "📏 NoSpace": text.replace(" ", ""), "🎯 Title": text.title(),
        "🔀 Shuffle": " ".join(random.sample(text.split(), len(text.split()))) if text.split() else text
    }
    return modes.get(mode, text)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 STYLES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
body, .gradio-container { background: #080808 !important; font-family: 'Space Grotesk', sans-serif !important; }
.block { background: #111 !important; border: 1px solid #1a1a1a !important; border-radius: 14px !important; }
textarea, input { background: #0a0a0a !important; border: 1px solid #1a1a1a !important; border-radius: 10px !important; color: #ddd !important; }
button.primary { background: linear-gradient(135deg, #8b5cf6, #6366f1) !important; border: none !important; border-radius: 10px !important; }
.tab-nav { background: #0c0c0c !important; border-radius: 12px !important; padding: 5px !important; }
.tab-nav button { background: transparent !important; color: #555 !important; border: none !important; border-radius: 8px !important; }
.tab-nav button.selected { background: #1a1a1a !important; color: #fff !important; }
.gr-markdown, p { color: #e0e0e0 !important; }
@media (max-width: 768px) { .gr-row { flex-direction: column !important; } }
</style>
"""

HEADER = """
<div style="text-align:center; padding:24px 16px;">
<h1 style="font-size:clamp(1.8rem,5vw,2.5rem); margin:0; background:linear-gradient(135deg,#8b5cf6,#6366f1,#ec4899); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:700;">⚡ GARDIO</h1>
<p style="color:#444; margin-top:6px; font-size:0.9rem;">December 2025 Lab • <span style="color:#8b5cf6;">Xeyronox</span></p>
</div>
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🖥️ UI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with gr.Blocks(title="Gardio") as demo:
    gr.HTML(CSS + HEADER)
    
    with gr.Tabs():
        
        # 👋 Welcome
        with gr.Tab("👋 Hi"):
            with gr.Row():
                inp = gr.Textbox(label="Name", scale=2)
                btn = gr.Button("✨", variant="primary", scale=1)
            out = gr.Markdown("*...*")
            btn.click(welcome, inp, out)
        
        # 🔢 Calc
        with gr.Tab("🔢 Calc"):
            with gr.Row():
                n1 = gr.Number(label="A", value=0)
                op = gr.Dropdown(["➕ Add", "➖ Sub", "✖️ Mul", "➗ Div"], label="Op", value="➕ Add")
                n2 = gr.Number(label="B", value=0)
            out = gr.Markdown("*...*")
            gr.Button("🔢 Go", variant="primary").click(calculate, [n1, op, n2], out)
        
        # 📝 Stats
        with gr.Tab("📝 Stats"):
            inp = gr.Textbox(label="Text", lines=3)
            out = gr.Markdown("*...*")
            gr.Button("📊", variant="primary").click(analyze, inp, out)
        
        # 📈 Words
        with gr.Tab("📈 Words"):
            inp = gr.Textbox(label="Text", lines=3)
            out = gr.Markdown("*...*")
            gr.Button("📊", variant="primary").click(frequency, inp, out)
        
        # 🔄 Transform
        with gr.Tab("🔄"):
            inp = gr.Textbox(label="Text", lines=2)
            mode = gr.Radio(["🔄 Reverse", "🔼 UPPER", "🔽 lower", "📏 NoSpace", "🎯 Title", "🔀 Shuffle"], value="🔄 Reverse")
            out = gr.Textbox(label="Result", lines=2, interactive=False)
            gr.Button("🔄 Go", variant="primary").click(transform, [inp, mode], out)
    
    gr.HTML('<p style="text-align:center; color:#333; font-size:0.75rem; margin-top:16px;">Gradio 5.9.1 • Xeyronox</p>')


if __name__ == "__main__":
    demo.launch()
