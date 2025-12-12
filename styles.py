"""
Gardio CSS Styles
"""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
:root { --bg:#050508; --surface:rgba(15,15,20,0.8); --glass:rgba(255,255,255,0.03); --border:rgba(255,255,255,0.08); --accent:#8b5cf6; --accent2:#06b6d4; --text:#f8fafc; --gradient:linear-gradient(135deg,#8b5cf6,#06b6d4); }
body,.gradio-container{background:var(--bg)!important;font-family:'Inter',sans-serif!important;color:var(--text)!important}
.block,.form{background:var(--surface)!important;backdrop-filter:blur(20px)!important;border:1px solid var(--border)!important;border-radius:16px!important}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:12px;padding:12px}
.stat-card{background:var(--glass);border:1px solid var(--border);border-radius:12px;padding:16px;text-align:center}
.stat-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.stat-card .value{font-size:1.8rem;font-weight:700;color:var(--accent2);margin-top:8px;display:block}
.freq-row{display:grid;grid-template-columns:30px 1fr 40px;gap:8px;align-items:center;margin-bottom:10px;padding:8px;background:var(--glass);border-radius:8px}
.bar-fill{height:100%;background:var(--gradient);border-radius:2px}
textarea,input{background:rgba(0,0,0,0.4)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--text)!important}
textarea:focus,input:focus{border-color:var(--accent)!important}
button.primary{background:var(--gradient)!important;border:none!important;border-radius:10px!important;font-weight:600!important}
.chatbot{height:400px!important}
.empty-state,.error-state{padding:20px;text-align:center;border-radius:10px;background:var(--glass);border:1px solid var(--border);color:var(--text);font-weight:600}
.error-state{border-color:#ef4444;color:#ef4444}
"""
