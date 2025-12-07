# Changelog

All notable changes documented here.

## [2.1.0] - 2025-12-07

### Added
- **Enhanced Chatbot** - 11+ commands (hello, help, time, date, joke, quote, author, version, tips, thanks, bye, clear)
- **Remove Duplicates Tool** - New Toolbox sub-tab to remove duplicate lines
- **Radio Selection** - Transform and Calculator now use radio buttons (no typing)

### Fixed
- **No API Found Error** - Moved inline functions to top-level (HuggingFace compatibility)
- **Button Handlers** - All buttons now use pre-defined output components
- **Dropdown Issue** - Replaced with Radio buttons for pure click-to-select

### Changed
- Version bumped to 2.1.0
- Improved chatbot responses with markdown formatting
- Added more programming jokes and quotes

---

## [2.0.0] - 2025-12-07

### 🔄 Full Rewrite
Complete code reset following audit checklist for stability and reliability.

### Added
- **Debug Logging** - All functions log to console for HF debugging
- **Input Validation** - `validate_text()` helper prevents crashes
- **Error Handling** - Try-except wrappers on all core functions
- **Fallback UI** - Empty/error states show friendly messages
- **Read Time** - Analytics now shows estimated reading time
- **Premium Glass CSS** - Glassmorphism, gradients, neon glow

### Changed
- **Architecture** - Clean separation: Constants → Helpers → Logic → UI
- **CSS** - Mobile-first design
- **Chat** - Keyword-based responses (no ML dependencies)

---

## [1.x] - Previous Versions

See git history for Day 1-6 changes.

---

**Maintained by Xeyronox**
