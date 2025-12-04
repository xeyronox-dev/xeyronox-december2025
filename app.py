import gradio as gr
import random
import re
from collections import Counter
from datetime import datetime

# Welcome message function
def welcome(name):
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

# Calculator function
def calculate(num1, operation, num2):
    try:
        num1 = float(num1)
        num2 = float(num2)
        
        if operation == "Add ➕":
            result = num1 + num2
        elif operation == "Subtract ➖":
            result = num1 - num2
        elif operation == "Multiply ✖️":
            result = num1 * num2
        elif operation == "Divide ➗":
            if num2 == 0:
                return "❌ Error: Cannot divide by zero!"
            result = num1 / num2
        else:
            return "❌ Invalid operation"
        
        return f"✅ Result: {result}"
    except ValueError:
        return "❌ Error: Please enter valid numbers"

# Text analysis function
def analyze_text(text):
    if not text or text.strip() == "":
        return "📝 Please enter some text to analyze."
    
    words = text.split()
    chars = len(text)
    chars_no_spaces = len(text.replace(" ", ""))
    word_count = len(words)
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    analysis = f"📊 **Text Analysis Results:**\n\n"
    analysis += f"• **Characters:** {chars}\n"
    analysis += f"• **Characters (no spaces):** {chars_no_spaces}\n"
    analysis += f"• **Words:** {word_count}\n"
    analysis += f"• **Sentences:** {sentence_count if sentence_count > 0 else 1}\n"
    
    if word_count > 0:
        avg_word_length = chars_no_spaces / word_count
        analysis += f"• **Average word length:** {avg_word_length:.2f} characters\n"
    
    return analysis

def word_frequency_analyzer(text):
    if not text or text.strip() == "":
        return "📝 Please enter some text to analyze."
    
    # Clean text and split into words
    words = re.sub(r'[^\w\s]', ' ', text.lower()).split()
    
    if not words:
        return "No valid words found in the text."
    
    # Calculate statistics
    word_counts = Counter(words)
    total_words = len(words)
    unique_words = len(word_counts)
    top_words = word_counts.most_common(5)
    
    # Format results
    result = f"📊 **Word Frequency Analysis**\n\n"
    result += f"• **Total words:** {total_words:,}\n"
    result += f"• **Unique words:** {unique_words:,}\n\n"
    
    result += "**Top 5 Most Frequent Words:**\n"
    for i, (word, count) in enumerate(top_words, 1):
        percentage = (count / total_words) * 100
        result += f"{i}. '{word}': {count:,} ({percentage:.1f}%)\n"
    
    return result

# Create tabbed interface with dark theme
with gr.Blocks(
    title="Gardio - December Lab",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
        neutral_hue="slate",
        radius_size=gr.themes.sizes.radius_md,
        font=["Inter", "sans-serif"],
    )
) as demo:
    # Custom CSS for additional styling
    css = """
    .gradio-container {
        background: linear-gradient(135deg, #1e1e2f 0%, #1a1a2e 100%) !important;
    }
    .gradio-header {
        color: white !important;
    }
    .tab-nav button {
        font-weight: 600 !important;
    }
    """
    demo.css = css
    gr.Markdown(
        """
        # ⚡ Gardio - December Lab
        ### A personal experimental Space for learning AI/ML deployment
        
        Created by **Xeyronox** for December 2025 transformation journey.
        """
    )
    
    with gr.Tabs():
        # Welcome Tab
        with gr.Tab("👋 Welcome"):
            gr.Markdown("### Get a personalized welcome message!")
            with gr.Row():
                with gr.Column():
                    name_input = gr.Textbox(
                        label="Enter your name",
                        placeholder="Type your name here...",
                        lines=1
                    )
                    welcome_btn = gr.Button("Get Welcome Message", variant="primary")
                with gr.Column():
                    welcome_output = gr.Textbox(
                        label="Welcome Message",
                        lines=6,
                        interactive=False
                    )
            
            welcome_btn.click(
                fn=welcome,
                inputs=name_input,
                outputs=welcome_output
            )
            
            gr.Examples(
                examples=[["Xeyronox"], ["Developer"], ["AI Enthusiast"]],
                inputs=name_input
            )
        
        # Calculator Tab
        with gr.Tab("🔢 Calculator"):
            gr.Markdown("### Simple calculator for basic operations")
            with gr.Row():
                with gr.Column():
                    num1 = gr.Number(label="First Number", value=0)
                    operation = gr.Radio(
                        choices=["Add ➕", "Subtract ➖", "Multiply ✖️", "Divide ➗"],
                        label="Operation",
                        value="Add ➕"
                    )
                    num2 = gr.Number(label="Second Number", value=0)
                    calc_btn = gr.Button("Calculate", variant="primary")
                with gr.Column():
                    calc_output = gr.Textbox(
                        label="Result",
                        lines=3,
                        interactive=False
                    )
            
            calc_btn.click(
                fn=calculate,
                inputs=[num1, operation, num2],
                outputs=calc_output
            )
            
            gr.Examples(
                examples=[
                    [10, "Add ➕", 5],
                    [20, "Multiply ✖️", 3],
                    [100, "Divide ➗", 4]
                ],
                inputs=[num1, operation, num2]
            )
        
        # Text Analyzer Tab
        with gr.Tab("📝 Text Analyzer"):
            gr.Markdown("### Analyze your text for word count, character count, and more")
            with gr.Row():
                with gr.Column():
                    text_input = gr.Textbox(
                        label="Enter text to analyze",
                        placeholder="Type or paste your text here...",
                        lines=8
                    )
                    analyze_btn = gr.Button("Analyze Text", variant="primary")
                with gr.Column():
                    text_output = gr.Textbox(
                        label="Analysis Results",
                        lines=8,
                        interactive=False
                    )
            
            analyze_btn.click(
                fn=analyze_text,
                inputs=text_input,
                outputs=text_output
            )
            
            gr.Examples(
                examples=[
                    ["Hello World! This is a test sentence."],
                    ["AI and Machine Learning are transforming the world."]
                ],
                inputs=text_input
            )
        
        # Word Frequency Counter Tab
        with gr.Tab("📊 Word Frequency"):
            gr.Markdown("### Analyze word frequency in your text")
            with gr.Row():
                with gr.Column():
                    freq_input = gr.Textbox(
                        label="Enter text to analyze",
                        placeholder="Paste your text here to see word frequency...",
                        lines=8
                    )
                    freq_btn = gr.Button("Analyze Word Frequency", variant="primary")
                with gr.Column():
                    freq_output = gr.Textbox(
                        label="Word Frequency Analysis",
                        lines=8,
                        interactive=False
                    )
            
            freq_btn.click(
                fn=word_frequency_analyzer,
                inputs=freq_input,
                outputs=freq_output
            )
            
            gr.Examples(
                examples=[["The quick brown fox jumps over the lazy dog. The quick brown fox is fast."]],
                inputs=freq_input
            )
        
        # Text Transform Tab (Day 2 Addition)
        with gr.Tab("🔄 Text Transform"):
            gr.Markdown("### Transform your text in fun and useful ways!")
            with gr.Row():
                with gr.Column():
                    transform_input = gr.Textbox(
                        label="Enter text to transform",
                        placeholder="Type your text here...",
                        lines=5
                    )
                    transform_type = gr.Radio(
                        choices=[
                            "🔄 Reverse Text",
                            "🔼 UPPERCASE",
                            "🔽 lowercase",
                            "📏 Remove Spaces",
                            "🎯 Count Vowels & Consonants"
                        ],
                        label="Choose transformation",
                        value="🔄 Reverse Text"
                    )
                    transform_btn = gr.Button("Transform", variant="primary")
                with gr.Column():
                    transform_output = gr.Textbox(
                        label="Transformed Text",
                        lines=8,
                        interactive=False
                    )
            
            def transform_text(text, transform_type):
                if not text or text.strip() == "":
                    return "⚠️ Please enter some text to transform."
                
                if transform_type == "🔄 Reverse Text":
                    return text[::-1]
                elif transform_type == "🔼 UPPERCASE":
                    return text.upper()
                elif transform_type == "🔽 lowercase":
                    return text.lower()
                elif transform_type == "📏 Remove Spaces":
                    return text.replace(" ", "")
                elif transform_type == "🎯 Count Vowels & Consonants":
                    vowels = "aeiouAEIOU"
                    vowel_count = sum(1 for char in text if char in vowels)
                    consonant_count = sum(1 for char in text if char.isalpha() and char not in vowels)
                    total_alpha = sum(1 for char in text if char.isalpha())
                    
                    result = f"📊 **Character Analysis:**\n\n"
                    result += f"• **Vowels:** {vowel_count}\n"
                    result += f"• **Consonants:** {consonant_count}\n"
                    result += f"• **Total Letters:** {total_alpha}\n"
                    if total_alpha > 0:
                        vowel_percent = (vowel_count / total_alpha) * 100
                        result += f"• **Vowel Percentage:** {vowel_percent:.1f}%\n"
                    result += f"\n**Original Text:**\n{text}"
                    return result
                
                return text
            
            transform_btn.click(
                fn=transform_text,
                inputs=[transform_input, transform_type],
                outputs=transform_output
            )
            
            gr.Examples(
                examples=[
                    ["Hello World!", "🔄 Reverse Text"],
                    ["make this loud", "🔼 UPPERCASE"],
                    ["MAKE THIS QUIET", "🔽 lowercase"]
                ],
                inputs=[transform_input, transform_type]
            )
    
    gr.Markdown(
        """
        ---
        **Powered by Gradio 6.0.2** | Built with ❤️ by Xeyronox
        """
    )

if __name__ == "__main__":
    demo.launch()
