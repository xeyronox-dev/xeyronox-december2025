# Changelog

All notable changes documented here.

## [2.0.0] - 2025-12-07

### 🔄 Full Rewrite
Complete code reset following audit checklist for stability and reliability.

### Added
- **Debug Logging** - All functions log to console for HF debugging
- **Input Validation** - `validate_text()` helper prevents crashes
- **Error Handling** - Try-except wrappers on all core functions
- **Fallback UI** - Empty/error states show friendly messages
- **Read Time** - Analytics now shows estimated reading time

### Changed
- **Architecture** - Clean separation: Constants → Helpers → Logic → UI
- **CSS** - Mobile-first design, simpler than glassmorphism
- **Chat** - Keyword-based responses (no ML dependencies)
- **Version** - Bumped to 2.0.0

### Fixed
- Gradio 5.x message format compatibility
- Stop word filtering in frequency analysis
- Long text input handling (50k char limit)

### Removed
- Heavy visual effects (performance)
- Pattern-based chatbot (reliability)

---

## [1.x] - Previous Versions

See git history for Day 1-6 changes including:
- Premium Glass UI
- Real-Time Analysis
- Toolbox Expansion
- Chat Features

---

**Maintained by Xeyronox**
