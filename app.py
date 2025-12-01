import gradio as gr
from datetime import datetime

# ===== Core Functions =====

def welcome_message(name):
    """Welcome function with personalized greeting"""
    if not name or name.strip() == "":
        return "👋 Welcome to Gardio! Please enter your name to get started."
    
    current_time = datetime.now().strftime("%I:%M %p")
    message = (
        f"🎉 Welcome to December Lab, **{name}**!\n\n"
        f"Current Time: {current_time}\n\n"
        f"This Space is created by **Xeyronox** for AI/ML learning, "
        f"project testing, and deployment experiments.\n\n"
        f"Explore the tabs above to try different tools and features! ⚡"
    )
    return message

def text_analyzer(text):
    """Analyze text and provide statistics"""
    if not text or text.strip() == "":
        return "Please enter some text to analyze."
    
    words = text.split()
    characters = len(text)
    characters_no_spaces = len(text.replace(" ", ""))
    word_count = len(words)
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    
    analysis = (
        f"📊 **Text Analysis Results**\n\n"
        f"• Characters (with spaces): {characters}\n"
        f"• Characters (without spaces): {characters_no_spaces}\n"
        f"• Words: {word_count}\n"
        f"• Sentences: {sentence_count}\n"
        f"• Average word length: {characters_no_spaces/word_count:.2f} characters\n"
    )
    return analysis

def calculator(num1, operation, num2):
    """Simple calculator function"""
    try:
        num1 = float(num1)
        num2 = float(num2)
        
        if operation == "Add (+)":
            result = num1 + num2
        elif operation == "Subtract (-)":
            result = num1 - num2
        elif operation == "Multiply (×)":
            result = num1 * num2
        elif operation == "Divide (÷)":
            if num2 == 0:
                return "❌ Error: Cannot divide by zero!"
            result = num1 / num2
        else:
            return "❌ Error: Invalid operation"
        
        return f"✅ **Result:** {num1} {operation.split()[1]} {num2} = **{result}**"
    except ValueError:
        return "❌ Error: Please enter valid numbers"

def generate_gradient(color1, color2):
    """Generate a simple gradient description"""
    gradient_text = (
        f"🎨 **Gradient Preview**\n\n"
        f"Color 1: {color1}\n"
        f"Color 2: {color2}\n\n"
        f"This would create a beautiful gradient from {color1} to {color2}!"
    )
    return gradient_text

# ===== Custom Theme =====
custom_theme = gr.themes.Soft(
    primary_hue="emerald",
    secondary_hue="blue",
    neutral_hue="slate",
    font=("Inter", "sans-serif")
).set(
    body_background_fill="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    body_background_fill_dark="linear-gradient(135deg, #1e3a8a 0%, #312e81 100%)",
)

# ===== Build Interface =====

with gr.Blocks(theme=custom_theme, title="Gardio - Xeyronox December Lab") as demo:
    
    # Header
    gr.Markdown(
        """
        # ⚡ Gardio - December Lab
        ### A personal experimental Space for learning AI/ML deployment
        *Created by Xeyronox for testing and deployment experiments*
        """
    )
    
    # Tabs
    with gr.Tabs():
        
        # Tab 1: Welcome
        with gr.Tab("🏠 Welcome"):
            with gr.Row():
                with gr.Column(scale=2):
                    name_input = gr.Textbox(
                        label="Enter Your Name",
                        placeholder="Type your name here...",
                        lines=1
                    )
                    welcome_btn = gr.Button("Get Welcome Message", variant="primary")
                with gr.Column(scale=3):
                    welcome_output = gr.Markdown(label="Welcome Message")
            
            # Examples
            gr.Examples(
                examples=[["Xeyronox"], ["Developer"], ["AI Enthusiast"]],
                inputs=name_input
            )
            
            welcome_btn.click(
                fn=welcome_message,
                inputs=name_input,
                outputs=welcome_output
            )
        
        # Tab 2: Text Analyzer
        with gr.Tab("📝 Text Analyzer"):
            with gr.Row():
                with gr.Column():
                    text_input = gr.Textbox(
                        label="Enter Text to Analyze",
                        placeholder="Type or paste your text here...",
                        lines=5
                    )
                    analyze_btn = gr.Button("Analyze Text", variant="primary")
                with gr.Column():
                    analysis_output = gr.Markdown(label="Analysis Results")
            
            analyze_btn.click(
                fn=text_analyzer,
                inputs=text_input,
                outputs=analysis_output
            )
        
        # Tab 3: Calculator
        with gr.Tab("🧮 Calculator"):
            with gr.Row():
                num1_input = gr.Number(label="Number 1", value=0)
                operation_input = gr.Dropdown(
                    choices=["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)"],
                    label="Operation",
                    value="Add (+)"
                )
                num2_input = gr.Number(label="Number 2", value=0)
            
            calc_btn = gr.Button("Calculate", variant="primary")
            calc_output = gr.Markdown(label="Result")
            
            calc_btn.click(
                fn=calculator,
                inputs=[num1_input, operation_input, num2_input],
                outputs=calc_output
            )
        
        # Tab 4: Gradient Preview
        with gr.Tab("🎨 Gradient Maker"):
            with gr.Row():
                color1_input = gr.ColorPicker(label="Color 1", value="#667eea")
                color2_input = gr.ColorPicker(label="Color 2", value="#764ba2")
            
            gradient_btn = gr.Button("Preview Gradient", variant="primary")
            gradient_output = gr.Markdown(label="Gradient Info")
            
            gradient_btn.click(
                fn=generate_gradient,
                inputs=[color1_input, color2_input],
                outputs=gradient_output
            )
        
        # Tab 5: About
        with gr.Tab("ℹ️ About"):
            gr.Markdown(
                """
                ## About Gardio
                
                **Gardio** is a demonstration Gradio Space created as part of the Xeyronox December 2025 transformation project.
                
                ### Features
                - 🏠 Personalized welcome messages
                - 📝 Text analysis tool
                - 🧮 Simple calculator
                - 🎨 Gradient color preview
                
                ### Tech Stack
                - **Framework:** Gradio 6.0.1
                - **Deployment:** HuggingFace Spaces
                - **Repository:** GitHub & HuggingFace
                
                ### Links
                - 🔗 [GitHub Repository](https://github.com/xeyronox-dev/xeyronox-december2025)
                - 🤗 [HuggingFace Space](https://huggingface.co/spaces/xeyronox/Gardio)
                
                ---
                *Built with ❤️ by Xeyronox | December 2025*
                """
            )
    
    # Footer
    gr.Markdown("---")
    gr.Markdown("⚡ **Gardio v1.0** | Powered by Gradio")

# Launch
if __name__ == "__main__":
    demo.launch()

