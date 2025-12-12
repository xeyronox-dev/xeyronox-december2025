# 🎨 Gardio Assets

This directory serves as the static storage for all visual and data assets used in the Gardio application.

## 📂 Directory Structure

| Directory | Content Type | Git LFS | Description |
|-----------|--------------|---------|-------------|
| `images/` | `.png`, `.jpg`, `.svg` | No | Logos, icons, banners, and screenshot evidence. |
| `data/` | `.json`, `.csv`, `.txt` | No | Sample datasets for verification and demos. |
| `models/` | `.bin`, `.pt`, `.safetensors` | **Yes** | Local model weights (if any). |

## ℹ️ Guidelines

1. **Optimization**: Ensure images are compressed (WebP preferred) to keep repo size small.
2. **Naming**: Use `snake_case` for all filenames (e.g., `app_logo_dark.png`).
3. **LFS**: Any binary file >10MB **MUST** be tracked via Git LFS.

## 📜 Attribution

If you use third-party assets (icons, fonts), listed them below:
- **Fonts**: [Inter](https://fonts.google.com/specimen/Inter) (Google Fonts)
- **Icons**: Standard Emoji Set (v15.0)
