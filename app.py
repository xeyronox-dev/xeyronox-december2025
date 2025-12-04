import gradio as gr
import random
import re
from collections import Counter
from datetime import datetime

# ============================================
# UTILITY FUNCTIONS
# ============================================

def welcome(name):
    """Generate personalized welcome message"""
    if not name or name.strip() == "":
        return "👋 Please enter your name to get started!"
    
    greetings = [
        f"Welcome to Gardio, {name}! ⚡",
        f"Hello {name}! Ready to explore? 🚀",
        f"Greetings {name}! Let's build something amazing! 💡",
        f"Hey {name}! Welcome to the December Lab! 🧪"
    ]
    
    message = random.choice(greetings)
    message += f"\n\nThis Space is created by Xeyronox for AI/ML learning, "
    message += f"project testing, and deployment experiments."
    message += f"\n\n🕐 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return message

def calculate(num1, operation, num2):
    """Basic calculator operations"""
    try:
        num1 = float(num1)
        num2 = float(num2)
        
        operations = {
            "➕ Add": lambda a, b: a + b,
            "➖ Subtract": lambda a, b: a - b,
            "✖️ Multiply": lambda a, b: a * b,
            "➗ Divide": lambda a, b: "Cannot divide by zero!" if b == 0 else a / b
        }
        
        result = operations.get(operation, lambda a, b: "Invalid operation")(num1, num2)
        return f"✅ Result: {result}" if isinstance(result, (int, float)) else f"❌ {result}"
    except ValueError:
        return "❌ Please enter valid numbers"

def analyze_text(text):
    """Comprehensive text analysis"""
    if not text or text.strip() == "":
        return "📝 Enter some text to analyze."
    
    words = text.split()
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", ""))
    word_count = len(words)
    sentence_count = max(1, text.count('.') + text.count('!') + text.count('?'))
    
    return f"""📊 **Text Analysis**

| Metric | Value |
|--------|-------|
| Characters | {chars:,} |
| Characters (no spaces) | {chars_no_spaces:,} |
| Words | {word_count:,} |
| Sentences | {sentence_count} |
| Avg word length | {chars_no_spaces / max(1, word_count):.1f} chars |
"""

def word_frequency(text):
    """Analyze word frequency in text"""
    if not text or text.strip() == "":
        return "📝 Enter some text to analyze."
    
    words = re.sub(r'[^\w\s]', ' ', text.lower()).split()
    if not words:
        return "No valid words found."
    
    word_counts = Counter(words)
    total = len(words)
    unique = len(word_counts)
    top_5 = word_counts.most_common(5)
    
    result = f"""📊 **Word Frequency Analysis**

**Stats:**
- Total words: **{total:,}**
- Unique words: **{unique:,}**

**Top 5 Words:**
"""
    for i, (word, count) in enumerate(top_5, 1):
        pct = (count / total) * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        result += f"\n{i}. `{word}` → {count} ({pct:.1f}%) {bar}"
    
    return result

def transform_text(text, mode):
    """Transform text in various ways"""
    if not text:
        return "⚠️ Enter text to transform"
    
    transforms = {
        "🔄 Reverse": text[::-1],
        "🔼 UPPERCASE": text.upper(),
        "🔽 lowercase": text.lower(),
        "📏 No Spaces": text.replace(" ", ""),
        "🎯 Title Case": text.title(),
        "🔀 Shuffle Words": " ".join(random.sample(text.split(), len(text.split()))) if text.split() else text,
    }
    
    return transforms.get(mode, text)

# ============================================
# BUILD THE UI
# ============================================

with gr.Blocks(title="Gardio - December Lab") as demo:
    
    # Inject CSS via HTML
    gr.HTML("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        body, .gradio-container, .main, .contain, .app {
            background: #0a0a0a !important;
            font-family: 'Space Grotesk', -apple-system, sans-serif !important;
        }
        
        .gr-panel, .gr-box, .gr-form, .block {
            background: #141414 !important;
            border: 1px solid #1f1f1f !important;
            border-radius: 14px !important;
        }
        
        .gr-textbox textarea, .gr-textbox input, .gr-number input, input, textarea {
            background: #0f0f0f !important;
            border: 1px solid #1f1f1f !important;
            border-radius: 10px !important;
            color: #e0e0e0 !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        .gr-textbox textarea:focus, input:focus {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.15) !important;
        }
        
        label, .gr-label, span {
            color: #888 !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        .gr-button-primary, button.primary {
            background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
            border: none !important;
            border-radius: 10px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
        }
        
        .gr-button-primary:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3) !important;
        }
        
        .tabs .tab-nav {
            background: #111 !important;
            border-radius: 12px !important;
            padding: 5px !important;
            border: 1px solid #1a1a1a !important;
        }
        
        .tabs .tab-nav button {
            background: transparent !important;
            color: #666 !important;
            border: none !important;
            border-radius: 8px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 500 !important;
        }
        
        .tabs .tab-nav button.selected {
            background: #1a1a1a !important;
            color: #fff !important;
        }
        
        .gr-markdown, .prose, p, h1, h2, h3 {
            color: #e0e0e0 !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }
        
        .gr-markdown code {
            background: #1a1a1a !important;
            color: #a78bfa !important;
            font-family: 'JetBrains Mono', monospace !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
        }
        
        .gr-markdown table { border-collapse: collapse !important; }
        .gr-markdown th, .gr-markdown td {
            border: 1px solid #222 !important;
            padding: 8px 12px !important;
            color: #ccc !important;
        }
        .gr-markdown th { background: #141414 !important; }
        
        @media (max-width: 768px) {
            .gr-row { flex-direction: column !important; }
            .gr-column { width: 100% !important; }
            .tab-nav { flex-wrap: wrap !important; }
            .tab-nav button { padding: 8px 10px !important; font-size: 12px !important; }
        }
    </style>
    """)
    
    # Header
    gr.HTML(
        """
        <div style="text-align: center; padding: 25px 15px; margin-bottom: 15px;">
            <h1 style="
                font-size: clamp(2rem, 5vw, 3rem); 
                margin: 0; 
                background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 50%, #ec4899 100%); 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 700;
            ">⚡ GARDIO</h1>
            <p style="color: #555; font-size: clamp(0.85rem, 2vw, 1rem); margin-top: 10px; font-family: 'Space Grotesk', sans-serif;">
                December 2025 Transformation Lab
            </p>
            <p style="color: #333; font-size: 0.8rem; font-family: 'Space Grotesk', sans-serif;">
                Built by <span style="color: #8b5cf6;">Xeyronox</span>
            </p>
        </div>
        """
    )
    
    with gr.Tabs() as tabs:
        
        # 👋 Welcome Tab
        with gr.Tab("👋 Welcome"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🎯 Get a personalized greeting")
                    name_input = gr.Textbox(label="Your Name", placeholder="Enter your name...", lines=1)
                    welcome_btn = gr.Button("✨ Get Welcome Message", variant="primary")
                with gr.Column(scale=1):
                    welcome_output = gr.Markdown(value="*Your message will appear here...*")
            welcome_btn.click(welcome, name_input, welcome_output)
            gr.Examples([["Xeyronox"], ["Developer"], ["AI Enthusiast"]], name_input)
        
        # 🔢 Calculator Tab
        with gr.Tab("🔢 Calculator"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🧮 Quick Calculator")
                    num1 = gr.Number(label="First Number", value=0)
                    operation = gr.Radio(["➕ Add", "➖ Subtract", "✖️ Multiply", "➗ Divide"], label="Operation", value="➕ Add")
                    num2 = gr.Number(label="Second Number", value=0)
                    calc_btn = gr.Button("🔢 Calculate", variant="primary")
                with gr.Column(scale=1):
                    calc_output = gr.Markdown(value="*Result will appear here...*")
            calc_btn.click(calculate, [num1, operation, num2], calc_output)
        
        # 📝 Text Analyzer Tab
        with gr.Tab("📝 Analyzer"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📊 Text Analysis")
                    text_input = gr.Textbox(label="Input Text", placeholder="Paste your text here...", lines=6)
                    analyze_btn = gr.Button("📊 Analyze", variant="primary")
                with gr.Column(scale=1):
                    analyze_output = gr.Markdown(value="*Analysis will appear here...*")
            analyze_btn.click(analyze_text, text_input, analyze_output)
        
        # 📈 Word Frequency Tab
        with gr.Tab("📈 Frequency"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📈 Word Frequency Counter")
                    freq_input = gr.Textbox(label="Input Text", placeholder="Enter text...", lines=6)
                    freq_btn = gr.Button("📊 Count Words", variant="primary")
                with gr.Column(scale=1):
                    freq_output = gr.Markdown(value="*Frequency will appear here...*")
            freq_btn.click(word_frequency, freq_input, freq_output)
        
        # 🔄 Transform Tab
        with gr.Tab("🔄 Transform"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🔄 Text Transformer")
                    trans_input = gr.Textbox(label="Input Text", placeholder="Enter text...", lines=4)
                    trans_mode = gr.Radio(
                        ["🔄 Reverse", "🔼 UPPERCASE", "🔽 lowercase", "📏 No Spaces", "🎯 Title Case", "🔀 Shuffle Words"],
                        label="Transform Mode", value="🔄 Reverse"
                    )
                    trans_btn = gr.Button("🔄 Transform", variant="primary")
                with gr.Column(scale=1):
                    trans_output = gr.Textbox(label="Transformed Text", lines=4, interactive=False)
            trans_btn.click(transform_text, [trans_input, trans_mode], trans_output)
    
    # Footer
    gr.HTML(
        """
        <div style="text-align: center; padding: 20px; margin-top: 20px; border-top: 1px solid #1a1a1a;">
            <p style="color: #444; font-size: 0.8rem; font-family: 'Space Grotesk', sans-serif; margin: 0;">
                Powered by <span style="color: #6366f1;">Gradio 6.0.2</span> • Built with ❤️ by <span style="color: #8b5cf6;">Xeyronox</span>
            </p>
        </div>
        """
    )

# ============================================
# LAUNCH
# ============================================

if __name__ == "__main__":
    demo.launch()
