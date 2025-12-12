"""
⚡ GARDIO - Text Intelligence Suite
Author: Xeyronox | Version: 2.3.0
Design: Clean, Robust, Mobile-First
"""

import gradio as gr
from constants import VERSION
from styles import CSS
from javascript import JS_LOGIC
import logic

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
            msg.submit(fn=logic.chat_respond, inputs=[msg, chatbot], outputs=[chatbot, msg])
            send_btn.click(fn=logic.chat_respond, inputs=[msg, chatbot], outputs=[chatbot, msg])
        
        with gr.Tab("📊 Analytics"):
            with gr.Row():
                with gr.Column():
                    txt_in = gr.Textbox(lines=6, placeholder="Paste text...")
                    analyze_btn = gr.Button("Analyze", variant="primary")
                stats_out = gr.HTML()
            txt_in.change(fn=logic.analyze_text, inputs=[txt_in], outputs=[stats_out])
            analyze_btn.click(fn=logic.analyze_text, inputs=[txt_in], outputs=[stats_out])
        
        with gr.Tab("📈 Frequency"):
            with gr.Row():
                freq_in = gr.Textbox(lines=5, placeholder="Enter text...")
                freq_out = gr.HTML()
            gr.Button("Find Keywords", variant="primary").click(fn=logic.count_frequency, inputs=[freq_in], outputs=[freq_out])
            freq_in.change(fn=logic.count_frequency, inputs=[freq_in], outputs=[freq_out])
        
        with gr.Tab("🛠️ Toolbox"):
            with gr.Tabs():
                # Client-Side Tools (Turbo) ⚡
                with gr.Tab("⚡ Transform"):
                    t_in = gr.Textbox(label="Input", lines=3)
                    t_mode = gr.Radio(["Reverse", "UPPERCASE", "lowercase", "Title Case", "Sentence Case", "No Spaces", "No Punctuation", "Shuffle Words"], value="Reverse", label="Transformation")
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
                    str_op = gr.Radio(["Length", "Split (comma)", "Split (space)", "Join (-)", "Strip", "Is Alpha", "Is Digit", "Is Alnum"], value="Length", label="Operation")
                    str_out = gr.Textbox(label="Result")
                    str_in.change(None, [str_in, str_op], str_out, js="(t, o) => js_logic.stringOps(t, o)")
                    str_op.change(None, [str_in, str_op], str_out, js="(t, o) => js_logic.stringOps(t, o)")

                # Server-Side Tools
                with gr.Tab("🔢 Calculator"):
                    num_a = gr.Number(value=0, label="A")
                    op = gr.Radio(["+", "-", "×", "÷", "^", "%"], value="+", label="Operator")
                    num_b = gr.Number(value=0, label="B")
                    calc_out = gr.Textbox(label="Result")
                    gr.Button("Calculate", variant="primary").click(fn=logic.calculate, inputs=[num_a, op, num_b], outputs=[calc_out])

                # New Tools (Batch 2)
                with gr.Tab("📝 JSON"):
                    json_in = gr.Textbox(lines=6, placeholder='{"key": "value"}', label="Bad JSON")
                    json_out = gr.Textbox(lines=6, label="Pretty JSON")
                    gr.Button("Format", variant="primary").click(fn=logic.format_json, inputs=[json_in], outputs=[json_out])
                
                with gr.Tab("⚖️ Diff"):
                    d_a = gr.Textbox(lines=3, label="Text A")
                    d_b = gr.Textbox(lines=3, label="Text B")
                    d_out = gr.Textbox(lines=6, label="Differences")
                    gr.Button("Compare", variant="primary").click(fn=logic.diff_text, inputs=[d_a, d_b], outputs=[d_out])
                
                with gr.Tab("🔐 Encoder"):
                    enc_in = gr.Textbox(lines=3, placeholder="Text...", label="Input")
                    enc_mode = gr.Radio(["Base64 Encode", "Base64 Decode", "URL Encode", "URL Decode"], value="Base64 Encode", label="Mode")
                    enc_out = gr.Textbox(lines=3, label="Output")
                    gr.Button("Convert", variant="primary").click(fn=logic.encode_decode, inputs=[enc_in, enc_mode], outputs=[enc_out])

                # Standard Tools
                with gr.Tab("🧹 Duplicates"):
                    rd_in = gr.Textbox(lines=4, label="Paste Text")
                    rd_out = gr.Textbox(lines=4, label="Unique Lines")
                    rd_in.change(fn=logic.remove_duplicates, inputs=[rd_in], outputs=[rd_out])

                with gr.Tab("🔢 Numbers"):
                    ne_in = gr.Textbox(lines=4, label="Paste Text")
                    ne_out = gr.Textbox(lines=2, label="Extracted Numbers")
                    ne_in.change(fn=logic.extract_numbers, inputs=[ne_in], outputs=[ne_out])

                with gr.Tab("🔗 URLs"):
                    ue_in = gr.Textbox(lines=4, label="Paste Text")
                    ue_out = gr.Textbox(lines=3, label="Extracted URLs")
                    ue_in.change(fn=logic.extract_urls, inputs=[ue_in], outputs=[ue_out])
                
                with gr.Tab("🔍 Replace"):
                    fr_text = gr.Textbox(lines=3, label="Input Text")
                    with gr.Row():
                        fr_find = gr.Textbox(label="Find")
                        fr_replace = gr.Textbox(label="Replace")
                    fr_out = gr.Textbox(lines=3, label="Result")
                    gr.Button("Replace All", variant="primary").click(fn=logic.find_replace, inputs=[fr_text, fr_find, fr_replace], outputs=[fr_out])

                # Python Data Tools (Simple)
                with gr.Tab("📋 List"):
                    l_in = gr.Textbox(lines=4, label="Items (One per line)")
                    l_out = gr.Textbox(lines=2, label="Python List")
                    gr.Button("Convert").click(fn=logic.text_to_list, inputs=[l_in], outputs=[l_out])
                
                with gr.Tab("📦 Tuple"):
                    tup_in = gr.Textbox(lines=4, label="Items (One per line)")
                    tup_out = gr.Textbox(lines=2, label="Python Tuple")
                    gr.Button("Convert").click(fn=logic.text_to_tuple, inputs=[tup_in], outputs=[tup_out])
                
                with gr.Tab("📖 Dict"):
                    dict_in = gr.Textbox(lines=4, label="Key:Value (One per line)")
                    dict_out = gr.Textbox(lines=2, label="Python Dict")
                    gr.Button("Convert").click(fn=logic.text_to_dict, inputs=[dict_in], outputs=[dict_out])

    gr.HTML('<div style="text-align:center;padding:20px;color:#6b7280;font-size:0.75rem">Built with ❤️ by Xeyronox</div>')

if __name__ == "__main__":
    demo.launch()
