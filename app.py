import gradio as gr

def welcome(name):
    message = (
        f"Welcome to December Lab, {name}! "
        f"This Space is created by Xeyronox for AI/ML learning, "
        f"project testing, and deployment experiments."
    )
    return message

demo = gr.Interface(
    fn=welcome,
    inputs=gr.Textbox(label="Enter your name"),
    outputs=gr.Textbox(label="Response"),
    title="December Lab",
    description="A personal experimental Space for learning AI/ML deployment."
)

demo.launch()
