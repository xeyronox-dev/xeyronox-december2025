# Changelog

All notable changes to the Gardio project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added - 2025-12-04
- **Word Frequency Counter**
  - Added new tab for analyzing word frequencies
  - Shows top 5 most repeated words with percentages
  - Displays total word count and unique word count
  - Includes example text for quick testing

### Changed - 2025-12-04
- **UI/UX Overhaul**
  - Completely redesigned dark theme with gradient background
  - Improved typography with Inter font family
  - Enhanced tab navigation with better visual hierarchy
  - Added smooth animations and transitions
  - Improved responsive design for all screen sizes

### Updated - 2025-12-04
- **Dependencies**
  - Upgraded Gradio to v4.19.0
  - Added NLTK for advanced text processing
  - Included development dependencies (Black, Flake8)
  - Updated Python version requirements

### Fixed - 2025-12-04
- Fixed text analysis accuracy
- Improved error handling in calculator
- Addressed minor UI inconsistencies
- Optimized performance for large text inputs
- Enhanced `README.md` with feature list and tech stack documentation
- Cleaned up `.gitattributes` by:
  - Removing duplicate LFS entries
  - Organizing entries by category (Archives, Data Files, Model Files)
  - Adding helpful section comments
- Updated `requirements.txt` with additional dependency: `python-dateutil>=2.8.0`

### Fixed - 2025-12-01
- Resolved git interactive rebase state
- Cleared wrong GitHub cached credentials (carfunfactory user)
- Fixed `.gitattributes` file that had git commands in the beginning
- Configured dual Git remotes (github and huggingface)

### Deployment - 2025-12-01
- Successfully deployed to GitHub: https://github.com/xeyronox-dev/xeyronox-december2025
- Successfully deployed to HuggingFace Spaces: https://huggingface.co/spaces/xeyronox/Gardio
- Commit: `1f7a399` - "Clean up .gitattributes and prepare for dual deployment"

## [Initial] - 2025-12-01

### Added
- Initial Gradio application with simple welcome function
- Basic `requirements.txt` with `gradio==4.31.5`
- Git LFS configuration in `.gitattributes`
- README.md with HuggingFace Space metadata

---

**Maintained by Xeyronox**
