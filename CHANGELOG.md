# 📜 Changelog

All notable changes to the **Gardio** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.3.0] - Turbo Edition ⚡
**Released**: 2025-12-12

### 🚀 Major Features
- **Turbo Mode**: Implemented client-side JavaScript for **<0.10s latency** on common tools.
- **Gradio 6.1.0**: Upgraded core framework to latest version with native JS/CSS injection.
- **New Tools**:
  - **📝 JSON Formatter**: Validate and pretty-print JSON.
  - **⚖️ Diff Checker**: Side-by-side text comparison.
  - **🔐 Encoder**: Base64 & URL Encode/Decode.

### ⚡ Turbo Tools (Instant)
- **Transform**: Reverse, Uppercase, Lowercase, Title Case, etc.
- **Word Counter**: Real-time typing statistics.
- **Trimmer**: Instant whitespace cleaning.
- **String Ops**: Split, Join, Length checks.

### 🛠️ Improvements
- **UI Consistency**: Standardized labels for all 16 Toolbox items.
- **Performance**: Disabled debug logging and pre-compiled Regex patterns.
- **Fixes**: Resolved JS scope issues (`window.js_logic`) and added missing CSS classes.

---

## [2.2.0] - Feature Expansion 🛠️
**Released**: 2025-12-10

### ✨ New Features
- **Toolbox Expansion**: Added 8 new tools including Number/URL Extractor and Python Data Converters (List, Tuple, Dict).
- **Chat Enhancements**: Added multi-language support (Hola, Bonjour, Namaste) and expanded Jokes/Quotes.
- **UI Polish**: Improved Glassmorphism visuals.

### 🐛 Fixes
- **API Handling**: Moved core functions to top-level to fix "No API found" errors on Hugging Face.
- **Interaction**: Converted dropdowns to Radio buttons for better mobile usability.

---

## [2.0.0] - The Foundation 🏗️
**Released**: 2025-12-08

- **Complete Rewrite**: Re-architected application with cleaner code structure.
- **Design System**: Introduced "Premium Glass" dark UI theme.
- **Stability**: Robust error handling and input validation.

---
*Maintained by Xeyronox*
