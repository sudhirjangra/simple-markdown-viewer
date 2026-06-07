# Markdown Studio 📝
A fast, standalone Markdown reader with live GitHub-style rendering, built with Python and PyQt6.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

## Features
* 🌓 **Dynamic Themes:** Toggle between GitHub Light and Dark modes.
* 📑 **Interactive Outline:** Auto-generated Table of Contents for easy navigation.
* 🛡️ **Full Rendering:** Supports tables, code blocks, and remote image badges (like shields.io).
* 🪶 **Standalone:** No heavy web-browsers or electron bloat.

## Download & Install
Head over to the [Releases](../../releases) page to download the latest version for your OS.
* **Windows:** Download the `.exe` and double click to run.
* **Linux:** Download the binary, make it executable (`chmod +x MarkdownViewer`), and run it.

## For Developers
If you want to run from source:
```bash
git clone https://github.com/sudhirjangra/simple-markdown-viewer.git
cd simple-markdown-viewer
pip install -r requirements.txt
python app.py